import os, sys
import pandas as pd
import numpy as np
from Utils import *
import datetime
import re


class ServerLogProcessor(object):

    def __init__(self, whoami):
        self.u = Utils()
        self.config = self.u.load_config('./config.json')
        self.global_path = self.config['env_prefix'][whoami][self.u.os]
        self.server_log_dir = self.global_path + self.config['data_path_prefix_cn'] + 'Sigcomm2020_fied_test_server_logs/'
        self.output_dir = self.global_path + self.config["output_path"]
        self.pftp_dir = self.output_dir + 'post_ft_processing/'
        self.server_log_summary = self.pftp_dir + 'field_test_database.csv'
        self.csv_to_be_merged = self.output_dir + 'csv_to_be_merged/'

    def add_column(self, file_dir, out_dir):
        # add several columns and change app_type
        fl = self.u.get_file_list(file_dir)
        dict_app = {'01004': 'WM', '01005': 'WM', '01006': 'WM', '01007': 'WM',
                '01008': 'SD', '01009': 'SD', '01010': 'SD', '01011': 'SD', '01101': 'SD',
                '01102': 'SL', '01103': 'SL', '01104': 'SL', '01105': 'SL', '01106': 'SL',
                '01201': 'SL', '01202': 'WM', '01203': 'SD',
                '01204': 'SL', '01205': 'WM', '01206': 'SD',
                '01207': 'SL', '01208': 'WM', '01209': 'SD',
                '01303': 'WM', '01304': 'SD', '01305': 'SL',
                '01306': 'WM', '01307': 'SD', '01308': 'SL',
                '01309': 'WM', '01310': 'SD', '01311': 'SL',
                '01312': 'WM', '01313': 'SD', '01314': 'SL',
                '01315': 'SL', '01316': 'WM',
                '01401': 'WM', '01402': 'WM', '01403': 'WM', '01404': 'WM', '01405': 'WM', '01406': 'WM',
                '01407': 'WM', '01408': 'WM', '01409': 'WM', '01410': 'WM', '01411': 'WM', '01412': 'WM', '01413': 'WM',
                '01501': 'SD', '01502': 'SD', '01503': 'SD', '01504': 'SD', '01505': 'SD', '01506': 'SD'}
        # test_id: app_type
        dict_op = {'001': 'CM', '002': 'CT', '003': 'VZ'}

        dict_loc = {'01004': 'south35', '01005': 'south35', '01006': 'south35', '01007': 'south35',
                '01008': 'south35', '01009': 'south35', '01010': 'south35', '01011': 'south35', '01101': 'south35',
                '01102': 'south35', '01103': 'south35', '01104': 'south35', '01105': 'south35', '01106': 'south35',
                '01201': 'library', '01202': 'library', '01203': 'library',
                '01204': 'library', '01205': 'library', '01206': 'library',
                '01207': 'library', '01208': 'library', '01209': 'library',
                '01303': 'library', '01304': 'library', '01305': 'library',
                '01306': 'library', '01307': 'library', '01308': 'library',
                '01309': 'building1', '01310': 'building1', '01311': 'building1',
                '01312': 'building1', '01313': 'building1', '01314': 'building1',
                '01315': 'building1', '01316': 'building1',
                '01401': 'FuDi', '01402': 'FuDi', '01403': 'FuDi', '01404': 'FuDi', '01405': 'FuDi', '01406': 'FuDi',
                '01407': 'FuDi', '01408': 'FuDi', '01409': 'FuDi', '01410': 'FuDi', '01411': 'FuDi', '01412': 'FuDi', '01413': 'FuDi',
                '01501': 'mall', '01502': 'mall', '01503': 'mall', '01504': 'mall', '01505': 'mall', '01506': 'mall'}

        dict_floor = {'01004': '8', '01005': '6', '01006': '4', '01007': '2',
                '01008': '10', '01009': '8', '01010': '6', '01011': '4', '01101': '2',
                '01102': '10', '01103': '8', '01104': '6', '01105': '4', '01106': '2',
                '01201': '2', '01202': '2', '01203': '2',
                '01204': '3', '01205': '3', '01206': '3',
                '01207': '4', '01208': '4', '01209': '4',
                '01303': '5', '01304': '5', '01305': '5',
                '01306': '6', '01307': '6', '01308': '6',
                '01309': '1', '01310': '1', '01311': '1',
                '01312': '2', '01313': '2', '01314': '2',
                '01315': '4', '01316': '4',
                '01401': '29', '01402': '29', '01403': '28', '01404': '26', '01405': '24', '01406': '22',
                '01407': '20', '01408': '17', '01409': '14', '01410': '13', '01411': '8', '01412': '5', '01413': '2',
                '01501': '1', '01502': '2', '01503': '4', '01504': '4', '01505': '3', '01506': '2'}
        dict_long = {'south35': '118.795638', 'library': '118.795649', 'building1': '118.790993', 'FuDi': '118.804518', 'mall': '118.820176'}
        dict_lat = {'south35': '31.935125', 'library': '31.938166', 'building1': '31.937465', 'FuDi': '31.982458', 'mall': '31.929911'}
        for f in fl:
            loc = f.find('App_Type')
            if loc < 0:
                # pass other file(summary and others)
                continue
            old_name = f
            test_id = old_name.split('Test_id_')[1].split('_Pack_Time')[0]
            app_type = old_name.split('App_Type_')[1].split('UE_Type')[0]
            operator = old_name.split('.')[0].split('Operator_')[1]

            print(test_id)
            # new_name = old_name.replace(app_type, dict_app[test_id])
            # new_name = new_name.replace(operator, dict_op[operator])
            # tmp = list(old_name)
            # loc = f.find('App_Type_') + len('App_Type_')
            # tmp[loc: loc + 3] = dict_app[test_id] + '_'
            # loc = f.find('Operator_') + len('Operator_')
            # tmp[loc: loc + 3] = dict_op[operator] + '_'
            # new_name = ''.join(tmp)

            # print('old:', old_name, '\nnew:', new_name)
            # os.rename(os.path.join(file_dir, old_name), os.path.join(file_dir, new_name))
            # print(old_name, "has been renamed successfully! New name is: ", new_name)  # 输出提示

            df = pd.read_csv(file_dir + f)
            # app type is wrong, need to rewrite app_type and change the filename
            # df['App_Type'] = dict_app[test_id]
            # df['Operator'] = dict_op[operator]
            df['loc'] = dict_loc[test_id] + ' F' + dict_floor[test_id]
            # df['floor'] = dict_floor[test_id]
            df['long'] = dict_long[dict_loc[test_id]]
            df['lat'] = dict_lat[dict_loc[test_id]]
            df.to_csv(out_dir + f, index=False)

    def merge_server_log_file(self):
        # merge all server logs into one file
        fl = self.u.get_file_list(self.server_log_dir)
        print(fl)
        # column_list = ['UE_ID', 'Pack_index', 'UE_Type', 'Operator', 'App_Type', 'Sleep_Timer', 'CSQ', 'Earfcn', 'Pci',
        #                'Cell_Id', 'ECL', 'RSRQ', 'RSRP', 'SNR', 'Temperature', 'Humidity', 'V_Bat', 'UBHV', 'UMHV',
        #                'MSV', 'ERROR_CODE', 'Test_ID', 'Pack Len', 'Pack Timer', 'msg1_rtx', 'msg3_rtx',
        #                'tx_energy', 'ul_tx_energy', 'active_energy', 'loc',	'long', 'lat']
        df_all = pd.DataFrame()

        for f in fl:
            if f in ['log_summary.csv', 'result.csv']:
                continue
            df = pd.read_csv(self.server_log_dir + f, delimiter=',', index_col=False, low_memory=False)
            df_all = df_all.append(df, ignore_index=True, sort=True)
        rename_dict = {'UE_ID': 'node_id',
                       'Pack_index': 'packet_index',
                       'UE_Type': 'module',
                       'Operator': 'op',
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
                       'Pack Timer': 'packet_timestamp',
                       'loc': 'location'}

        df_all = df_all.drop(columns=['msg1_rtx', 'msg3_rtx', 'tx_energy', 'ul_tx_energy', 'active_energy'])
        df_all = df_all.rename(columns=rename_dict)
        columns = ['node_id','test_id','packet_index','csq','rsrp','snr','ecl','earfcn','pci','cell_id','rsrq','module',
                   'packet_timestamp','temperature','rh','v_batt','ubhv','umhv','msv','err_code','sleep_timer',
                   'packet_len','location','lat','long','app','op']
        df_all.to_csv(self.output_dir + 'csv_to_be_merged/' + 'merged_server_log_cn.csv', index=False, header=True, columns=columns)
        # df_all.to_csv(self.server_log_summary, sep=',', columns=write_columns, index=False)

    # 然后创建一个新的CSV，每个设备的每个testID形成新的一行。每一行需要有以下项目：
    def get_field_test_info(self):
        columns = ['UE ID', 'Test ID', 'assigned total packet', 'received number of packet', 'packet delivery rate',
                   'app type', 'operator', 'sleep timer', 'Latitude', 'Longitude',
                   'csq mean', 'csq std', 'csq min', 'csq max',
                   'is earfcn changed', 'is pci changed', 'is cell_id changed',
                   'number of distinct EARFCN', 'number of distinct PCI', 'number of distinct CellID',
                   'ECL0 count', 'ECL1 count', 'ECL2 count',
                   'Extra MSG1 retransmission', 'Extra MSG3 retransmission',
                   'RSRP mean', 'RSRP std', 'RSRP min', 'RSRP max',
                   'SNR mean', 'SNR std', 'SNR min', 'SNR max',
                   'count of ERROR_CODE != 00',
                   'Task duration',
                   'UL tx energy mean', 'UL tx energy std', 'UL tx energy min', 'UL tx energy max',
                   'active energy mean', 'active energy std', 'active energy min', 'active energy max',
                   'packet energy mean', 'packet energy std', 'packet energy min', 'packet energy max']

        result_df = pd.DataFrame(columns=columns)
        dict_line = dict(zip(columns, [0] * len(columns)))
        df_0 = pd.read_csv(self.server_log_summary)
        # df_all = df_0.dropna(axis=0, subset=['csq', 'rsrp', 'snr', 'ecl', 'earfcn', 'pci', 'cell_id', 'rsrq', 'i_max',
        #                                      'i_min', 'e_tx', 'e_active', 'e_packet'])


        for (ue_id, test_id), group in df_0.groupby(['node_id', 'test_id']):

            # print(ue_id, test_id)
            assigned_total_pack = 20
            df = group[group['packet_index'] <= assigned_total_pack]
            received_num_pack = len(df['packet_index'].unique())

            # server may receive same packet twice(with same ue_id , packet_id, test_id), might be retransmission
            pack_delivery_rate = len(df['packet_index'].unique()) / assigned_total_pack
            dict_line['UE ID'] = ue_id
            dict_line['Test ID'] = test_id
            dict_line['assigned total packet'] = assigned_total_pack
            dict_line['received number of packet'] = received_num_pack
            dict_line['packet delivery rate'] = pack_delivery_rate
            dict_line['app type'] = group.iloc[0]['app']
            print(ue_id, test_id, group.iloc[0]['app'])
            dict_line['operator'] = group.iloc[0]['operator']
            dict_line['sleep timer'] = group.iloc[0]['sleep_timer']

            if received_num_pack == 0:
                result_df = result_df.append(dict_line, ignore_index=True)
                continue

            dict_line['csq mean'] = np.mean(df['csq'])
            dict_line['csq std'] = np.std(df['csq'])
            dict_line['csq max'] = max(df['csq'])
            dict_line['csq min'] = min(df['csq'])

            if len(df['earfcn'].unique()) > 1:
                dict_line['is earfcn changed'] = 1
                dict_line['number of distinct EARFCN'] = len(df['earfcn'].unique())
            if len(df['pci'].unique()) > 1:
                dict_line['is pci changed'] = 1
                dict_line['number of distinct PCI'] = len(df['pci'].unique())
            if len(df['cell_id'].unique()) > 1:
                dict_line['is cell_id changed'] =1
                dict_line['number of distinct CellID'] = len(df['cell_id'].unique())

            dict_line['ECL0 count'] = len(df[df['ecl'] == '0'])
            dict_line['ECL1 count'] = len(df[df['ecl'] == '1'])
            dict_line['ECL2 count'] = len(df[df['ecl'] == '2'])

            dict_line['RSRP mean'] = np.mean(df['rsrp'])
            dict_line['RSRP std'] = np.std(df['rsrp'])
            dict_line['RSRP min'] = min(df['rsrp'])
            dict_line['RSRP max'] = max(df['rsrp'])

            dict_line['SNR mean'] = np.mean(df['snr'])
            dict_line['SNR std'] = np.std(df['snr'])
            dict_line['SNR min'] = min(df['snr'])
            dict_line['SNR max'] = max(df['snr'])

            dict_line['count of ERROR_CODE != 00'] = len(df[df['err_code'] != 0])
            # start_time = datetime.datetime.strptime(df.iloc[0]['Pack Timer'], '_%Y%m%d_%H%M_%S')
            # tmp = df[df['pack_index'] <= 20]
            # end_time = datetime.datetime.strptime(tmp.iloc[-1]['Pack Timer'], '_%Y%m%d_%H%M_%S')
            # dict_line['Task duration'] = end_time - start_time

            dict_line['UL tx energy mean'] = np.mean(df['e_tx'])
            dict_line['UL tx energy std'] = np.std(df['e_tx'])
            dict_line['UL tx energy min'] = np.min(df['e_tx'])
            dict_line['UL tx energy max'] = np.max(df['e_tx'])

            dict_line['active energy mean'] = np.mean(df['e_active'])
            dict_line['active energy std'] = np.std(df['e_active'])
            dict_line['active energy min'] = np.min(df['e_active'])
            dict_line['active energy max'] = np.max(df['e_active'])

            dict_line['packet energy mean'] = np.mean(df['e_packet'])
            dict_line['packet energy std'] = np.std(df['e_packet'])
            dict_line['packet energy min'] = np.min(df['e_packet'])
            dict_line['packet energy max'] = np.max(df['e_packet'])

            result_df = result_df.append(dict_line, ignore_index=True)
        print(result_df)
        dict_rename = {'UE ID': 'node_id', 'Test ID': 'test_id', 'assigned total packet': 'packet_total',
                       'received number of packet': 'packet_receive', 'packet delivery rate': 'delivery_rate',
                   'app type': 'app', 'operator': 'op', 'sleep timer': 'sleep_timer', 'Latitude': 'lat', 'Longitude': 'long',
                   'csq mean': 'csq_mean', 'csq std': 'csq_std', 'csq min': 'csq_min', 'csq max': 'csq_max',
                   'is earfcn changed': 'earfcn_change', 'is pci changed': 'pci_change', 'is cell_id changed': 'cell_id_change',
                   'number of distinct EARFCN': 'earfcn_num', 'number of distinct PCI': 'pci_num', 'number of distinct CellID': 'cell_id_num',
                   'ECL0 count': 'ecl0_count', 'ECL1 count': 'ecl1_count', 'ECL2 count': 'ecl2_count',
                   'Extra MSG1 retransmission': 'extra_msg1_rtx', 'Extra MSG3 retransmission': 'extra_msg3_rtx',
                   'RSRP mean': 'rsrp_mean', 'RSRP std': 'rsrp_std', 'RSRP min': 'rsrp_min', 'RSRP max': 'rsrp_max',
                   'SNR mean': 'snr_mean', 'SNR std': 'snr_std', 'SNR min': 'snr_min', 'SNR max': 'snr_max',
                   'count of ERROR_CODE != 00': 'count_error_code_not_00',
                   'Task duration': 'task_duration',
                   'UL tx energy mean': 'e_tx_mean', 'UL tx energy std': 'e_tx_std', 'UL tx energy min': 'e_tx_min', 'UL tx energy max': 'e_tx_max',
                   'active energy mean': 'e_active_mean', 'active energy std': 'e_active_std', 'active energy min': 'e_active_min', 'active energy max': 'e_active_max',
                   'packet energy mean': 'e_packet_mean', 'packet energy std': 'e_packet_std', 'packet energy min': 'e_packet_min', 'packet energy max': 'e_packet_max'}
        result_df = result_df.rename(columns=dict_rename)
        result_df.to_csv(self.output_dir + 'new_field_test_info.csv', index=False)

    def get_field_test_meta_info(self):
        fl = self.u.get_file_list(self.server_log_dir)
        df_meta = pd.read_csv(self.csv_to_be_merged + 'field_test_meta_info_cn.csv')
        df_server = pd.DataFrame(columns=['node_id', 'test_id', 'date', 'start_time', 'app', 'op', 'assigned_total_packet'])
        for f in fl:
            # _UE_ID_C01_Test_id_01005_Pack_Time__20200111_1623_50App_Type_WM_UE_Type_009_Operator_CT_
            result = re.search(
                'UE_ID_(\D\d+)_Test_id_(\d+)_Pack_Time__(\d+)_(\d+)_(\d+)App_Type_(\D+)_UE_Type_(\d+)_Operator_(\D+)_.csv',
                f)

            line = {'node_id': result[1],
                    'test_id': result[2],
                    'date': result[3][4:],
                    'start_time': result[4][0:2]+':'+result[4][2:],
                    'app': result[6],
                    'op': result[8],
                    'assigned_total_packet': 20
                    }

            df_server = df_server.append(line, ignore_index=True)
        df_server['test_id'] = df_server.test_id.astype(int)

        df_server_2 = df_server[df_server.test_id.isin(df_meta.test_id.unique())]
        print(df_server_2)

        new_df = pd.merge(df_server_2, df_meta, how='inner', on=['node_id', 'test_id'])
        print(new_df)
        new_df.to_csv(self.csv_to_be_merged + 'field_test_meta_info_cn_2.csv', sep=',', index=None, header=True)


if __name__ == '__main__':
    whoami = 'ls'
    slp = ServerLogProcessor(whoami)
    # slp.merge_server_log_file()
    out_dir = 'D:\\Nutstore\\我的坚果云\\Field Test\\STM32 Node Deployment\\\Sigcomm2020_fied_test_server_logs/'
    file_dir = 'C:\\Users\\lenovo\\Desktop\\copy_0210_Sigcomm2020_fied_test_server_logs/'
    # slp.add_column(file_dir, out_dir)
    # slp.merge_server_log_file()
    slp.get_field_test_info()
    # slp.get_field_test_meta_info()