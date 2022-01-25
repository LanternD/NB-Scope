from Utils import *
import pickle
import pandas as pd
import csv
import numpy as np
import pandas
from collections import OrderedDict
from DataVisualizer import DataVisualizer


class DeploymentDataProcessor(object):
    '''
    Naming:
        - extract_xx_from_yy(): take out the information from one msg logs and export to a csv.
        - visualize_xx(): call the plot function in the DataVisualizer module and plot something.
        - process_xx_log(): middle step of the pipeline.
    Data format convention:
        - csv: the column name should be all lower cases, connected with underline.
        - Data in the program: all should be in pandas DataFrame. Load and store through csv files.
    '''

    def __init__(self, whoami):

        self.u = Utils()
        self.config = self.u.load_config('./config.json')

        self.global_path = self.config['env_prefix'][whoami][self.u.os]
        print(INFO, 'Global prefix', self.global_path)

        self.output_dir = self.global_path + self.config['output_path']
        # self.pkl_dir = self.output_dir + 'decoded_pkl/'
        self.pkl_dir = 'E:/decoded_pkl/'
        self.rse_csv_output_dir = self.output_dir + 'rsrp_snr_ecl_output/'
        self.bler_report_csv_dir = self.output_dir + 'bler_csv/'
        self.dci_csv_dir = self.output_dir + 'dci_csv/'
        self.rar_csv_dir = self.output_dir + 'rar_csv/'
        self.merge_dir = self.output_dir + 'csv_to_be_merged/'
        self.meta_data = self.merge_dir + 'field_test_meta_info_cn.csv'
        self.pftp_data_dir = self.output_dir + 'post_ft_processing/'

        self.v = DataVisualizer(whoami)
        self.tts_ratio = 1000000  # time ticks to second ratio

    def get_decoded_log_names(self):
        fnl = self.u.get_file_list(self.pkl_dir)
        return fnl

    def get_rse_csv_names(self):
        rse = self.u.get_file_list(self.rse_csv_output_dir)
        return rse

    def get_bler_report_csv_names(self):
        flist = self.u.get_file_list(self.bler_report_csv_dir)
        return flist

    def load_pickle_file(self, fp):
        f_pkl = open(fp, 'rb')
        msg_list = pickle.load(f_pkl)
        print(INFO, 'Length of messages:', len(msg_list))
        return msg_list

    def msg_list_stats(self, fp):
        msg_list = self.load_pickle_file(fp)
        msg_type_list = [m[3] for m in msg_list]
        from collections import Counter
        msg_type_cnt = Counter(msg_type_list)
        for t in msg_type_cnt:
            print(t, msg_type_cnt[t])

    def process_ecl_log(self, md):
        if len(md) != 6:
            print(DBG, md, len(md))
            return []

        row_buf = []
        row_buf.append('ECL')
        row_buf.append(md['current_ecl'])
        select_reason = md['ecl_selected_by']
        sr = ''
        if select_reason == '2(LL1_RACH_ECL_SELECTED_BY_MEASUREMENT)':
            sr = 'm'
        elif select_reason == '3(LL1_RACH_ECL_SELECTED_NEXT_COVERAGE_LEVEL)':
            sr = 'n'
        elif select_reason == '0(LL1_RACH_ECL_SELECTED_BY_MANUAL_OVERRIDE)':
            sr = 'o'
        elif select_reason == '1(LL1_RACH_ECL_SELECTED_BY_PDCCH_ORDER)':
            sr = 'p'
        else:
            sr = 'err'
            print(ERR, 'Unknown ECL selection reason.', md)

        if sr in {'m', 'n', 'o', 'p'}:
            row_buf.append(sr)
            row_buf.append(int(md['rsrp'])/10)
        else:
            row_buf = []
        return row_buf

    def process_nrs_measurement_log(self, md):
        if len(md) != 8:
            return []
        row_buf = []

        row_buf.append('MEA')
        rsrp = int(md['rsrp'])/10
        if -150 < rsrp < 0:
            row_buf.append(rsrp)
        snr = int(md['snr'])/10
        if -20 < snr < 40:
            row_buf.append(snr)
        return row_buf

    def extract_rsrp_snr_ecl(self, fp):
        print(INFO, 'Extract RSRP, SNR, and ECL.')
        msg_list = self.load_pickle_file(fp)
        rse_list = []  # rsrp, snr, ecl

        ecl_count = [0, 0]
        meas_count = [0, 0]

        for m in msg_list:
            row_buf = m[0:2]
            md = m[7]
            if m[3] == 'LL1_LOG_ECL_INFO':
                ecl_buf = self.process_ecl_log(md)
                if ecl_buf != []:
                    row_buf += ecl_buf
                    ecl_count[0] += 1
                ecl_count[1] += 1
            elif m[3] == 'LL1_NRS_MEASUREMENT_LOG':
                meas_buf = self.process_nrs_measurement_log(md)
                if len(meas_buf) == 3:
                    row_buf += meas_buf
                    meas_count[0] += 1
                meas_count[1] += 1

            # Processed one msg
            if len(row_buf) > 2:
                rse_list.append(row_buf)

        file_name = self.generate_rse_file_name(fp)
        with open(self.rse_csv_output_dir+file_name, 'w', newline='') as f_rse_csv:
            cw = csv.writer(f_rse_csv)
            for l in rse_list:
                cw.writerow(l)
            print(INFO, 'RSRP, SNR, ECL are written into {0}'.format(self.rse_csv_output_dir+file_name))
        print(INFO, 'Number of ECL: {0}, MEASUREMENT: {1}, total: {2}'.format(ecl_count, meas_count, len(rse_list)))

    def take_out_specific_logs_from_msg_list(self, msg_list, log_name, out_folder):
        '''
        Note1: the message list is from .pkl file loading.
        Note2: this method only outputs the seq_num, time ticks, msg name. If you want to extract specific information from specific logs, write another function to do so.
        '''
        print(DBG, msg_list[:10])
        with open(self.output_dir+'{0}/{1}.csv'.format(out_folder, log_name), 'w') as f_csv:
            writer = csv.writer(f_csv)
            for msg in msg_list:
                if msg[3] == log_name:
                    writer.writerow(msg[0:4])
            f_csv.flush()

    def rse_to_df(self, rse_list):

        # Note: ticks should be flatten before dividing the dictionary
        tt_list = [float(m[1])/self.tts_ratio for m in rse_list]
        flatten_tt_list = self.flatten_time_tick_list(tt_list)
        for i in range(len(tt_list)):
            rse_list[i][1] = flatten_tt_list[i]

        meas_list = [m for m in rse_list if m[2] == 'MEA']

        # Create df for measurement records
        df_meas = pd.DataFrame(meas_list, columns=['seq', 'time_ticks', 'type', 'rsrp', 'snr'])
        # print(INFO, df_meas.columns)
        # print(df_meas.head(5))

        ecl_list = [m for m in rse_list if m[2] == 'ECL']
        df_ecl = pd.DataFrame(ecl_list, columns = ['seq', 'time_ticks', 'type', 'ecl', 'ecl_selection_reason', 'rsrp'])
        # print(INFO, df_ecl.columns)
        # print(DBG, df_ecl.head(5))

        return df_meas, df_ecl

    def visualize_time_ticks(self, fp):
        msg_list = self.load_pickle_file(fp)
        time_ticks_list = [m[1]/1000000 for m in msg_list]
        time_ticks_list = self.flatten_time_tick_list(time_ticks_list)

        fig_name = fp.split('/')[-1].split('.')[0]
        fig_name = 'flatten_{0}.png'.format(fig_name[8:])  # remove 'decoded_'
        self.v.plot_time_ticks(time_ticks_list, fig_name)

    def flatten_time_tick_list(self, tt_list):
        if type(tt_list[1]) == float:
            epsilon = 0.0001
        else:
            epsilon = 1000
        ret_list = [tt_list[0]]
        for i in range(1, len(tt_list)):
            delta = tt_list[i] - tt_list[i-1]
            if delta > 0:
                ret_list.append(ret_list[-1] + delta)
            else:
                ret_list.append(ret_list[-1] + epsilon)
        print(INFO, 'Start: {0}, end: {1}'.format(ret_list[0], ret_list[-1]))
        return ret_list

    def generate_rse_file_name(self, full_path):
        path_buf = full_path.split('/')
        idx = path_buf.index('decoded_pkl')
        output_file_name = '_'.join(path_buf[idx+1:-1]+[path_buf[-1].split('.')[0]])
        output_file_name = 'rsrp_snr_ecl_' + output_file_name + '.csv'
        # print(DBG, output_file_name)
        return output_file_name

    def generate_measurement_ecl_fig_name(self, full_path):
        path_buf = full_path.split('/')
        idx = path_buf.index('rsrp_snr_ecl_output')
        output_file_name = '_'.join(path_buf[idx+1:-1]+[path_buf[-1].split('.')[0]])
        output_file_name = output_file_name + '.png'
        # print(DBG, output_file_name)
        return output_file_name

    def visualize_measurement_ecl(self, fp):
        # Load the file from csv files, make sure extract_rsrp_snr_ecl() is run.
        # Note: we need two types of records, so pd.read_csv doesn't work here.
        rse_list = self.u.load_csv_to_list(fp)
        df_meas, df_ecl = self.rse_to_df(rse_list)

        # Update the Dataframe
        df_meas['rsrp'] = df_meas['rsrp'].astype(float)
        df_meas['snr'] = df_meas['snr'].astype(float)
        df_ecl['rsrp'] = df_ecl['rsrp'].astype(float)
        df_ecl['ecl'] = df_ecl['ecl'].astype(int)

        fig_name = self.generate_measurement_ecl_fig_name(fp)
        self.v.plot_measurement_ecl_vs_time(df_meas, df_ecl, fig_name)

    def extract_bler_report(self, fp):
        # From .pkl message list to csv.
        msg_list = self.load_pickle_file(fp)
        log_name = 'PROTO_UE_STATS_TPUT_BLER_REPORT'
        bler_msg_list_all = []
        for msg in msg_list:
            if msg[3] == log_name:
                row_buf = []
                # print(DBG, msg)
                msg_dict = msg[7]
                # print(DBG, len(msg_dict), msg_dict)
                if len(msg_dict) == 6:
                    row_buf = msg[0:4] + [msg_dict['rate'], msg_dict['bler'], msg_dict['nack_pdu'],
                                          msg_dict['total_pdu'], msg_dict['newtx_data_len'],
                                          msg_dict['retx_data_len']]
                else:
                    print(ERR, 'Error in the BLER dict.', msg_dict)
                if row_buf and int(msg_dict['newtx_data_len']) < 10000 and int(msg_dict['retx_data_len']) < 10000:
                    # In case of some strange values.
                    bler_msg_list_all.append(row_buf)
        print(INFO, 'Number of BLER logs', len(bler_msg_list_all))
        new_df = pd.DataFrame(bler_msg_list_all, columns=['seq_num', 'time_ticks', 'message_id',
                                                          'message_name', 'rate', 'bler',
                                                          'nack_pdu', 'total_pdu', 'newtx_data_len',
                                                          'retx_data_len'])
        f_name = 'bler_' + fp.split('/')[-1].split('.')[0] + '.csv'
        print(f_name)
        new_df.to_csv(self.output_dir+'bler_csv/'+f_name)

    def visualize_bler_report_vs_time(self, fp):
        bler_df = pd.read_csv(fp)
        # Flatten time list
        t_list = [float(x)/self.tts_ratio for x in bler_df['time_ticks'].to_list()]
        bler_df['time_ticks'] = self.flatten_time_tick_list(t_list)

        self.v.plot_bler_report_vs_time(bler_df)

    def pipeline_bler_log(self, file_list):
        # classify bler according to app types
        df = pd.DataFrame(columns=['operator', 'app', 'bler'])
        df_all = pd.DataFrame(columns=['operator', 'app', 'bler'])
        for fl in file_list:
            fl_split = fl.split('_')
            operator, app_type = fl_split[0], fl_split[1]
            df = pd.read_csv(fl)
            df['operator'] = operator
            df['app_type'] = app_type

    def visualize_bler_vs_app(self, fp):
        bler_df = pd.read_csv(fp)
        self.v.plot_bler_vs_app()

    def extract_msg3_repetition(self, fp):
        # from : RAR_UL_GRANT
        print(INFO, 'Extract msg3 repetition.')
        msg_list = self.load_pickle_file(fp)
        log_name = 'LL1_RAR_UL_GRANT'
        row_buf_list = []
        for msg in msg_list:
            if msg[3] == log_name:
                row_buf = []
                # print(DBG, msg)
                msg_dict = msg[7]
                print(len(msg_dict))
                # print(DBG, len(msg_dict), msg_dict)
                if len(msg_dict) == 3:
                    row_buf = [msg[3], msg_dict['rar_pdu']['modulation_coding_scheme_tbs'],
                                      msg_dict['rar_pdu']['repetition_number'],
                                      msg_dict['rar_pdu']['modulation_coding_scheme_imcs'],
                                      msg_dict['rar_pdu']['modulation_coding_scheme_itbs'],
                                      msg_dict['rar_pdu']['resource_unit_number']]
                else:
                    print(ERR, 'Error in the BLER dict.', msg_dict)
                # if row_buf and int(msg_dict['newtx_data_len']) < 10000 and int(msg_dict['retx_data_len']) < 10000:
                #     # In case of some strange values.
                row_buf_list.append(row_buf)
        print(INFO, 'Number of RAR logs', len(row_buf_list))
        new_df = pd.DataFrame(row_buf_list, columns=['message_name', 'modulation_coding_scheme_tbs', 'repetition_number',
                                                     'modulation_coding_scheme_imcs', 'modulation_coding_scheme_itbs',
                                                     'resource_unit_number'])
        f_name = 'rar_' + fp.split('/')[-1].split('.')[0] + '.csv'
        print(f_name)
        new_df.to_csv(self.output_dir + 'rar_csv/' + f_name, index=False)

    def extract_dci(self, fp):
        print(INFO, 'extract DCI info.')
        msg_list = self.load_pickle_file(fp)
        msg_name = ['LL1_DCI_FORMAT_N0', 'LL1_DCI_FORMAT_N1_NORMAL']
        row_buf_list = []
        for m in msg_list:
            if m[3] in msg_name:
                if m[3] == msg_name[0]:
                    dci = m[7]['dci_n0']
                    print(dci)
                    row_buf = [m[3], dci['repetition_number'], dci['dci_sf_repetition_number'],
                              dci['modulation_coding_scheme_tbs'], dci['resource_assignment_nru']]
                else:
                    dci = m[7]['dci_n1']
                    print(dci)
                    row_buf = [m[3], dci['repetition_number'], dci['dci_sf_repetition_number'],
                              dci['modulation_coding_scheme_tbs'], None]

                # if row_buf and int(dci['newtx_data_len']) < 10000 and int(dci['retx_data_len']) < 10000:
                    # In case of some strange values.
                row_buf_list.append(row_buf)
        print(INFO, 'Number of DCI logs', len(row_buf_list))
        new_df = pd.DataFrame(row_buf_list, columns=['msg_name', 'repetition_number', 'dci_sf_repetition_number',
                                                     'modulation_coding_scheme_tbs', 'resource_assignment_nru'
                                                     ])
        f_name = 'dci_' + fp.split('/')[-1].split('.')[0] + '.csv'
        print(f_name)
        new_df.to_csv(self.output_dir + 'dci_csv/' + f_name, index=False)

    def pipeline_process_all(self, file_list):
        file_count = 0
        for fl in file_list[:]:
            file_count += 1
            print('\n')
            print(INFO, 'Processed file count: {0}, file_name: {1}'.format(file_count, fl.split('/')[-1]))

            # self.extract_rsrp_snr_ecl(self.pkl_dir+fl)
            # self.visualize_time_ticks(self.pkl_dir+fl)
            # self.visualize_measurement_ecl(self.rse_csv_output_dir+fl)

            # self.extract_bler_report(self.pkl_dir+fl)
            # self.visualize_bler_report_vs_time(self.output_dir+'bler_csv/'+fl)

            self.extract_msg3_repetition(self.pkl_dir + fl)
            # self.extract_dci(self.pkl_dir + fl)

    def aggregate_extracted_info_to_csv(self, flag, csv_dir):
        # aggregate the extracted info into one summary file
        # flags: rar, dci, nrs, ecl

        df_all = pd.DataFrame()
        df_result = pd.DataFrame()

        file_list = self.u.get_file_list(csv_dir)
        if flag == 'ecl':
            for fl in file_list:
                rse_list = self.u.load_csv_to_list(csv_dir + fl)
                df_meas, df = self.rse_to_df(rse_list)
                fs = fl.split('.')[0].split('_')
                loc_index = fs.index('D')
                df['node_id'], df['test_id'], df['pack_id'] = fs[loc_index - 1], fs[loc_index + 1], fs[loc_index + 2]
                df_all = df_all.append(df)
            df_result = self.aggregate_ecl_dci_rar_info(df_all, 'ecl', flag)

        elif flag == 'nrs':
            for fl in file_list:
                print(fl)
                rse_list = self.u.load_csv_to_list(csv_dir + fl)
                df, df_ecl = self.rse_to_df(rse_list)
                fs = fl.split('.')[0].split('_')
                loc_index = fs.index('D')
                df = df[df.rsrp != '-']
                df['rsrp'] = df['rsrp'].astype('float')
                df['snr'] = df['snr'].astype('float')
                df_line = self.get_nrs_stats(df, fs[loc_index - 1], fs[loc_index + 1], fs[loc_index + 2])
                df_result = df_result.append(df_line, ignore_index=True)

        elif flag == 'rar':
            count = 0
            for fl in file_list:
                df = pd.read_csv(csv_dir + fl)
                if len(df) == 0:
                    count += 1
                    print(fl)
                fs = fl.split('.')[0].split('_')
                loc_index = fs.index('D')
                df['node_id'], df['test_id'], df['pack_id'] = fs[loc_index - 1], fs[loc_index + 1], fs[loc_index + 2]
                df_all = df_all.append(df)
            df_result = self.aggregate_ecl_dci_rar_info(df_all, 'repetition_number', flag)
            print(len(df_result), count)
        elif flag == 'dci':
            for fl in file_list:
                df = pd.read_csv(csv_dir + fl)
                fs = fl.split('.')[0].split('_')
                loc_index = fs.index('D')
                df['node_id'], df['test_id'], df['pack_id'] = fs[loc_index - 1], fs[loc_index + 1], fs[loc_index + 2]
                df_all = df_all.append(df[(df['msg_name'] == 'LL1_DCI_FORMAT_N0')])
            df_result = self.aggregate_ecl_dci_rar_info(df_all, 'repetition_number', flag)

        df_result.to_csv(self.merge_dir + flag + '_summary.csv', index=False)

    def drop_outlier(self, df, column):
        upper_limit = {'rsrp': -60, 'snr': 20}
        lower_limit = {'rsrp': -140, 'snr': -20}
        df_2 = df[(df[column] <= upper_limit[column]) & (df[column] >= lower_limit[column])]
        if len(df) != len(df_2):
            drop_lines = len(df)-len(df_2)
            print('DBG:', column, drop_lines)
            # print('DBG: drop outlier:', df.node_id.iloc[0], df.test_id.iloc[0], df.pack_id.iloc[0])
        return df_2

    def get_nrs_stats(self, df, node_id, test_id, pack_id):
        df_1 = self.drop_outlier(df, 'rsrp')
        df_2 = self.drop_outlier(df_1, 'snr')

        rsrp_mean = df_2['rsrp'].mean() * 10
        rsrp_min = min(df_2['rsrp']) * 10
        rsrp_max = max(df_2.rsrp) * 10
        rsrp_std = df_2.rsrp.std() * 10
        snr_mean = df_2['snr'].mean() * 10
        snr_min = min(df_2.snr) * 10
        snr_max = max(df_2.snr) * 10
        snr_std = df_2.snr.std() * 10

        dict = {
            'node_id': node_id,
            'test_id': test_id,
            'pack_id': pack_id,
            'rsrp_min': rsrp_min,
            'rsrp_max': rsrp_max,
            'rsrp_mean': rsrp_mean,
            'rsrp_std': rsrp_std,
            'snr_min': snr_min,
            'snr_max': snr_max,
            'snr_mean': snr_mean,
            'snr_std': snr_std
                }
        print('INFO:', dict)
        df_result = pd.DataFrame(dict, index=[0])
        # df_result = df_result.append(dict, ignore_index=True)
        # df_result.to_csv(self.merge_dir + 'nrs_summary_2.csv', index=False)
        return df_result

    def aggregate_ecl_dci_rar_info(self, df_all, column, flag):
        df_result = pd.DataFrame(columns=['node_id', 'test_id', 'pack_id', column])
        for (node_id, test_id, pack_id), df in df_all.groupby(['node_id', 'test_id', 'pack_id']):
            value = list(df[column])
            dict = {'node_id': node_id,
                    'test_id': test_id,
                    'pack_id': pack_id,
                    column: value}
            # print('INFO:', dict)
            df_result = df_result.append(dict, ignore_index=True)
        return df_result

    def merge_msg3_data_rep_with_meta(self):
        df_meta = pd.read_csv(self.meta_data)
        df_msg3 = pd.read_csv(self.merge_dir + 'rar_summary.csv', low_memory=False)
        df_data = pd.read_csv(self.merge_dir + 'dci_summary.csv', low_memory=False)
        df_msg3 = df_msg3.rename(columns={'repetition_number': 'msg3_rep'})
        df_data = df_data.rename(columns={'repetition_number': 'data_rep'})
        df = pd.merge(df_msg3, df_data, how='inner', on=['node_id', 'test_id', 'pack_id'])

        df = pd.merge(df, df_meta, how='outer', on=['node_id', 'test_id'])
        df.to_csv(self.pftp_data_dir + 'msg3_data_rep.csv', index=False)


