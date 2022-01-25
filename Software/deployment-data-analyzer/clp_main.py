import os
import sys
import time

from CurrentLogProcessor import CurrentLogProcessor

whoami = 'dy'  # change this before running this script.
# whoami = 'ls'
region = 'cn'  # 'us'/'cndy'/'cn'/'opt'/'sz'
# Note: 'amarisoft' was replaced by 'opt'

'''
us: select the folder that has US field test logs.
cndy: use by DY only.
chn: select the folder that has China field test logs.
dpow: select the folder "Distance vs Power" test logs. (for Mobicom 2020 revision)
'''

def get_msg1_width(df, node_id):
    msg1_s, msg1_e, msg3_s, msg3_e = 0, 0, 0, 0
    tx_rx_threshold = 80
    msg3_threshold = 10
    # tx_rx_threshold = {'C01': 40, 'C02': 40, 'C03': 40, 'C04': 40, 'C05': 50}
    # FIND MSG1
    for i in range(1, len(df)):
        if df.iloc[i]['current'] > tx_rx_threshold and df.iloc[i-1]['current'] < tx_rx_threshold:
            msg1_s = df.iloc[i]['time']/1000
        elif df.iloc[i]['current'] < tx_rx_threshold and df.iloc[i-1]['current'] > tx_rx_threshold:
            msg1_e = df.iloc[i-1]['time']/1000
            if msg1_e - msg1_s > 0.008:
                break
            else:
                msg1_s, msg1_e = 0, 0
    # FIND MSG3
    df1 = df[df['time'] > msg1_e * 1000].copy().reset_index(drop=True)
    index = df1[df1.current > tx_rx_threshold].index[0]
    msg3_s = df1.iloc[index]['time'] / 1000
    df2 = df1[index:].copy().reset_index(drop=True)
    index = df2[df2.current < msg3_threshold].index[0] - 1
    msg3_e = df2.iloc[index].time/1000
    # FIND LAST DATA TX

    # FIND RRC RELEASE

    return msg1_s, msg1_e, msg3_s, msg3_e

def current_log_main_ls(filelist):
    clp = CurrentLogProcessor(whoami=whoami, region=region)
    # datadir = 'building-south35/'
    # allowed_node = {}
    # allowed_test_id = {}
    # clp.pipeline_plot(datadir, allowed_node, allowed_test_id)
    if len(filelist) == 0:
        # filepath = "D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/Inactivetimer/Down_OK_Inactivetimer/logs" \
        #            "/Logs/Current/Timer=20s/"
        # filepath = "D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/Inactivetimer/Current/Timer=20s/"

        filepath = "D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/benchmark/ECL1/BC26/C08/"

        for root, dirs, files in os.walk(filepath):
            pass
        filelist = [filepath + f for f in files]
    print(filelist)
    for f in filelist:
        filename = f.split('/')[-1]
        node_id = filename.split('_')[0]
        if filename.split('_')[1] == 'I':
            df = clp.current_raw_to_df(f)
            # msg1_s, msg1_e, msg3_s, msg3_e = get_msg1_width(df, node_id)
            # msg3_s, msg3_e = get_msg3_width(df, msg1_e)
            # print('**************************************************')
            # print(f.split('/')[-1].split('.')[0], msg1_e - msg1_s, msg3_e - msg3_s)
            # print("f: {4}  msg1_s:{0}  msg1_e:{1}  msg3_s:{2}  msg3_e:{3}\n".format(msg1_s, msg1_e, msg3_s, msg3_e,
            #                                                                         f.split('/')[-1].split('.')[0]))
            clp.v.plot_current(df, filename, show_flag=False)


def current_log_main_dy(function_switch):
    clp = CurrentLogProcessor(whoami=whoami, region=region)

    t0 = time.time()

    if function_switch == 0:
        '''Pipeline: convert current raw log to csv
        Benchmark: 3208.577 s for 10117 files on Zima
        Benchmark: 1h37min for 13740 files on Zima
        '''
        print('Pipeline: current raw.log to csv.')
        clp.pipeline_from_raw_to_csv(enable_multiprocessing=True)
    elif function_switch == 1:
        '''Pipeline: convert current csv to png visualization
        Obtain the current stats.
        Benchmark: 680.284 s for 1462 files (A02) on MSDY
        Benchmark: 414.391 s for 956 files (A05) on MSDY,no plot => 286 s
        Benchmark: 765.801 s for 1953 files (A03) on Zima
        '''
        print('Pipeline: current csv to png with stats.')
        clp.pipeline_df_to_current_plot_dy(enable_multiprocessing=True)

    elif function_switch == 2:
        # Single file processing. (For dev purpose)
        print('Development: One file processing.')
        fp = clp.current_csv_dir + 'C05/01312/C05_I_01312_0002.csv'
        df = clp.load_current_data_from_csv(fp)
        stats_dict = clp.calculate_energy_one_df(df)
        # clp.visualize_current_distribution(df)
        fn = clp.u.get_filename_from_path(fp)
        df['time'] = df['time'] * 1000  # /1000 in calc_eng_one_df
        clp.v.plot_current(df, fn, show_flag=True, stats_dict=stats_dict)

    elif function_switch == 3:
        # Find the unprocessed files (error occurs and stoped)
        rg = region
        ext_type = {'src': 'log', 'dst': 'csv'}
        # src_fp_list = clp.get_all_current_log_filename_list(clp.current_csv_dir+'A03/', f_extension='csv')
        # dst_fp_list = clp.get_all_current_log_filename_list(clp.v.figure_dir+'current_cn/A03/', f_extension='csv')
        src_fp_list = clp.get_all_current_log_filename_list(
            clp.global_path + clp.config['i_raw_folder_by_host'][rg],
            f_extension=ext_type['src'])
        dst_fp_list = clp.get_all_current_log_filename_list(
            clp.current_csv_dir, f_extension=ext_type['dst'])
        # log_fp_list = [x for x in log_fp_list if '_I_' in x]
        untouched_csv_list = clp.u.find_different_set_csv_png(src_fp_list, dst_fp_list)
        print('Length of untouched: {0}'.format(len(untouched_csv_list)))
        for x in untouched_csv_list:
            print(x)
        if untouched_csv_list is None:
            print('All the CSV files are proccessed.')

    elif function_switch == 4:
        ll = ['A03_I_01503_0013', 'A03_I_01503_0028']  # copy the filenames here.
        print('Caution: uncomment the line below to continue.')
        # clp.u.move_files_to_subfolder_by_name(clp.global_path+'Field Test/Deployment Experiment Output/figures/current_us/A03/', 'useless', ll, ext='png')

    elif function_switch == 5:
        all_node = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'C01', 'C02',
                    'C03', 'C04', 'C05', 'C06', 'C07', 'C08', 'C09', 'C10',
                    'C11', 'C12']

        clp.list_zero_energy_packets_drop_duplicates('C05')
        # for x in all_node:
        #     print(x)
        #     clp.list_zero_energy_packets(x)
    elif function_switch == 6:
        # get the file_list of abnormal current of amarisoft
        # current file size > 1.5MB
        # clp.search_abnormal_current_amarisoft()
        clp.solve_abnormal_current_amarisoft()

    t1 = time.time()
    print("Execution time:", '{0:.3f}'.format(t1-t0))


def pipeline_csv_processing(function_switch):
    clp = CurrentLogProcessor(whoami=whoami, region=region)
    t0 = time.time()

    if function_switch == -1:
        # Append new engery stats to existing ones.
        candidates = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06']
        clp.append_enery_stats_by_node_id(candidates)
    elif function_switch == 0:
        # Stack packet energy stats, US+CN
        new_df = clp.aggregate_csv(
            clp.output_dir + 'packet_energy_stats/sorted and 1st round processed/',
            is_energy_stats=True,
            sort_col_list=['node_id', 'test_id', 'packet_index'])
        while new_df.iloc[-1]['node_id'] == 'node_id':
            # Fix a strange bug
            new_df.drop(new_df.tail(1).index, inplace=True)
        out_path = clp.output_dir + 'csv_to_be_merged/all_packet_energy_stats.csv'
        new_df.to_csv(out_path, sep=',', index=None)
    elif function_switch == 1:
        # Stack server logs, US or CN
        rg = 'cn'
        out_path = clp.output_dir + 'csv_to_be_merged/server_packet_log_{0}_RAW.csv'.format(rg)
        if rg == 'us':
            clp.aggregate_server_log_csv(rg, 'US Server Log to be Merged/', out_path)
        elif rg == 'cn':
            clp.aggregate_server_log_csv(rg, 'Server Log NJ+SZ/', out_path)
    elif function_switch == 2:
        # Append test meta column to server logs, US or CN
        rg = 'cn'
        csv_dir = clp.output_dir + 'csv_to_be_merged/'
        clp.merge_server_log_and_test_meta(
            csv_dir + 'server_packet_log_{0}.csv'.format(rg),
            csv_dir + 'field_test_meta_info_{0}.csv'.format(rg),
            csv_dir + 'merged_server_log_{0}.csv'.format(rg))
    elif function_switch == 3:
        # Concat CN + US server log
        csv_dir = clp.output_dir + 'csv_to_be_merged/'
        clp.merge_cn_us_server_log(
            csv_dir + 'merged_server_log_cn.csv',
            csv_dir + 'merged_server_log_us.csv',
            csv_dir + 'all_server_packet_cn+us.csv')
    elif function_switch == 4:
        # Final step to merge, energy stats+server log, both CN+US
        csv_dir = clp.output_dir + 'csv_to_be_merged/'
        clp.merge_energy_stats_and_node_log(
            csv_dir + 'all_packet_energy_stats.csv',
            csv_dir + 'all_server_packet_cn+us.csv',
            clp.output_dir + 'post_ft_processing/field_test_database_RENAME.csv')

    t1 = time.time()
    print("Execution time:", '{0:.3f}'.format(t1-t0))


# DY: move these types of function to the class file.
def calc_power_consumption(dict, output):
    datadir = 'building-library/'
    t0 = time.time()
    clp = CurrentLogProcessor(whoami, region)
    import pandas as pd
    df_result = pd.DataFrame(columns=['file', 'energy'])
    for j in range(0, len(dict)):
        df_0 = clp.current_raw_to_df(datadir+dict[j]['file'])
        df_0['time'] /= 1000
        df = df_0[(df_0['time']>dict[j]['t1']) & (df_0['time']<dict[j]['t2']) & (df_0['current']<1)].copy()
        df_abnormal = df[df['current']<0]
        df_normal = df[df['current']>=0]
        print(len(df_abnormal), len(df), df_abnormal['current'].mean(), df_abnormal['current'].std(), df_normal['current'].mean(), df_normal['current'].std())
        energy = 0
        for i in range(0, len(df)-1):
            if df.iloc[i]['current'] < 0:
                energy -= (df.iloc[i]['current'] * (df.iloc[i+1]['time'] - df.iloc[i]['time']))
            else:
                energy += (df.iloc[i]['current'] * (df.iloc[i + 1]['time'] - df.iloc[i]['time']))
        if output == 'psm_power':
            result = energy * 360 * 3.3 * 0.001 # energy is 10 seconds
        elif output == 'edrx_power':
            result = energy * 703.125 * 3.3 * 0.001 # energy is 5.12 seconds
        df_result.loc[j] = [dict[j]['file'], result]
        # print(dict[j]['file'], result)
    df_result.to_csv('D:/temp/'+output+'.csv', header=True, index=False)
    print('using time:', time.time()-t0)


def calc_psm_edrx_power():
    psm_dict = [
        {'file': 'C05_I_01005_0002', 't1': 70, 't2': 80},
        {'file': 'C05_I_01102_0002', 't1': 70, 't2': 80},
        {'file': 'C05_I_01102_0008', 't1': 70, 't2': 80},
        {'file': 'C05_I_01102_0014', 't1': 70, 't2': 80},
        {'file': 'C05_I_01102_0022', 't1': 70, 't2': 80},
        {'file': 'C05_I_01105_0001', 't1': 70, 't2': 80},
        {'file': 'C05_I_01105_0003', 't1': 70, 't2': 80},
        {'file': 'C05_I_01105_0005', 't1': 70, 't2': 80},
        {'file': 'C05_I_01105_0007', 't1': 70, 't2': 80},
        {'file': 'C06_I_01105_0024', 't1': 90, 't2': 100},
        {'file': 'C06_I_01105_0020', 't1': 90, 't2': 100},
        {'file': 'C06_I_01104_0025', 't1': 90, 't2': 100},
        {'file': 'C07_I_01106_0024', 't1': 50, 't2': 60},
        {'file': 'C07_I_01106_0016', 't1': 50, 't2': 60},
        {'file': 'C07_I_01105_0017', 't1': 50, 't2': 60},
        # {'file': 'C05_I_01105_0009', 't1': 70, 't2': 80},
        # {'file': 'C05_I_01105_0011', 't1': 70, 't2': 80},
        # {'file': 'C05_I_01105_0013', 't1': 70, 't2': 80},
        # {'file': 'C05_I_01105_0015', 't1': 70, 't2': 80},
        # {'file': 'C05_I_01105_0017', 't1': 70, 't2': 80},
        # {'file': 'C05_I_01105_0019', 't1': 70, 't2': 80}
    ]
    edrx_dict = [
        {'file': 'C05_I_01304_0009', 't1': 58.05, 't2': 63.17},
        {'file': 'C05_I_01304_0013', 't1': 58.28, 't2': 63.4},
        {'file': 'C05_I_01304_0015', 't1': 67.53, 't2': 72.65},
        {'file': 'C06_I_01305_0009', 't1': 57.70, 't2': 62.82},
        {'file': 'C06_I_01305_0011', 't1': 56.01, 't2': 61.13},
        {'file': 'C06_I_01304_0022', 't1': 56.16, 't2': 61.28},
        {'file': 'C06_I_01304_0014', 't1': 55.61, 't2': 60.73},
        {'file': 'C07_I_01308_0013', 't1': 53.60, 't2': 58.72},
        {'file': 'C07_I_01308_0007', 't1': 64.06, 't2': 69.18},
        {'file': 'C07_I_01308_0001', 't1': 49.56, 't2': 54.68},
        {'file': 'C07_I_01307_0019', 't1': 48.6, 't2': 53.72},
        {'file': 'C08_I_01202_0024', 't1': 72.84, 't2': 77.96},
        {'file': 'C08_I_01202_0018', 't1': 33.17, 't2': 38.29},
        {'file': 'C08_I_01201_0015', 't1': 54.64, 't2': 59.76},
        {'file': 'C08_I_01201_0003', 't1': 69.01, 't2': 74.13}
    ]
    calc_power_consumption(edrx_dict, output='edrx_power')


if __name__ == '__main__':

    current_log_main_dy(function_switch=2)
    # pipeline_csv_processing(function_switch=4)

















    # root = "D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/Inactivetimer/" \
    #        "Down_OK_Inactivetimer/logs/Logs/Current/Timer=20s/"
    # filelist0 = ['C08_I_01528_0018', 'C08_I_01528_0023', 'C08_I_01528_0029', 'C08_I_01528_0035', 'C08_I_01528_0057',
    #             'C08_I_01528_0012', 'C08_I_01528_0058', 'C08_I_01528_0039', 'C08_I_01528_0016', 'C08_I_01528_0011']
    # filelist = [root+x+'.log' for x in filelist0]
