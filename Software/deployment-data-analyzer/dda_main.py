from RawLogProcessor import RawLogProcessor
from DeploymentDataProcessor import DeploymentDataProcessor
from DataVisualizer import DataVisualizer
import time
import os


whoami = 'ls'  # 'ls', 'xh'


def stage_1(cmd, one_file_name=''):
    # From raw signal flow to decoded message list, stored in PKL file.
    print('<Stage 1> Raw => Decoded message list.')
    device_name = 'BC28'
    filter_out_list = {'N/A', 'UICC_DBG_LOG_P0', 'UICC_DBG_LOG_P1', 'UICC_DBG_LOG_P2'}  # add item to only one of them!!! E.g. to remove invalid message, use 'N/A'.
    filter_in_list = {}  # add item to only one of them!!!
    filter_dict = {'FO': filter_out_list, 'FI': filter_in_list}

    rlp = RawLogProcessor(device_name, filter_dict)
    if cmd == 'print':
        print(rlp.generate_raw_log_list())
    elif cmd == 'one':
        # fp = '/Users/dlyang/Nutstore Files/NutstoreX/Field Test/STM32 Node Deployment/Beijing/北邮/F1.txt'
        fp = 'D:/Nutstore/我的坚果云/Field Test/STM32 Node Deployment/STM32 SDIO/Lab_Test_1/Node.txt'    # ue type='BC35'
        # fp = one_file_name
        print(fp)
        rlp.decode_one_file(fp)
    elif cmd == 'all':
        rootpath = 'D:/Nutstore/我的坚果云/Field Test/STM32 Node Deployment - SZ/Current/D09/'
        flist = []
        for root, dirs, files in os.walk(rootpath):
            if len(files)!=0:
                for f in files:
                    if f.split('_')[1] == 'D':
                        flist.append(root+f)
        # print(len(flist), flist)
        rlp.pipeline_from_raw_to_csv(flist)
    elif cmd == 'meta':
        # amarisoft
        rlp.generate_meta_csv()


def stage_2(cmd, one_file_name):
    # Input from PKL, process and output the results.
    print('<Stage 2> Message list => Extracted info')
    ddp = DeploymentDataProcessor(whoami)
    if cmd == 'print':
        print(ddp.get_decoded_log_names())
    if cmd == 'one':
        ml = ddp.load_pickle_file(ddp.pkl_dir+one_file_name)
        print(ml[0])
        # ddp.extract_rsrp_snr_ecl(ddp.pkl_dir + one_file_name)
        # ddp.get_rsrp_snr_ecl_list(ml)
    if cmd == 'test':
        ml = ddp.load_pickle_file(ddp.pkl_dir+one_file_name)
        log_name = 'LL1_RAR_UL_GRANT'
        log_name = 'LL1_PUSCH_CALC_TX_POWER'
        log_name = 'LL1_LOG_ECL_INFO'
        log_name = 'EMM_PSM_STATUS_IND'
        ddp.take_out_specific_logs_from_msg_list(ml, log_name, 'visualize_seq_num/实验楼2F_消防栓/')

    if cmd == 'ecl':
        ddp.extract_rsrp_snr_ecl(ddp.pkl_dir+one_file_name)
    if cmd == 'stat':
        ddp.msg_list_stats(ddp.pkl_dir+one_file_name)
    if cmd == 'dci':
        ddp.extract_dci(ddp.pkl_dir + one_file_name)
    if cmd == 'rar':
        ddp.extract_msg3_repetition(ddp.pkl_dir + one_file_name)
    if cmd == 'all':
        '''
        Note1: remember to change the function in pipeline_process_all()
        Note2: select between the two file lists below. They are different.
        '''
        file_list = ddp.get_decoded_log_names()
        # file_list = ddp.get_rse_csv_names()
        # file_list = ddp.get_bler_report_csv_names()
        ddp.pipeline_process_all(file_list)

def stage_3(flag):
    print('<Stage 3> Aggregate Extracted Info')
    ddp = DeploymentDataProcessor(whoami)
    if flag == 'ecl':
        csv_dir = ddp.rse_csv_output_dir
    elif flag == 'rar':
        csv_dir = ddp.rar_csv_dir
    elif flag == 'dci':
        csv_dir = ddp.dci_csv_dir
    elif flag == 'nrs':
        csv_dir = ddp.rse_csv_output_dir
    ddp.aggregate_extracted_info_to_csv(flag, csv_dir)

def stage_4(flag):
    # merge the sum output data with meta csv
    print('<Stage 4> Merge with meta data to post_ft_processing')
    ddp = DeploymentDataProcessor(whoami)
    if flag == 1:
        ddp.merge_msg3_data_rep_with_meta()


if __name__ == '__main__':
    start_time = time.time()
    # stage_1('all', '')
    # stage_2('all', '')
    # stage_3('rar')
    stage_1('all', '')
    print('Total execution time: {0:.4f} s'.format(time.time()-start_time))

