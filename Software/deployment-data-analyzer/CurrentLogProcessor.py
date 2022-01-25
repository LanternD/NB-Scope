import csv
import multiprocessing
import os
import shutil
import time
from pathlib import Path

import numpy as np
import pandas as pd

from DataVisualizer import DataVisualizer
from Utils import *


class CurrentLogProcessor(object):
    def __init__(self, whoami, region):
        # Helper
        self.u = Utils()
        self.v = DataVisualizer(whoami)
        print(INFO, self.u.log_in, self.u.hostname, self.u.os)
        self.config = self.u.load_config("./config.json")
        self.region = region
        self.whoami = whoami

        # Nutstore folder
        self.global_path = self.config["env_prefix"][whoami][self.u.os]
        print(INFO, 'Global prefix', self.global_path)

        # Assign current raw .log dirs
        self.raw_log_dir = self.global_path + self.config['i_raw_folder_by_host'][self.region]
        # self.raw_log_dir_us = self.global_path + self.config["data_path_prefix_us"] + 'Current/'
        # self.raw_log_dir_amarisoft = self.global_path + self.config['data_path_prefix_amarisoft']

        self.output_dir = self.global_path + self.config["output_path"]

        # Store the intermediate process output files: csv/figure/stats of each packet or test.
        self.mid_out_dir = self.config["middle_file_dir_by_host"][self.u.hostname]

        '''
        Add your path in config.json: csv_folder_by_host, csv_subfolder_by_region
        Choose a place other than Nutstore
        '''
        self.current_csv_dir = self.config['csv_folder_by_host'][self.u.hostname] + self.config['csv_subfolder_by_region'][self.region]
        self.region_suffix = self.region
        if self.region in {'cndy', 'sz'}:
            self.region_suffix = 'cn'

        # Region checking
        if self.region not in {'cn', 'cndy', 'us', 'sz', 'opt'}:
            print(ERR, 'Unkown region assignment')

        print(INFO, 'CSV output dir: {0}'.format(self.current_csv_dir))

        self.format = "B"  # fixed

        # Load dictionary
        self.node_id_to_module_dict = self.config['node_id_to_module_dict']
        self.module_to_i_tx_threshold_dict = self.config['module_to_i_tx_th_dict']
        self.module_to_i_idle_threshold_dict = self.config['module_to_i_idle_th_dict']
        self.module_vcc = self.config['module_vcc']

# Supporting Funtions BEGIN ###############################################
    def generate_current_raw_log_name_list_2(self, datadir, allowed_node, allowed_test_id):
        current_raw_log_name_list = []
        # for p in self.raw_log_dir:
        # print(DBG, self.data_dir+p)
        f_candidate = self.u.get_file_list(self.raw_log_dir + datadir)
        for x in f_candidate:
            node_id, log_type, test_id = x.split("_")[0:3]
            if len(allowed_test_id) != 0 and len(allowed_node) != 0:
                if (
                    node_id in allowed_node
                    and log_type == "I"
                    and test_id in allowed_test_id
                ):
                    current_raw_log_name_list.append(x.split(".")[0])
            else:
                if node_id in allowed_node and log_type == 'I':
                    current_raw_log_name_list.append(x.split('.')[0])
        # print(INFO, current_raw_log_name_list)
        # print(INFO, 'Number of current log files:', len(current_raw_log_name_list))
        return current_raw_log_name_list

    def generate_current_raw_log_name_list(self):
        current_raw_log_name_list = []
        # for p in self.raw_log_dir:
        # print(DBG, self.data_dir+p)
        f_candidate = self.u.get_file_list(self.raw_log_dir)

        for x in f_candidate:
            # node_id, log_type, test_id = x.split("_")[0:3]
            if x.split('_')[1] == 'I':
                current_raw_log_name_list.append(x.split(".")[0])

        print(INFO, current_raw_log_name_list)
        print(INFO, 'Number of current log files:', len(current_raw_log_name_list))
        return current_raw_log_name_list

    def get_all_current_log_filename_list(self, file_path, f_extension):
        # This one only gets the current log.
        print(INFO, file_path)
        current_log_list = []
        for root, dirs, files in os.walk(file_path):
            for file in files:
                if file.endswith(f_extension) and '_I_' in file:
                    current_log_list.append(os.path.join(root, file))
                    # print(os.path.join(root, file))
        return current_log_list

    def current_raw_to_df(self, filename):
        if self.region in {'us', 'cndy', 'sz', 'opt'}:
            fp = filename  # absolute path
        else:
            fp = self.raw_log_dir + filename + ".log"

        with open(fp, 'rb') as f_r:
            time_list = []
            current_list = []
            if self.format == "A":
                data = f_r.read(2)
                while data:
                    current = int.from_bytes(data, byteorder="little", signed=True) * 0.018311
                    current_list.append(current)
                    data = f_r.read(2)

                count_samples = len(current_list)
                stop_time = count_samples  # time unit: ms
                time_list = np.linspace(0, stop_time, count_samples)
            elif self.format == "B":
                last_ts = 0
                current_group = []
                offset = 0

                data = f_r.read(4)
                while data:
                    # two byte for timestamp, unit='ms'
                    ts = int.from_bytes(data[0:2], byteorder="little", signed=False)
                    # two byte for current
                    current = int.from_bytes(data[2:], byteorder="little", signed=True) * 0.018311

                    if ts != last_ts:
                        if ts < last_ts:
                            offset += 1
                            last_ts = 0

                        # end last group
                        new_ts_list = np.linspace(
                            last_ts + offset * 65536,
                            ts + offset * 65536,
                            len(current_group),
                            endpoint=False,
                        ).tolist()
                        time_list += new_ts_list
                        current_list += current_group

                        # start new group
                        last_ts = ts
                        current_group = []
                    current_group.append(current)
                    data = f_r.read(4)
                # last group
                try:
                    new_ts_list = np.linspace(ts + offset * 65536, ts + 1 + offset * 65536, len(current_group), endpoint=False).tolist()
                except UnboundLocalError:
                    print(ERR, 'TS list unbounded.', filename)
                    return None

                time_list += new_ts_list
                current_list += current_group

            elif self.format == "C":
                head = f_r.read(16)
                print(head)
                t_start = int.from_bytes(head[2:4], byteorder="little", signed=False)
                t_end = int.from_bytes(head[4:6], byteorder="little", signed=False)

                if t_start >= t_end:
                    t_end += 65536
                current_list = []
                current = f_r.read(2)
                print(current)
                while current:
                    current_list.append(int.from_bytes(current, byteorder="little", signed=True) * 0.018311)
                    current = f_r.read(2)
                time_list = np.linspace(t_start, t_end, len(current_list), endpoint=True).tolist()
                # print(time_list)
                print(t_start, t_end, len(current_list))

            # Convert to dataframe
            df = pd.DataFrame(
                {"time": time_list, "current": current_list},
                columns=["time", "current"],
            )
            fn = self.u.get_filename_from_path(filename)
            df.node_id, df.test_id, df.packet_id = self.u.get_info_from_filename(fn)  # Important: for future processing.

            # The nodes in SZ area are not calibrated before testing. Manually calibrate.
            if 'D' in df.node_id and self.region == 'sz':
                origin_cali_reg = 2757
                calibrated_reg = self.config['d_series_node_i_calibration'][df.node_id]

                # Add bias to SZ ME3616 nodes (problems in their zeros), applied to examples before 2020.03.23
                if df.node_id == 'D05':
                    df['current'] = df['current'] - 6.6  # other me3616 has 10.7 bias
                # elif df.node_id == 'D06':
                #     df['current'] = df['current'] - 10.7
                # elif df.node_id == 'D11':
                #     df['current'] = df['current'] - 10.7
                # elif df.node_id == 'D12':
                #     df['current'] = df['current'] - 10.7

                df['current'] = df['current'] * calibrated_reg / origin_cali_reg
            # print(INFO, df.node_id)
            return df

    def dump_current_df_to_csv(self, df, filename):
        # Note: if you want to change the output dir, update the config.json file.
        fpath = filename.split('/')[:-1]
        dir_path = '/'.join(fpath)
        Path(self.current_csv_dir+dir_path).mkdir(parents=True, exist_ok=True)

        time_offset = min(df["time"])
        df["time"] = df["time"] - time_offset
        # Note: the time unit is ms, need to /1000 in plotting.

        df['current'] = df['current'].map('{:,.6f}'.format)  # keep 6 tens digits

        df.to_csv(self.current_csv_dir + filename + ".csv", sep=",", index=None)

    def load_current_data_from_csv(self, ph):
        '''
        Note: it takes two types of argument,
        (1) File name only: 'A01_I_01201_0001' (without the extension)
        (2) Absolute path: '/Users/dlyang/Nutstore Files/NutstoreX/Field Test/STM32 Node Deployment - US/Current/A01/01201/A01_I_01201_0001.csv'
        Use '/' to determine
        '''
        if '/' in ph:
            df = pd.read_csv(ph, delimiter=",", header=0, index_col=None, engine="python")
        else:
            df = pd.read_csv(ph + ".csv", delimiter=",", header=0, index_col=None, engine="python")
        filename = self.u.get_filename_from_path(ph)
        df.node_id, df.test_id, df.packet_id = self.u.get_info_from_filename(filename)  # Important: for future processing.
        df.filename = filename

        return df
# Supporting Functions END ################################################

# Pipeline Marker
# Pipeline: LOG to CSV BEGIN ##############################################
    def pipeline_from_raw_to_csv(self, enable_multiprocessing=True):
        if self.region in {'us', 'cndy', 'sz', 'opt'}:
            log_fp_list = self.get_all_current_log_filename_list(self.raw_log_dir, f_extension='log')
            log_fp_list = [x for x in log_fp_list if '_I_' in x]
        elif self.region == 'amarisoft':
            '''Note: need to specify the sub dir in this case.'''
            log_fp_list = self.get_all_current_log_filename_list(self.raw_log_dir + 'Inactivetimer/', f_extension='log')
            log_fp_list = [x for x in log_fp_list if '_I_' in x]
        else:
            # For region == 'cn'
            log_fp_list = self.generate_current_raw_log_name_list()
        log_fp_list.sort()
        print(INFO, 'Total # of logs:', len(log_fp_list))

        file_count = 0

        # Run a subset
        # Random subset
        # import random
        # random.seed(123)
        # log_fp_list = random.sample(log_fp_list, int(len(log_fp_list)*0.1))

        # Specific model
        # log_fp_list = [x for x in log_fp_list if ('07601' in x)]
        log_fp_list = [x for x in log_fp_list if ('D05' in x)]
        # log_fp_list = [x for x in log_fp_list if ('C04' in x) or ('C02' in x) or ('C10' in x) or ('C11' in x)]

        # Select by test date
        # log_fp_list = [x for x in log_fp_list if int(x.split('_')[-2]) > 8000]

        # Load specific absolute path file
        # log_fp_list = self.u.load_path_or_names_to_list('/home/dlyang-zmly/Desktop/fn_temp.txt')

        # Subsampling for development
        # log_fp_list = log_fp_list[:2]

        print(INFO, '# of logs this round:', len(log_fp_list))
        print(INFO, "Examples:", log_fp_list[:3])

        # return  # SAFTY, uncomment this to run.

        cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cores)

        if enable_multiprocessing:
            # Parallel computing
            print(INFO, 'Using multiprocessing.')
            file_count += sum(pool.map(self.subpipeline_current_raw_to_csv, log_fp_list))
            print(INFO, "Processed files:", file_count)
        else:
            # Serial computing
            for filename in log_fp_list:
                file_count += 1
                self.subpipeline_current_raw_to_csv(filename)
                if file_count % 100 == 0:
                    print(INFO, "Processed files:", file_count)

    def subpipeline_current_raw_to_csv(self, filename):
        df = self.current_raw_to_df(filename)
        if self.region in {'us', 'cndy', 'opt', 'sz'}:
            filename = self.u.get_csv_output_dir_from_path(filename)
        self.dump_current_df_to_csv(df, filename)
        return 1  # for counting

# Pipeline: LOG to CSV END ################################################

# Pipeline: CSV to PNG BEGIN ##############################################
    def calculate_energy_one_df(self, df, new_tx_th=None, new_idle_th=None):
        '''
        Use composite trapezoidal rule to calculate the integal.
        Return: stats_dict, storing the statistics
        '''
        node_id = df.node_id
        module = self.node_id_to_module_dict[node_id]
        tx_th = self.module_to_i_tx_threshold_dict[module]
        idle_th = self.module_to_i_idle_threshold_dict[module]
        stats_dict = {'point': len(df['current']),
                      'i_max': max(df['current']),
                      'i_min': min(df['current']),
                      'i_tx_threshold': tx_th,
                      'tx_energy': 0,
                      'active_energy': 0,
                      'till_last_tx_energy': 0,
                      'tx_intervals': [],
                      'last_tx_idx': 0
                      }

        # Deal with low current issue when in ECL0 good signal quality
        # Note: update config.json if needed.
        module = self.node_id_to_module_dict[df.node_id]
        if module in {'BC66', 'BC26', 'BC28'}:
            if stats_dict['i_max'] < self.config["ecl0_i_tx_th_override_i_max_condition"][module]:
                stats_dict['i_tx_threshold'] = self.config['overriden_i_tx_th'][module]  # chosen empirically

        # Override the default value.
        if new_tx_th is not None:
            stats_dict['i_tx_threshold'] = new_tx_th  # chosen empirically

        if new_idle_th is not None:
            idle_th = new_idle_th

        # print(DBG, stats_dict['i_tx_threshold'], idle_th)

        # Change time scale
        df['time'] = df['time'] / 1000  # ms to s
        # print(df.describe())

        stats_dict['tx_energy'], stats_dict['tx_intervals'] = self.calculate_tx_energy(df, stats_dict['i_tx_threshold'])  # unit: mJ
        try:
            last_tx_ts_idx = stats_dict['tx_intervals'][-1][1]
        except IndexError:
            # This happens when all the current are below threshold
            print(ERR, 'Error processing file:', df.filename)
            last_tx_ts_idx = 0

        if self.node_id_to_module_dict[df.node_id] == 'SARA':
            last_tx_ts_idx = self.find_sara_last_tx_idx(df, last_tx_ts_idx)

        stats_dict['active_energy'] = self.calculate_active_energy(df, idle_th)
        stats_dict['last_tx_idx'] = last_tx_ts_idx
        stats_dict['till_last_tx_energy'] = self.calculate_energy_till_last_tx(df, last_tx_ts_idx)

        return stats_dict

    def calculate_tx_energy(self, df, bar):
        i_tx_df = df[df['current'] > bar]
        # print(i_tx_df.describe())

        idx_list = list(i_tx_df.index)
        # print(DBG, idx_list)
        interval_list = self.u.find_consecutive_range(idx_list)
        # print(DBG, interval_list)
        tx_energy_sum = 0

        for p in interval_list:
            df_tx = df[p[0]:p[1]].copy()
            it_mul = np.trapz(df_tx['current'], df_tx['time'])  # sum(I*t), mA to A
            tx_energy_sum += it_mul * self.module_vcc  # U*sum(I*t)
        return tx_energy_sum, interval_list

    def calculate_active_energy(self, df, idle_mean_bar):
        active_energy_sum = 0
        n_win = (len(df) - len(df) % 100) // 100  # ignore tailing points
        for i in range(n_win):
            sub_df = df[100*i:100*i+100].copy()
            if sub_df['current'].mean() > idle_mean_bar:
                e_win = np.trapz(sub_df['current'], sub_df['time'])
                active_energy_sum += e_win * self.module_vcc
        return active_energy_sum

    def calculate_energy_till_last_tx(self, df, t_end_idx):
        range_energy_sum = 0
        sub_df = df[:t_end_idx].copy()
        range_energy_sum = np.trapz(sub_df['current'], sub_df['time']) * self.module_vcc
        return range_energy_sum

    def find_sara_last_tx_idx(self, df, last_tx_ts_from_energy_calc):
        '''
        SARA module has too many spikes, change a function for a better accuracy
        The bars are taken empirically.
        '''
        if last_tx_ts_from_energy_calc == 0:
            return 0
        sara_i_idle_df = df[df['current'] < 12].copy()
        idle_idx_list = list(sara_i_idle_df.index)
        i = 0
        while i < len(idle_idx_list):
            # Move forward a little bit
            if idle_idx_list[i] > last_tx_ts_from_energy_calc:
                last_tx_ts_idx = idle_idx_list[i]
                break
            i += 1
        if i == len(idle_idx_list):
            return last_tx_ts_from_energy_calc
        else:
            return last_tx_ts_idx

    def export_stats_dict(self, stats_dict, fn, output_path):
        one_row = []
        node_id, test_id, packet_id = self.u.get_info_from_filename(fn)
        one_row = [node_id, test_id, packet_id]
        one_row += [stats_dict['i_max'], stats_dict['i_min'],
                    stats_dict['tx_energy'], stats_dict['active_energy'],
                    stats_dict['till_last_tx_energy']]
        with open(output_path, 'a') as f_csv:
            cw = csv.writer(f_csv)
            cw.writerow(one_row)
            f_csv.close()

    # Pipeline Marker
    def pipeline_df_to_current_plot_dy(self, enable_multiprocessing=True):
        if self.region in {'us', 'cndy', 'opt', 'sz'}:
            log_fp_list = self.get_all_current_log_filename_list(self.current_csv_dir, f_extension='csv')
        else:
            log_fp_list = self.generate_current_raw_log_name_list()
        print(INFO, '# of found logs:', len(log_fp_list))
        log_fp_list.sort()

        # Process some device only:
        log_fp_list = [x for x in log_fp_list if ('D05' in x)]
        # log_fp_list = [x for x in log_fp_list if int(x.split('_')[-2]) > 8000]
        # log_fp_list = [x for x in log_fp_list if ('D14' in x) or ('D06' in x) or ('D11' in x) or ('D12' in x)]
        # log_fp_list = [x for x in log_fp_list if ('D11' in x)]
        # log_fp_list = [x for x in log_fp_list if '07601' in x]
        # log_fp_list = [x for x in log_fp_list if '07601' in x]

        # Truncate the range:
        # log_fp_list = log_fp_list[:10]

        # Load specific absolute path file:
        # log_fp_list = self.u.load_path_or_names_to_list('/home/dlyang/Desktop/fn_log_temp.txt')

        print(INFO, 'Examples:', log_fp_list[:3])
        print(INFO, 'Number of logs this round: {0}'.format(len(log_fp_list)))

        # return  # SAFTY, uncomment this to run.

        cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cores)

        file_count = 0
        if enable_multiprocessing:
            # Parallel computing
            print(INFO, 'Using multiprocessing.')
            file_count += sum(pool.map(self.subpipeline_df_to_current_plot, log_fp_list))
            print(INFO, "Processed files:", file_count)
        else:
            # Serial computing
            print(INFO, 'Using serial proceesing.')
            for filename in log_fp_list:
                file_count += 1
                self.subpipeline_df_to_current_plot(filename)
                if file_count % 100 == 0:
                    print(INFO, "Processed files:", file_count)
            print(INFO, "Total processed files:", file_count)

    def subpipeline_df_to_current_plot(self, fp):
        '''
        Subpipeline: Processing one file
        fp: file path, absolute
        '''
        df = self.load_current_data_from_csv(fp)
        if df.node_id == 'D05':
            df['current'] = df['current'] * 360 / 600

        df['current'] = df['current'] - 9.70
        # df['current'] = df['current'] - 6.6  # extra bias
        stats_dict = self.calculate_energy_one_df(df, 120)  # can add tx_th here.

        fn = self.u.get_filename_from_path(fp)
        is_amarisoft = False
        if self.region == 'opt':
            is_amarisoft = True
        self.export_stats_dict(stats_dict, fn, self.output_dir + 'packet_energy_stats_{0}_{1}.csv'.format(self.region_suffix, fn[:3]))

        local_vis = DataVisualizer(self.whoami)
        local_vis.plot_current(df,
                               fn,
                               show_flag=False,
                               stats_dict=stats_dict,
                               is_amarisoft=is_amarisoft)
        return 1  # for counting

# Pipeline: CSV to PNG END ################################################

    def get_time_stamp_send_packet(self, filename):
        print("current processing:", filename)
        ue_type = filename.split("_")[0]
        df = self.load_current_data_from_csv(self.current_csv_dir + filename)
        window_len = 1024 * 4
        beg = 0
        flag = 0
        # current_threshold = 70
        current_threshold = {
            "C01": 30,
            "C02": 30,
            "C03": 30,
            "C04": 30,
            "C05": 70,
            "C06": 70,
            "C07": 70,
            "C08": 70,
            "C09": 30,
            "C10": 30,
            "C11": 30,
            "C12": 30,
        }
        while beg < len(df) - window_len:
            window = df.loc[beg : beg + window_len].copy()
            # print('DEBUG:', window)
            # print("current processing:", window.loc[beg].time, window.loc[beg + window_len].time)
            max_current = np.max(window["current"])
            if not flag:
                if max_current > current_threshold[ue_type]:
                    index = window.loc[window["current"] == max_current].index
                    print("start:\n", window.loc[index[0]]["time"])
                    flag = 1
            else:
                if max_current < current_threshold[ue_type]:
                    index = window.loc[window["current"] == max_current].index
                    print("end:\n", window.loc[index[0]]["time"])
                    break
            beg += window_len

    def split_current_period(self, filename):
        print("current processing:", filename)
        ue_type = filename.split("_")[0]
        df = self.load_current_data_from_csv(self.current_csv_dir + filename)
        current_threshold = {
            "C01": 30,
            "C02": 30,
            "C03": 30,
            "C04": 30,
            "C05": 70,
            "C06": 70,
            "C07": 70,
            "C08": 70,
            "C09": 30,
            "C10": 30,
            "C11": 30,
            "C12": 30,
        }
        df["send_period"] = 0
        last_send_index = -1
        for i in range(0, len(df)):
            if df.loc[i]["current"] > current_threshold[ue_type]:
                if last_send_index > 0:
                    # for j in range(last_send_index+1, i+1):
                    #     df.loc[j, 'send_period'] = 1
                    df.loc[last_send_index + 1 : i, "send_period"] = 1

                last_send_index = i
                # print(i)
            else:
                pass
        df.to_csv("D:/test.csv")

    def visualize_current_distribution(self, df):
        print(df.describe())
        self.v.plot_current_distributions(df)
        rx = 40
        tx = 70
        list1 = []
        list2 = []
        list3 = []
        for i in range(0, len(df)):
            if df.loc[i]["current"] < rx:
                list1.append(df.loc[i]["time"])
            elif rx < df.loc[i]["current"] < tx:
                list2.append(df.loc[i]["time"])
            elif df.loc[i]["current"] > tx:
                list3.append(df.loc[i]["time"])

    def smooth_current_df(self, df):
        '''
        Smooth the data for better visualization.
        (Not every well at this point)
        '''
        # for i in range(1, len(df)):
        #     df['current'].iloc[i] = df['current'].iloc[i-1] * 0.6 + df['current'].iloc[i] * 0.4
        df['current'] = df['current'].rolling(window=3).mean()
        return df

    def pipeline_plot(self, datadir, allowed_node, allowed_test_id):
        log_list = self.generate_current_raw_log_name_list_2(
            datadir, allowed_node, allowed_test_id
        )
        log_list = [datadir + '/' + x for x in log_list]
        file_count = 0
        for filename in log_list:
            print(DBG, filename)
            file_count += 1
            df = self.current_raw_to_df(filename)
            self.v.plot_current(df, filename.split('/')[1], show_flag=True)

# Device packet statistics proceesing #####################################

    def load_packet_energy_stats_csv(self, fp):
        col_list = ['node_id', 'test_id', 'packet_index', 'i_max', 'i_min', 'e_tx', 'e_active', 'e_packet']
        df = pd.read_csv(fp, delimiter=",", names=col_list, index_col=False, engine="python")
        node_id = df['node_id'][0]
        df.node_id_str = node_id
        # print(df.node_id_str)
        # print(df)
        return df

    def list_zero_energy_packets_drop_duplicates(self, node_id):
        if node_id[0] == 'A':
            suf = 'us'
        elif node_id[0] == 'C':
            suf = 'cn'
        else:
            suf = 'xx'
        csv_path = self.output_dir + 'packet_energy_stats/packet_energy_stats_{0}_{1}.csv'.format(suf, node_id)
        df = self.load_packet_energy_stats_csv(csv_path)

        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_rows', None)

        df = df.sort_values(by=['test_id', 'packet_index'])
        print("len df:", len(df))
        # print(df.describe())

        # Show zero rows
        # df_zero = df[(df['e_tx'] == 0) | (df['e_packet'] == 0)]
        # print(len(df_zero), df_zero)

        # Show duplicate (test_id, packet_id) combo
        print(INFO, 'First dulicates:')
        df_dup_1 = df[df.duplicated(['test_id', 'packet_index'], keep='first')].copy()
        print(len(df_dup_1))
        print(df_dup_1)

        print(INFO, 'Last dulicates:')
        df_dup = df[df.duplicated(['test_id', 'packet_index'], keep='last')].copy()
        print(len(df_dup))
        print(df_dup)

        # return
        # Drop duplicates
        df.drop_duplicates(subset=['test_id', 'packet_index'], keep='last', inplace=True, ignore_index=True)
        print('Len df after dropping:', len(df))

        # Export to file
        new_name = self.output_dir + 'packet_energy_stats/' + csv_path.split('/')[-1][:-4] + '_m2.csv'
        df.to_csv(new_name, sep=',', index=None, header=None)  # no header to be consistent

    def append_enery_stats_by_node_id(self, nd_list):
        '''Deal with the newly calculated energy stats to the existing ones.
        May do a dropping duplicates afterwards'''

        print(INFO, 'Candidates lists:', nd_list)
        for nd in nd_list:
            src_fp = self.output_dir + 'packet_energy_stats_{0}_{1}.csv'.format(self.region_suffix, nd)
            src_csv_df = self.load_packet_energy_stats_csv(src_fp)
            src_csv_df = src_csv_df.sort_values(by=['test_id', 'packet_index'], axis=0, ignore_index=True)
            dst_fp = self.output_dir + 'packet_energy_stats/packet_energy_stats_{0}_{1}.csv'.format(self.region_suffix, nd)
            dst_csv_df = self.load_packet_energy_stats_csv(dst_fp)
            print(src_fp, dst_fp)
            new_df = pd.concat([dst_csv_df, src_csv_df], axis=0, join='outer', ignore_index=True)
            new_df.to_csv(dst_fp, sep=',', index=None, header=True)

    def aggregate_csv(self, individual_csv_dir, is_energy_stats=False, sort_col_list=None, rename_dict=None):
        '''Merge all the csv in a folder into one.
        Make sure all the info is correct for each device before running this one.'''
        csv_name_list = self.u.get_file_list(individual_csv_dir)
        csv_name_list.sort()
        # print(DBG, csv_name_list)
        print(individual_csv_dir)
        # return

        df_list = []
        len_sum = 0
        for fn in csv_name_list:
            if is_energy_stats:
                df_buf = self.load_packet_energy_stats_csv(individual_csv_dir+fn)
            else:
                df_buf = pd.read_csv(individual_csv_dir+fn, delimiter=",", index_col=False, engine="python")
            len_sum += len(df_buf)
            print(INFO, 'This file:', len(df_buf), '\tTotal:', len_sum)
            df_list.append(df_buf)

        new_df = pd.concat(df_list, axis=0, join='outer', ignore_index=True)
        print(INFO, new_df.columns)
        if sort_col_list is not None:
            new_df = new_df.sort_values(by=sort_col_list, axis=0, ignore_index=True)
        if rename_dict is not None:
            new_df = new_df.rename(columns=rename_dict)
            print('After rename', new_df.columns)
        print(INFO, 'Final DF len:', len(new_df))

        return new_df

    def aggregate_server_log_csv(self, region, folder_name, out_path):
        if region == 'us':
            log_dir = 'Field Test/STM32 Node Deployment - US/'
            # self.config["data_path_prefix_us"]
        elif region == 'cn':
            log_dir = 'Field Test/'

        rename_dict = {'UE_ID': 'node_id',
                       'Pack_index': 'packet_index',
                       'UE_Type': 'module',
                       'Operator': 'operator',
                       'App_Type': 'app',
                       'Sleep_Timer': 'sleep_timer',
                       'CSQ': 'csq',
                       'Earfcn': 'earfcn',
                       'Pci': 'pci',
                       'Cell_Id': 'cell_id',
                       'ECL': 'ecl',
                       'RSRQ': 'rsrq',
                       'RSRP': 'rsrp',
                       'SNR': 'snr',
                       'Temperature': 'temperature',
                       'Humidity': 'rh',
                       'V_Bat': 'v_batt',
                       'UBHV': 'ubhv',
                       'UMHV': 'umhv',
                       'MSV': 'msv',
                       'ERROR_CODE': 'err_code',
                       'Test_ID': 'test_id',
                       'Pack Len': 'packet_len',
                       'Pack Timer': 'packet_timestamp'}

        new_df = self.aggregate_csv(self.global_path + log_dir + folder_name,
                                    sort_col_list=['UE_ID', 'Test_ID', 'Pack_index'],
                                    rename_dict=rename_dict)
        new_order = ['node_id', 'test_id', 'packet_index', 'app', 'csq', 'rsrp', 'snr', 'ecl', 'earfcn', 'pci', 'cell_id', 'rsrq', 'module', 'operator', 'packet_timestamp', 'temperature', 'rh', 'v_batt', 'ubhv', 'umhv', 'msv', 'err_code', 'sleep_timer', 'packet_len']
        new_df = new_df[new_order]

        # Type convertion
        int_type_var_list = ['ecl', 'earfcn', 'packet_len', 'module', 'operator', 'app', 'csq', 'sleep_timer', 'packet_len', 'ubhv', 'umhv', 'msv', 'err_code']
        for v in int_type_var_list:
            try:
                new_df[v] = new_df[v].astype('int')
            except ValueError:
                print(ERR, 'Has NA/INF in', v)
                new_df[v].fillna(-1, inplace=True)
                # new_df[v] = new_df[v].astype('int')

        # Save to file
        new_df.to_csv(out_path, sep=',', index=None, header=True)

    def merge_server_log_and_test_meta(self, server_log_path, test_meta_path, out_path):
        df_server = pd.read_csv(server_log_path, engine='python')
        df_meta = pd.read_csv(test_meta_path, engine='python')
        df_server = df_server.drop(columns=['operator', 'app'])
        df_meta = df_meta.drop(columns=['date', 'start_time'])
        print(df_server)
        print(df_meta)
        # new_df = pd.concat([df_server, df_meta], axis=1, sort=True)

        df_server.test_id.astype(int)
        df_meta.test_id.astype(int)

        new_df = pd.merge(df_server, df_meta, how='inner', on=['node_id', 'test_id'])
        print(new_df)
        new_df.to_csv(out_path, sep=',', index=None, header=True)

    def merge_cn_us_server_log(self, cn_csv_path, us_csv_path, out_path):
        df_cn = pd.read_csv(cn_csv_path, engine='python')
        df_us = pd.read_csv(us_csv_path, engine='python')
        # new_df = pd.concat([df_us, df_cn], axis=0, ignore_index=True, sort=False)
        new_df = pd.concat([df_cn, df_us], ignore_index=True)

        print(new_df)
        new_df.to_csv(out_path, sep=',', index=None, header=True)

    def merge_energy_stats_and_node_log(self, energy_stats_csv_path, packet_log_csv_path, out_path):
        '''Merge AT radio info, sensor readings .etc to packet energy csv stats.
        The energy stats contains cn+us logs. Please concat cn+us server log first.'''
        df_energy = pd.read_csv(energy_stats_csv_path, engine='python')
        df_log = pd.read_csv(packet_log_csv_path, engine='python')

        print(df_energy)
        print(df_log)

        df_all = pd.merge(df_log, df_energy, how='outer', on=['node_id', 'test_id', 'packet_index'])
        print(df_all)
        columns = df_all.columns

        df_all['module'] = df_all['module'].astype('str')
        df_all['module'] = df_all.apply(lambda x: self.node_id_to_module_dict[x['node_id']], axis=1)
        df_all = df_all.sort_values(by=['node_id', 'test_id', 'packet_index'], axis=0)
        df_all.to_csv(out_path, sep=',', index=None, header=True, columns=list(columns))

    def search_abnormal_current_amarisoft(self):
        df = pd.DataFrame(columns=['filename', 'filesize'])
        i = 0
        for dir in self.config['current_data_folder_list_amarisoft']:
            file_list = self.get_all_current_log_filename_list(self.raw_log_dir_amarisoft + dir, '.log')
            # file_list = self.get_all_current_log_filename_list("F:/Amarisoft_SDR_Optimization/" + dir, '.log')
            for f in file_list:
                fsize = os.path.getsize(f)
                if fsize > 1000*1024:
                    df.loc[i] = [f, fsize]
                    i += 1
        df.to_csv(self.global_path +
                  "Field Test/Useless Data/20200218_amarisoft_abnormal_current_log/abnormal_current_log_list.csv",
                  index=False)

    def solve_abnormal_current_amarisoft(self):
        df_file = pd.read_csv(self.global_path +
                  "Field Test/Useless Data/20200218_amarisoft_abnormal_current_log/abnormal_current_log_list.csv")
        df_file['initial_time_start'] = None
        df_file['new_time_start'] = None
        df_file['file_pos'] = None

        for i in range(0, len(df_file)):

            f = df_file.iloc[i]['filename']
            fsize = df_file.iloc[i]['filesize']
            packet_num = int(fsize / (1000*1024)) + 1
            # print(DBG, f.split('/')[-1], packet_num)
            packet_count = 1
            pos = 0
            if self.region in {'us', 'cndy', 'opt', 'sz'}:
                fp = f  # absolute path
            else:
                fp = self.raw_log_dir + f + ".log"

            with open(fp, 'rb') as f_r:
                offset = 0
                data = f_r.read(4)
                last_ts = int.from_bytes(data[0:2], byteorder="little", signed=False)
                df_file.loc[i, 'initial_time_start'] = last_ts / 1000
                data = f_r.read(4)
                count_read = 2
                while data:
                    # two bytes for timestamp, unit='ms'
                    ts = int.from_bytes(data[0:2], byteorder="little", signed=False)

                    if ts != last_ts:
                        t1 = last_ts + offset * 65536
                        if ts < last_ts:
                            offset += 1
                            # last_ts = 0
                        t2 = ts + offset * 65536

                        # the time gap between two packets' current is about 10+ seconds
                        # there may be several time period during the gap and split the gap into several parts
                        # according to current size, one file includes no more than 2 packets
                        if t2 - t1 > 5000:
                            packet_count += 1
                            print('DBG0:', t1/1000, t2/1000)
                            df_file.loc[i, 'new_time_start'] = t2/1000
                            if packet_count == packet_num:
                                # find the true current timestamp
                                pos = f_r.tell()
                                df_file.loc[i, 'file_pos'] = pos
                                break
                        # start new group
                        last_ts = ts
                    data = f_r.read(4)
                    count_read += 1
                # copy the left from current log file
                new_current = f_r.read(fsize - pos)

            # plot current file
            # df_current = self.current_raw_to_df(fp)
            # figname = fp.split('.')[0].split('/')[-1]
            # self.v.plot_current(df_current, figname, show_flag=True, is_amarisoft=True)

            # move the old current log to "Field Test/Useless Data/20200218_amarisoft_abnormal_current_log"
            des_path = self.global_path + "Field Test/Useless Data/20200218_amarisoft_abnormal_current_log/" + fp.split('/')[-1]
            shutil.move(fp, des_path)
            # write new current log into files
            f_w = open(fp, 'wb')
            f_w.write(new_current)

        df_file.to_csv(self.global_path +
                  "Field Test/Useless Data/20200218_amarisoft_abnormal_current_log/abnormal_current_log_list.csv",
                  index=False)
