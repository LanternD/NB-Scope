# coding = utf-8
import os
import pickle
import re
import time
import xml.etree.cElementTree as ET
from collections import OrderedDict

import pandas as pd

from LogDecoders import DebugLogDecoder
from Utils import *


class RawLogProcessor(DebugLogDecoder):

    def __init__(self, dev_name, filter_dict):

        super(RawLogProcessor, self).__init__(dev_name, filter_dict)

        self.data_df = None
        self.filter_dict = filter_dict
        self.u = Utils()
        self.config = self.u.load_config('./config.json')
        self.global_path = self.config['env_prefix'][self.u.log_in][self.u.os]
        print(INFO, 'Global prefix', self.global_path)

        self.data_dir_amarisoft = self.global_path + self.config['data_path_prefix_amarisoft']
        self.data_dir_cn = self.global_path + self.config['data_path_prefix_cn']
        self.output_dir = self.global_path + self.config['output_path']
        self.load_xml()

        # Processing log
        self.f_log = open(self.output_dir +
                          self.config['decoding_log_file_name'], 'a', encoding="utf-8")

    def load_xml(self):
        xml_path = self.global_path + self.config['messages_xml_path']
        msg_tree = ET.parse(xml_path)
        root = msg_tree.getroot()
        type_set = {}
        root = root[0]
        for child in root:  # each child is a message item
            # msg_name = child[0].text
            msg_id = child[1].text
            if len(child) > 4:
                msg_size = child[4].text
            else:
                msg_size = 0
            if msg_size != 0:
                self.message_dict[msg_id] = child
            try:
                fields = child[6]
            except IndexError:
                # this is a incomplete message definition. ignore it.
                # print(msg_id)
                continue
            for field in fields:
                msg_type = field[1].text
                msg_type_size = field[3].text
                # print(msg_type)
                type_set[msg_type] = msg_type_size

        print('[INFO] Message dict length:', len(self.message_dict))
        # print(type_set)
        print('[INFO] Available types:', len(type_set))

    def get_n_bytes(self, row_buf, i, n):

        bytes = []
        for x in range(n):
            try:
                bytes.append(row_buf[i+2*x:i+2*x+2])
            except IndexError:
                bytes = []
        return bytes, i+2*n

    def load_one_raw_log(self, full_path):
        with open(full_path, 'rb') as f_t:
            row_all = f_t.read()
            f_t.close()
        # DBG
        return row_all  # all the data in the file.

    def generate_decoded_output_file_name(self, full_path):
        path_buf = full_path.split('/')
        idx = path_buf.index('STM32 Node Deployment')
        # idx = path_buf.index('Amarisoft_SDR_Optimization')
        # idx = path_buf.index('STM32 SDIO')
        output_file_name = '_'.join(path_buf[idx+1:-1]+[path_buf[-1].split('.')[0]])
        output_file_name = 'decoded_' + output_file_name + '.pkl'
        # print(DBG, output_file_name)
        return output_file_name

    def state_machine(self, row_all):

        states = {'UNKNOWN': 0, 'PREAMBLE': 1, 'COUNT': 2, 'TICK': 3,
                  'DATA': 5, 'LENGTH': 4, 'FINISHED': 6}  # UART state machine
        str_buf = []
        raw_buf = []
        st = states['PREAMBLE']
        msg_all = []

        # Initialize local variable to prevent warning.
        seq_num = 0
        time_tick = 0
        parsed_msg = ''
        payload_len = 1
        preamble_count = 0  # count of '%DBG:'
        msg_count_bf = 0  # before filter
        app_rep_flag = False
        dummy = []

        empty_msg_list = [0, .0]  # Order: seq_num, timestamp, time tick,
        parsed_log_list = empty_msg_list.copy()
        # print(row_all)

        row_all = row_all.hex()
        row_buf = row_all.upper()

        i = 0
        buf_len = len(row_buf)
        print(INFO, 'Length of byte buffer', buf_len)
        quantile = 50000  # every 50k bytes

        while i <= len(row_buf):
            if st == states['PREAMBLE']:
                new_byte, i = self.get_n_bytes(row_buf, i, 1)

                if len(msg_all) % quantile == 1:
                    # Print updates
                    # print(DBG, msg_all[-1])
                    print(INFO, 'Processed bytes:', i)

                if new_byte == ['25']:  # '%'
                    str_buf.append(new_byte)
                    new_byte, i = self.get_n_bytes(row_buf, i, 4)
                    dbg_str = ''.join(new_byte)
                    if dbg_str == '4442473A':  # 'DBG:'
                        str_buf += new_byte
                        st = states['COUNT']
                        preamble_count += 1
                    else:
                        str_buf = []
                else:
                    str_buf = []  # Empty the buf and restart
            elif st == states['COUNT']:
                # 4 bytes' msg counter.
                byte_buf, i = self.get_n_bytes(row_buf, i, 4)

                num_temp = self.hex_to_decimal(byte_buf)
                if num_temp - seq_num != 1 and self.config['show_warning_msg']:
                    missing_log_msg = '[Warning] Inconsistent sequence number!\
                                This: {0}, Last: {1}'.format(num_temp, seq_num)
                    print(missing_log_msg)
                seq_num = num_temp
                parsed_log_list[0] = seq_num  # Update the dict

                # str_buf = []
                st = states['TICK']
            elif st == states['TICK']:
                byte_buf, i = self.get_n_bytes(row_buf, i, 4)

                time_tick = self.hex_to_decimal(byte_buf)
                parsed_log_list[1] = time_tick  # Update the dict

                dummy, i = self.get_n_bytes(row_buf, i, 4)

                if len(dummy) == 0:
                    st = states['PREAMBLE']
                    continue
                if dummy[0] == 'A':  # This is an application report message
                    app_rep_flag = True
                    parsed_log_list.append('APPLICATION_REPORT')
                else:
                    app_rep_flag = False
                    st = states['LENGTH']
            elif st == states['LENGTH']:
                byte_buf, i = self.get_n_bytes(row_buf, i, 2)

                payload_len = self.hex_to_decimal(byte_buf)
                # if max_len < payload_len:
                #     max_len = payload_len
                #     print('[INFO]Max payload length:', max_len)
                if payload_len > 720:
                    st = states['UNKNOWN']
                    if self.config['show_error_msg']:
                        print(ERR, 'Unbounded payload length.')
                    continue
                st = states['DATA']
            elif st == states['DATA']:
                # Read in the data as the length field specified.
                str_buf, i = self.get_n_bytes(row_buf, i, payload_len)

                raw_buf = parsed_log_list.copy()
                raw_buf.append('-'.join(str_buf))

                if app_rep_flag is True:
                    str_buf.reverse()  # There is another reverse in the hex to ascii function.
                    parsed_log_list.append(self.hex_to_ascii(str_buf))
                    self.application_report_export_processing(parsed_log_list)
                else:
                    disp_list = self.parse_one_msg_common(str_buf)
                    # disp_list order: msg_id_dec, msg_name, msg_src, msg_dest, msg_length, decoded_msg
                    parsed_log_list += disp_list  # parsed_log_list have time. disp_list only has message info.
                    # Now a complete debug log is processed.

                    msg_count_bf += 1
                    if len(parsed_log_list) >=3:
                        if parsed_log_list[3] not in self.filter_dict['FO']:
                            msg_all.append(parsed_log_list)

                st = states['FINISHED']
            elif st == states['FINISHED']:
                parsed_log_list = empty_msg_list.copy()
                st = states['PREAMBLE']  # Recycle the processing state machine
            elif st == states['UNKNOWN']:
                if self.config['show_error_msg']:
                    print(ERR, 'Something wrong happened. Reset to PREAMBLE state.')
                st = states['PREAMBLE']
        # All the bytes are processed.
        print(INFO,'Total number of messages in the log file:', msg_count_bf)
        print(INFO,'Number of useful messages:', len(msg_all))

        self.f_log.write('{0} / {1} / {2}\n'.format(len(msg_all), msg_count_bf, preamble_count))

        return msg_all

    def generate_raw_log_list(self, root_dir, data_dir, flag):
        file_size_threshold = 10000  # determine whether it is raw log.
        raw_log_path_list = []
        for p in data_dir:
            # print(DBG, self.data_dir+p)
            f_candidate = self.u.get_file_list(root_dir+p)
            # print(DBG, 'before', f_candidate)
            # Filter files by extension.
            allowed_extension = {'txt', 'uedl', 'log'}
            ext_examed = []
            for x in f_candidate:
                if x.split('.')[1] in allowed_extension:
                    # filter in the file needed.
                    if x.split('.')[1] == 'log':
                        if x.split('_')[1] == flag:
                            ext_examed.append(x)
                    else:
                        ext_examed.append(x)

            # print(DBG, 'after', ext_examed)
            # Filter files by file size
            for y in ext_examed:
                size = os.path.getsize(root_dir+p+y)
                # print('size:', size)
                if size > file_size_threshold:
                    raw_log_path_list.append(root_dir+p+y)

        # Final results
        print(INFO, raw_log_path_list)
        print(INFO, 'Number of log files:', len(raw_log_path_list))
        return raw_log_path_list

    def decode_one_file(self, fp, f_out_path=""):
        print(INFO, 'Working on:', fp[30:])
        start_time = time.time()
        row_all = self.load_one_raw_log(fp)
        if f_out_path == "":
            f_out_path = self.generate_decoded_output_file_name(fp)

        msg_all = self.state_machine(row_all)  # major point of execution
        # print("DEBUG**************************:")
        # for item in msg_all:
        #     print(item)
        with open(self.output_dir + 'decoded_pkl/' + f_out_path, 'wb') as f_pkl:    # write redirect to temp middle path
            pickle.dump(msg_all, f_pkl, protocol=pickle.HIGHEST_PROTOCOL)
            print(INFO, 'PKL written to', f_out_path)
        print(INFO, 'Processed:', fp[30:])
        print(INFO, 'Execution Time for this file: {0:.4f} s'.format(time.time()-start_time))

    def pipeline_from_raw_to_csv(self, log_list=[]):
        # Batch convert the raw file to message list.
        if len(log_list) == 0:
            log_list = self.generate_raw_log_list(self.data_dir_cn, self.config['data_folder_list_cn'], 'D')

        file_count = 0
        for fp in log_list:
            file_count += 1
            print(INFO, 'Progress: {0}/{1}'.format(file_count, len(log_list)))
            self.f_log.write('# File #{0}\n'.format(file_count))
            self.f_log.write('{0}\n'.format(fp))

            self.decode_one_file(fp, 'decoded_SZ_'+fp.split('/')[-1].split('.')[0]+'.pkl')

        self.f_log.flush()
        self.f_log.close()

    def generate_meta_csv(self):
        log_list = self.generate_raw_log_list(self.config["current_data_folder_list"], 'I')
        df = pd.DataFrame(columns=['node_id', 'test_id', 'opt_method', 'opt_var'])
        i = 0
        node_id, test_id, pack_id = 0, 0, 0
        for fp in log_list:
            # print(fp)

            fp_1 = fp.split('/')
            index = fp_1.index('Amarisoft_SDR_Optimization')
            dict_opt_method = {'Inactivetimer': 'timer',
                               'Threshold': 'rsrp_th'}

            opt_method = dict_opt_method[fp_1[index+1]]
            if opt_method == 'timer':
                opt_var = fp_1[index+3].split('=')[1][:-1]
            elif opt_method == 'rsrp_th':
                opt_var = fp_1[index+3]
            fp_2 = fp_1[-1].split('.')[0].split('_')
            if fp_2[0] == node_id and fp_2[2] == test_id:
                continue
            node_id, test_id, pack_id = fp_2[0], fp_2[2], fp_2[3]
            # print(opt_method, opt_var, node_id, test_id, pack_id)
            df.loc[i] = [node_id, test_id, opt_method, opt_var]
            i += 1
        # print(df)
        df.to_csv(self.output_dir + "csv_to_be_merged/amarisoft_test_meta_info.csv", index=False)
