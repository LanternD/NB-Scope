import datetime
import os
import pickle

import pandas as pd

from CurrentLogProcessor import CurrentLogProcessor
from DataVisualizer import DataVisualizer
from DeploymentDataProcessor import DeploymentDataProcessor
from PostFieldTestProcessor import PostFieldTestProcessor
from RawLogProcessor import RawLogProcessor

whoami = 'dy' #'ls'


def get_pack_delta(pftp):
    df_db = pd.read_csv(pftp.ft_db_csv_fn, low_memory=False).dropna(subset=['packet_timestamp'])
    df = df_db[['node_id', 'test_id', 'packet_index', 'packet_timestamp']].copy()
    ue_dict = pftp.config['node_id_to_module_dict']
    df['ue_type'] = [ue_dict[df.iloc[i]['node_id']] for i in range(0, len(df))]
    df['t_stop'] = None
    df['pack_delta_t'] = None

    for (test_id, node_id), group in df.groupby(['test_id', 'node_id']):
        # df1 = group.copy().set_index()
        print("***********{0}, {1}************".format(test_id, node_id))
        index_df = group.index.values
        time_format_1 = "_%Y%m%d_%H%M_%S"
        time_format_2 = "%Y%m%d_%H%M%S"
        for i in range(0, len(group) - 1):
            pack_id = group.iloc[i]['packet_index']
            str_t1 = group.iloc[i]['packet_timestamp']
            str_t2 = group.iloc[i + 1]['packet_timestamp']
            if str_t1.find('_') == 0:
                t1 = datetime.datetime.strptime(str_t1, time_format_1)
                if group.iloc[i + 1]['packet_index'] - pack_id == 1:
                    t2 = datetime.datetime.strptime(str_t2, time_format_1)
                    df.loc[index_df[i], 't_stop'] = str_t2
                    df.loc[index_df[i], 'pack_delta_t'] = t2 - t1

                    # print('pack_id:{3}, t1:{0}, t2:{1}, delta_t:{2}'.format(str_t1, str_t2, t2-t1, pack_id))
                else:
                    df.loc[index_df[i], 'pack_delta_t'] = None
            else:
                t1 = datetime.datetime.strptime(str_t1, time_format_2)
                if group.iloc[i + 1]['packet_index'] - pack_id == 1:
                    t2 = datetime.datetime.strptime(str_t2, time_format_2)
                    df.loc[index_df[i], 't_stop'] = str_t2
                    df.loc[index_df[i], 'pack_delta_t'] = t2 - t1
                else:
                    df.loc[index_df[i], 'pack_delta_t'] = None

    df.to_csv('D:/temp/df_pack_delta_t.csv')


def get_test_delta(pftp):
    df_db = pd.read_csv(pftp.ft_db_csv_fn, low_memory=False).dropna(subset=['packet_timestamp']).reset_index(drop=True)
    df = df_db[['node_id', 'test_id', 'packet_index', 'packet_timestamp', 'assigned_total_packet']].copy()
    print(datetime.datetime.now())
    # change two timestamp format into one type
    for i in range(0, len(df['packet_timestamp'])):
        ts = df.iloc[i]['packet_timestamp']
        if len(ts) == 17:
            tmp = ts.split('_')
            df.loc[i, 'packet_timestamp'] = tmp[1] + '_' + tmp[2] + tmp[3]

    df_result = pd.DataFrame(columns=['test_id', 'node_id', 'assigned_total_packet', 'pack_id_start', 'pack_id_end',
                                      'pack_count', 't_start', 't_end'])
    j = 0
    for (test_id, node_id), group in df.groupby(['test_id', 'node_id']):
        # df1 = group.copy().set_index()
        # print("***********{0}, {1}************".format(test_id, node_id))
        total = 20

        group = group[group['packet_index'] <= total].copy()
        if len(group) <= 1:
            continue

        count_pack = 1
        t_start = group.iloc[0]['packet_timestamp']
        pack_id_start = group.iloc[0]['packet_index']

        for i in range(1, len(group)):
            count_pack += 1
            t_end = group.iloc[i]['packet_timestamp']
            pack_id_end = group.iloc[i]['packet_index']
            if group.iloc[i]['packet_index'] == total:
                break
            elif group.iloc[i]['packet_index'] > total:
                t_end = group.iloc[i - 1]['packet_timestamp']
                pack_id_end = group.iloc[i - 1]['packet_index']
                break

        df_result.loc[j] = [test_id, node_id, total, pack_id_start, pack_id_end, count_pack, t_start, t_end]
        j += 1

    ue_dict = pftp.config['node_id_to_module_dict']
    df_result['ue_type'] = [ue_dict[df_result.iloc[i]['node_id']] for i in range(0, len(df_result))]
    df_result['delta_t'] = None
    for i in range(0, len(df_result)):
        t_start = datetime.datetime.strptime(df_result.iloc[i]['t_start'], "%Y%m%d_%H%M%S")
        t_end = datetime.datetime.strptime(df_result.iloc[i]['t_end'], "%Y%m%d_%H%M%S")
        df_result.loc[i, 'delta_t'] = (t_end - t_start).seconds
    df_result.to_csv('D:/temp/test_delta_time.csv', index=False)


def plot_function(flag):
    pftp = PostFieldTestProcessor(whoami)
    dv = DataVisualizer(whoami)
    if flag == 1:
        nut_prefix = '/Users/dlyang/Nutstore Files/NutstoreX/'
        df_agg = pd.read_csv(nut_prefix+'/Field Test/Deployment Experiment Output/post_ft_processing/new_field_test_info.csv')
        df = df_agg[(df_agg['app'] == 'SD') & (df_agg['ecl0_count'] < 100)][['node_id', 'app', 'delivery_rate']].copy()

        # get module type
        ue_dict = pftp.config['node_id_to_module_dict']
        df['ue_type'] = [ue_dict[df.iloc[i]['node_id']] for i in range(0, len(df))]
        df = df[df['delivery_rate'] > 0]
        print(df['delivery_rate'].describe())
        dv.plot_delivery_rate_vs_modules(df)

    elif flag == 2:
        df_db = pd.read_csv(pftp.ft_db_csv_fn, low_memory=False)
        df_db = df_db[(df_db['ecl'] == '0') | (df_db['ecl'] == '1') | (df_db['ecl'] == '2')]
        df = df_db[(df_db['app'] == 'SD')][['node_id', 'app', 'i_max', 'ecl', 'e_active']].copy()
        ue_dict = pftp.config['node_id_to_module_dict']
        df['ue_type'] = [ue_dict[df.iloc[i]['node_id']] for i in range(0, len(df))]
        dv.plot_i_max_vs_modules(df)

    elif flag == 3:
        df_db = pd.read_csv(pftp.ft_db_csv_fn, low_memory=False)
        df_db = df_db[(df_db['ecl'] == '0') | (df_db['ecl'] == '1') | (df_db['ecl'] == '2')]
        df = df_db[(df_db['app'] == 'SD') & (df_db.e_active > 0)][['node_id', 'app', 'i_max', 'ecl', 'e_active']].copy()
        ue_dict = pftp.config['node_id_to_module_dict']
        df['ue_type'] = [ue_dict[df.iloc[i]['node_id']] for i in range(0, len(df))]
        df['e_active'] /= 1000
        dv.plot_e_active_vs_modules(df)

    if flag == 4:
        # get_pack_delta(pftp)
        # csv_path = 'D:/temp/df_pack_delta_t.csv'
        csv_path = '/Users/dlyang/Nutstore Files/NutstoreX/Field Test/Deployment Experiment Output/post_ft_processing/df_pack_delta_t.csv'
        df = pd.read_csv(csv_path).dropna(subset=['pack_delta_t']).reset_index(drop=True)
        df['pack_seconds'] = 0
        for i in range(0, len(df)):
            tmp = df.iloc[i]['pack_delta_t'].split(':')
            # print(tmp)
            # h, m, s = [int(x) for x in tmp]
            # print(h, m, s)
            # df.loc[i, "pack_seconds"] = s + m * 60 + h * 3600
            for j in range(0, len(tmp)):
                df.loc[i, 'pack_seconds'] += pow(60, 2 - j) * int(tmp[j])
            # print(i, df.loc[i]['pack_seconds'])
        df = df[df['pack_seconds'] < 1000]
        pftp.v.plot_pack_delta_t_vs_module_type(df)

    if flag == 5:
        nut_prefix = '/Users/dlyang/Nutstore Files/NutstoreX/Field Test/Deployment Experiment Output/post_ft_processing/'
        df = pd.read_csv(nut_prefix+'test_delta_time.csv')
        df['delta_t'] /= 60  # change seconds in to minutes
        # df['test_time_estimated'] = (df['delta_t'] / (df['pack_id_end'] - df['pack_id_start'])) * 20
        # df['test_time_estimated'] = None
        for i in range(0, len(df)):
            if df.iloc[i]['ue_type'] in ['BG96', 'SARA', 'BC66']:
                df.loc[i, 'test_time_estimated'] = (df.iloc[i]['delta_t'] / (df.iloc[i]['pack_id_end'] -
                                                                             df.iloc[i]['pack_id_start'])) * 20 + 3  # compensate for the sleep timer difference.
            else:
                df.loc[i, 'test_time_estimated'] = (df.iloc[i]['delta_t'] / (df.iloc[i]['pack_id_end']
                                                                             - df.iloc[i]['pack_id_start'])) * 20
        df = df[df['pack_count'] >= 10]
        # df = df[df['delta_t'] < 58]
        df = df[df['test_time_estimated'] < 60]
        pftp.v.plot_test_delta_t(df)


def plot_current_main_ls(root, flist):
    clp = CurrentLogProcessor(whoami='ls', region='sz')
    for f in flist:
        figname = f.split('/')[-1]
        df = clp.current_raw_to_df(root + f)
        clp.v.plot_current(df, figname, show_flag=True)


def get_pkl(rootpath):
    # rootpath = 'D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/Msg3_Rep/DBG_Log/Msg3_Rep=8/'
    device_name = 'BC35'
    filter_out_list = {'N/A', 'UICC_DBG_LOG_P0', 'UICC_DBG_LOG_P1',
                       'UICC_DBG_LOG_P2'}  # add item to only one of them!!! E.g. to remove invalid message, use 'N/A'.
    filter_in_list = {}  # add item to only one of them!!!
    filter_dict = {'FO': filter_out_list, 'FI': filter_in_list}
    rlp = RawLogProcessor(device_name, filter_dict)

    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            print(dirs)
            for f in files:
                flist.append(root + '/' + f)
    rlp.pipeline_from_raw_to_csv(flist)


def get_msg3_rtx_1():
    # rep = 8
    # rep = 16
    # dbg_log = 'D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/Msg3_Rep/DBG_Log/'
    # get_pkl(dbg_log+'Msg3_Rep='+str(rep)+'/')
    # rep = 32
    # dbg_log = 'D:/Nutstore/我的坚果云/Field Test/Amarisoft_SDR_Optimization/Inactivetimer/DBG/Timer=20s/'
    # get_pkl(dbg_log)

    ddp = DeploymentDataProcessor('ls')
    rootpath = 'D:/Nutstore/我的坚果云/Field Test/Deployment Experiment Output/decoded_pkl/'
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            for f in files:
                flist.append(root + '/' + f)
    df = pd.DataFrame(columns=['node_id', 'test_id', 'pack_id', 'msg3_rep', 'msg1_tx', 'msg2_rx', 'msg4_rx'])
    i = 0
    for f in flist:
        fn = f.split('/')[-1].split('.')[0].split('_')
        node_id, test_id, pack_id = fn[0], fn[2], fn[3]
        count_msg1 = 0
        count_msg2 = 0
        count_msg4 = 0
        msg_list = ddp.load_pickle_file(f)
        for m in msg_list:
            if m[3] == 'LL1_RAR_UL_GRANT':
                count_msg2 += 1
            elif m[3] == 'LL1_NPRACH_START_TIME':
                count_msg1 += 1
            elif m[3] == 'LL1_RACH_CONTENTION_RESOLUTION_SUCCESS_IND':
                count_msg4 += 1
        df.loc[i] = [node_id, test_id, pack_id, rep, count_msg1, count_msg2, count_msg4]
        i += 1
    df.to_csv('D:/temp/rep=16.csv', index=False)


def get_msg3_rtx_field_test():
    ddp = DeploymentDataProcessor('ls')
    rootpath = 'F:/field_test_output_copy/decoded_pkl_1/'
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            for f in files:
                flist.append(root + '/' + f)
    print(len(flist))
    df = pd.DataFrame(columns=['node_id', 'test_id', 'pack_id', 'msg1_tx', 'msg2_rx', 'msg4_rx'])
    i = 0
    for f in flist:
        fn = f.split('/')[-1].split('.')[0].split('_')
        node_id, test_id, pack_id = fn[2], fn[4], fn[5]
        count_msg1 = 0
        count_msg2 = 0
        count_msg4 = 0
        msg_list = ddp.load_pickle_file(f)
        for m in msg_list:
            if m[3] == 'LL1_RAR_UL_GRANT':
                count_msg2 += 1
            elif m[3] == 'LL1_NPRACH_START_TIME':
                count_msg1 += 1
            elif m[3] == 'LL1_RACH_CONTENTION_RESOLUTION_SUCCESS_IND':
                count_msg4 += 1
        df.loc[i] = [node_id, test_id, pack_id, count_msg1, count_msg2, count_msg4]
        i += 1
    df.to_csv('D:/temp/field_test_msg3.csv', index=False)


def get_field_test_ecl_info():
    # important cell info: msg1 rep, msg3 rep, threshold, ecl
    ddp = DeploymentDataProcessor('ls')
    rootpath = 'F:/field_test_output_copy/decoded_pkl_1/'
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            for f in files:
                flist.append(root + '/' + f)
    print(len(flist))
    df = pd.DataFrame(columns=['node_id', 'test_id', 'pack_id', 'ra_id', 'ecl', 'selected_by', 'threshold'])
    i = 0
    for f in flist:
        fn = f.split('/')[-1].split('.')[0].split('_')
        node_id, test_id, pack_id, ra_id = fn[2], fn[4], fn[5], 1

        msg_list = ddp.load_pickle_file(f)
        for m in msg_list:
            if m[3] == 'LL1_LOG_ECL_INFO':
                if i != 0 and (node_id, pack_id, test_id) == (
                df.iloc[i - 1]['node_id'], df.iloc[i - 1]['pack_id'], df.iloc[i - 1]['test_id']):
                    ra_id += 1
                ecl = m[7]['current_ecl']
                ecl_by = m[7]['ecl_selected_by'].split('(')[0]
                threshold = m[7]['threshold']
                df.loc[i] = [node_id, test_id, pack_id, ra_id, ecl, ecl_by, threshold]
                i += 1
    df.to_csv('D:/temp/field_test_ecl.csv', index=False)


def get_field_test_msg1_info():
    # important cell info: msg1 rep, msg3 rep, threshold, ecl
    ddp = DeploymentDataProcessor('ls')
    rootpath = 'F:/field_test_output_copy/decoded_pkl_1/'
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            for f in files:
                flist.append(root + '/' + f)
    print(len(flist))
    df = pd.DataFrame(columns=['node_id', 'test_id', 'pack_id', 'ra_id', 'hfn1', 'sfn1', 'sf1', 'hfn2', 'sfn2', 'sf2'])
    i = 0
    for f in flist:
        fn = f.split('/')[-1].split('.')[0].split('_')
        node_id, test_id, pack_id, ra_id = fn[2], fn[4], fn[5], 1

        msg_list = ddp.load_pickle_file(f)
        for m in msg_list:
            if m[3] == 'LL1_NPRACH_START_TIME':
                if i != 0 and (node_id, pack_id, test_id) == (
                df.iloc[i - 1]['node_id'], df.iloc[i - 1]['pack_id'], df.iloc[i - 1]['test_id']):
                    ra_id += 1
                hfn1, sfn1, sf1 = m[7]['hfn'], m[7]['sfn'], m[7]['sf']
            elif m[3] == 'LL1_NPRACH_END_TIME':
                hfn2, sfn2, sf2 = m[7]['hfn'], m[7]['sfn'], m[7]['sf']

                df.loc[i] = [node_id, test_id, pack_id, ra_id, hfn1, sfn1, sf1, hfn2, sfn2, sf2]
                i += 1
    df.to_csv('D:/temp/field_test_msg1.csv', index=False)


def get_field_test_msg3_info():
    # important cell info: msg1 rep, msg3 rep, threshold, ecl
    ddp = DeploymentDataProcessor('ls')
    rootpath = 'F:/field_test_output_copy/decoded_pkl_1/'
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            for f in files:
                flist.append(root + '/' + f)
    print(len(flist))
    df = pd.DataFrame(
        columns=['node_id', 'test_id', 'pack_id', 'ra_id'] + ['subcarrier_ind_nsc', 'pusch_start_subframe',
                                                              'modulation_coding_scheme_tbs', 'repetition_number',
                                                              'subcarrier_space', 'modulation_coding_scheme_imcs',
                                                              'modulation_coding_scheme_itbs',
                                                              'modulation_coding_scheme_qm', 'subcarrier_ind_isc',
                                                              'subcarrier_ind_len', 'resource_unit_number',
                                                              'result', 'expected_rapid'])
    i = 0
    for f in flist:
        fn = f.split('/')[-1].split('.')[0].split('_')
        node_id, test_id, pack_id, ra_id = fn[2], fn[4], fn[5], 1

        msg_list = ddp.load_pickle_file(f)
        for m in msg_list:
            if m[3] == 'LL1_RAR_UL_GRANT':
                if i != 0 and (node_id, pack_id, test_id) == (
                df.iloc[i - 1]['node_id'], df.iloc[i - 1]['pack_id'], df.iloc[i - 1]['test_id']):
                    ra_id += 1

                df.loc[i] = [node_id, test_id, pack_id, ra_id] + list(m[7]['rar_pdu'].values()) + [m[7]['result'], m[7][
                    'expected_rapid']]
                i += 1
    df.to_csv('D:/temp/field_test_msg3.csv', index=False)


def merge_ra_info():
    df_ecl = pd.read_csv('D:/temp/field_test_ecl.csv')
    df_msg1 = pd.read_csv('D:/temp/field_test_msg1.csv')
    df_msg3 = pd.read_csv('D:/temp/field_test_msg3.csv')

    df_tmp = pd.merge(df_ecl, df_msg1, how='outer', on=['node_id', 'test_id', 'pack_id', 'ra_id'])
    df_result = pd.merge(df_tmp, df_msg3, how='outer', on=['node_id', 'test_id', 'pack_id', 'ra_id'])
    df_result.to_csv('D:/temp/ra_info_merge.csv', index=False)


def get_ra_info():
    ddp = DeploymentDataProcessor('ls')
    rootpath = 'F:/field_test_output_copy/decoded_pkl_1/'
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files) != 0:
            for f in files:
                flist.append(root + '/' + f)
    print(len(flist))
    df = pd.DataFrame(
        columns=['node_id', 'test_id', 'pack_id', 'ra_id'] + ['ecl', 'selected_by', 'threshold',
                                                              'hfn1', 'sfn1', 'sf1', 'hfn2', 'sfn2', 'sf2',
                                                              'subcarrier_ind_nsc', 'pusch_start_subframe',
                                                              'modulation_coding_scheme_tbs', 'repetition_number',
                                                              'subcarrier_space', 'modulation_coding_scheme_imcs',
                                                              'modulation_coding_scheme_itbs',
                                                              'modulation_coding_scheme_qm', 'subcarrier_ind_isc',
                                                              'subcarrier_ind_len', 'resource_unit_number',
                                                              'result', 'expected_rapid'])
    i = 0
    states = {'START': 0, 'ECL': 1, 'MSG1_START': 2, 'MSG1_END': 3,
              'RAR': 4, 'FINISHED': 5}
    ecl_list = 3 * [None]
    msg1_start_list = 3 * [None]
    msg1_end_list = 3 * [None]
    rar_list = 13 * [None]
    for j in range(0, len(flist)):
        f = flist[j]
        if j % 10 == 0:
            print('DEBUG: ', j, ' / ', len(flist))
        fn = f.split('/')[-1].split('.')[0].split('_')
        node_id, test_id, pack_id, ra_id = fn[2], fn[4], fn[5], 1
        msg_list = ddp.load_pickle_file(f)
        st = states['START']

        for m in msg_list:
            if st == states['START']:
                if m[3] == 'LL1_LOG_ECL_INFO':
                    ecl_list = [m[7]['current_ecl'], m[7]['ecl_selected_by'].split('(')[0], m[7]['threshold']]
                    st = states['ECL']
                elif m[3] == 'LL1_NPRACH_START_TIME':
                    msg1_start_list = [m[7]['hfn'], m[7]['sfn'], m[7]['sf']]
                    st = states['MSG1_START']
                elif m[3] == 'LL1_NPRACH_END_TIME':
                    msg1_end_list = [m[7]['hfn'], m[7]['sfn'], m[7]['sf']]
                    st = states['MSG1_END']
                elif m[3] == 'LL1_RAR_UL_GRANT':
                    rar_list = list(m[7]['rar_pdu'].values()) + [m[7]['result'], m[7]['expected_rapid']]
                    st = states['RAR']
            elif st == states['ECL']:
                if m[3] == 'LL1_NPRACH_START_TIME':
                    msg1_start_list = [m[7]['hfn'], m[7]['sfn'], m[7]['sf']]
                    st = states['MSG1_START']
            elif st == states['MSG1_START']:
                if m[3] == 'LL1_NPRACH_END_TIME':
                    msg1_end_list = [m[7]['hfn'], m[7]['sfn'], m[7]['sf']]
                    st = states['MSG1_END']
            elif st == states['MSG1_END']:
                if m[3] == 'LL1_RAR_UL_GRANT':
                    rar_list = list(m[7]['rar_pdu'].values()) + [m[7]['result'], m[7]['expected_rapid']]
                    st = states['RAR']
            elif st == states['RAR']:
                if m[3] == 'LL1_LOG_ECL_INFO':
                    # last RA finished and start new RA
                    df.loc[i] = [node_id, test_id, pack_id,
                                 ra_id] + ecl_list + msg1_start_list + msg1_end_list + rar_list
                    i += 1
                    ecl_list = 3 * [None]
                    msg1_start_list = 3 * [None]
                    msg1_end_list = 3 * [None]
                    rar_list = 13 * [None]

                    ra_id += 1
                    ecl_list = [m[7]['current_ecl'], m[7]['ecl_selected_by'].split('(')[0], m[7]['threshold']]
                    st = states['ECL']
        df.loc[i] = [node_id, test_id, pack_id, ra_id] + ecl_list + msg1_start_list + msg1_end_list + rar_list
        i += 1
        ecl_list = 3 * [None]
        msg1_start_list = 3 * [None]
        msg1_end_list = 3 * [None]
        rar_list = 13 * [None]

    df.to_csv('D:/temp/field_test_ra_info.csv', index=False)


def get_msg1_width_from_log():
    df = pd.read_csv('D:/temp/ra_info_merge.csv')
    df['msg1_t'] = 0
    for i in range(0, len(df)):
        df.loc[i, 'msg1_t'] = 1024 * (df.iloc[i]['hfn2'] - df.iloc[i]['hfn1']) + 10 * (
                    df.iloc[i]['sfn2'] - df.iloc[i]['sfn1']) +  1 * (df.iloc[i]['sf2'] - df.iloc[i]['sf1'])
    df.to_csv('D:/temp/ra_info_merge.csv', index=False)


def merge_meta_with_field_test_ra_info():
    import numpy as np
    df = pd.read_csv('D:/temp/field_test_ra_info.csv')
    op_dict = {'C05': 'CT', 'C06': 'CT', 'C07': 'CM', 'C08': 'CM', 'D03': 'CT', 'D04': 'CM', 'D09': 'CT', 'D10': 'CM'}
    df['operator'] = None
    df['msg1_t'] = None
    for i in range(0, len(df)):
        df.loc[i, 'operator'] = op_dict[df.iloc[i]['node_id']]
        df.loc[i, 'msg1_t'] = 1024 * (df.iloc[i]['hfn2'] - df.iloc[i]['hfn1']) + 10 * (
                    df.iloc[i]['sfn2'] - df.iloc[i]['sfn1']) + 1 * (df.iloc[i]['sf2'] - df.iloc[i]['sf1'])
        if np.isnan(df.iloc[i]['ecl']) == True and np.isnan(df.iloc[i]['msg1_t']) == False:
            if df.iloc[i]['msg1_t'] == 11:
                df.loc[i, 'ecl'] = 0
            elif df.iloc[i]['msg1_t'] == 44:
                df.loc[i, 'ecl'] = 1
            elif df.iloc[i]['msg1_t'] == 179:
                df.loc[i, 'ecl'] = 2
        if df.iloc[i]['threshold'] is not np.nan:
            threshold = list(map(eval, df.iloc[i]['threshold'][1:-1].split(', ')))
            threshold = [x-65536 for x in threshold]
            df.loc[i, 'threshold'] = str(threshold[0]) + ',' + str(threshold[1])
    df.to_csv('D:/Nutstore/我的坚果云/Field Test/Deployment Experiment Output/post_ft_processing/ra_info.csv', index=False)

def get_meta_cn_from_database():
    df = pd.read_csv('F:/Field Test/Deployment Experiment Output/csv_to_be_merged/field_test_database.csv', low_memory=False)
    df_result = pd.DataFrame(columns=['node_id','test_id', 'date', 'start_time', 'app', 'assigned_total_packet',
                                                              'operator', 'location', 'lat', 'long', 'group'])
    i = 0
    group_id = {'C01': 1,
                'C02': 2,
                'C03': 1,
                'C04': 2,
                'C05': 1,
                'C06': 2,
                'C07': 1,
                'C08': 2,
                'C09': 1,
                'C10': 2,
                'C11': 1,
                'C12': 2}

    for (node_id, test_id), group in df.groupby(['node_id', 'test_id']):
        if node_id not in group_id.keys():
            continue
        df_result.loc[i] = [node_id, test_id, '', '', group.iloc[0]['app'], group.iloc[0]['assigned_total_packet'],
                            group.iloc[0]['operator'], group.iloc[0]['location'], group.iloc[0]['lat'],
                            group.iloc[0]['long'], group_id[node_id]]
        i += 1
    df_result.to_csv('D:/temp/field_test_meta_cn.csv', index=False)

def merge_nj_sz_meta():
    df1 = pd.read_csv('D:/temp/field_test_meta_cn.csv')
    df2 = pd.read_csv('D:/Nutstore/我的坚果云/Field Test/STM32 Node Deployment - SZ/meta.csv',
                      names=['index', 'date', 'start_time', 'node_id', 'test_id', 'location',
                             'lat', 'long', 'app', 'operator', 'assigned_total_packet', 'group', 'comment'],
                      skiprows=1)
    df2 = df2.drop(['index'], axis=1)
    df1['comment'] = None
    df3 = pd.concat([df1, df2], sort=True)
    df3.to_csv('D:/temp/meta_nj&sz.csv', index=False, columns=['node_id', 'test_id', 'date', 'start_time', 'location',
                             'lat', 'long', 'app', 'operator', 'assigned_total_packet', 'group', 'comment'])

if __name__ == '__main__':
    plot_function(flag=1)
    # get_msg3_rtx_1()
    # get_msg3_rtx_field_test()
    # get_field_test_ecl_info()
    # get_field_test_msg1_info()
    # get_field_test_msg3_info()
    # merge_ra_info()
    # get_ra_info()
    # merge_meta_with_field_test_ra_info()
    # get_meta_cn_from_database()
    # root = 'D:/Nutstore/我的坚果云/Field Test/STM32 Node Deployment/building-south35/'
    # flist =['C01_I_01004_0001.log', 'C01_I_01005_0012.log',
    #         'C02_I_01105_0004.log', 'C02_I_01106_0009.log',
    #         'C03_I_01103_0016.log', 'C03_I_01104_0006.log']
    # flist = ['C05_I_01101_0009.log', 'C05_I_01105_0017.log',
    #          'C06_I_01005_0023.log', 'C06_I_01008_0010.log',
    #          'C07_I_01004_0014.log', 'C07_I_01008_0019.log',
    #          'C08_I_01005_0003.log', 'C08_I_01011_0004.log']
    # flist = ['C09_I_01005_0008.log', 'C10_I_01008_0025.log', 'C11_I_01010_0003.log', 'C12_I_01102_0016.log']

    '''
    rootpath = 'D:/Nutstore/我的坚果云/Field Test/STM32 Node Deployment - SZ/Current/D03/'
    # flist = ['D03_I_22001_0003.log']
    # flist = ['D03_I_21801_0024.log', 'D03_I_22001_0017.log']
    flist = []
    for root, dirs, files in os.walk(rootpath):
        if len(files)!=0:
            for f in files:
                if f.split('_')[0] == 'D03' and f.split('_')[1] == 'I':
                    flist.append(f)
    plot_current_main_ls(rootpath, flist)
    '''
