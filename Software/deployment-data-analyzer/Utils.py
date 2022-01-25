import csv
import json
import os
import platform
import shutil
from pathlib import Path

WARN = '\033[93m[WARN]\033[00m'
INFO = '\033[92m[INFO]\033[00m'
ERR = '\033[91m[ERR]\033[00m'
DBG = '\033[94m[DBG]\033[00m'


class Utils(object):
    def __init__(self):
        self.determine_platform()

    def determine_platform(self):
        self.log_in = os.getlogin()
        self.hostname = platform.node()
        self.os = platform.system()

    def get_file_list(self, file_path):
        # This one gets all the files
        files = []
        for root, dirs, files in os.walk(file_path):
            # print('# of files: {0}'.format(len(files)))
            pass
        file_list = files
        return file_list

    def load_config(self, config_path):
        f_config = open(config_path, 'rb')

        conf_dict = json.load(f_config)
        # print(INFO, 'Config Dictionary', conf_dict)
        return conf_dict

    def load_csv_to_list(self, full_path):
        res = []
        with open(full_path, 'r') as f_csv:
            rd = csv.reader(f_csv, delimiter=',')
            for row in rd:
                res.append(row)
        return res

    def get_csv_output_dir_from_path(self, fp):
        '''
        For us region logs only
        Input example: '/Users/dlyang/Nutstore Files/NutstoreX/Field Test/STM32 Node Deployment - US/Current/A01/01201/A01_I_01201_0001.log'
        Output: 'A01/01201/A01_I_01201_0001'
        '''
        if type(fp) != str:
            print(ERR, 'Invalid input type')
            return
        fp_temp = fp.split('/')[-1]  # 'A01_I_01201_0001.log'
        fn = fp_temp.split('.')[0]  # log to csv
        fn_list = fn.split('_')
        return '/'.join([fn_list[0], fn_list[2], fn])

    def get_filename_from_path(self, fp):
        '''
        Note: not very robust, do not send strange input here.
        fp: (1) absolute path, '/Users/dlyang/Nutstore Files/NutstoreX/Field Test/STM32 Node Deployment - US/Current/A01/01201/A01_I_01201_0001.log'
        (2) file name only: 'A01_I_01201_0001' (without the extension)
        Output: 'A01_I_01201_0001'
        '''
        if type(fp) != str:
            print(ERR, 'Invalid input type')
            return 'N/A'

        if '/' not in fp:
            # filename only
            if '.' in fp:
                fp = fp.split('.')[0]
            return fp

        # absolute path
        fp_temp = fp.split('/')[-1]
        fn = fp_temp.split('.')[0]  # log to csv
        return fn

    def get_info_from_filename(self, fn):
        '''
        Input can only be fileneme: 'A01_I_01201_0001' (without the extension)
        Output: node_id, test_id, packet_id
        '''
        fn_list = fn.split('_')
        return fn_list[0], fn_list[2], fn_list[3]

    def find_consecutive_range(self, idx_list):
        '''
        Input: [1,2,3,4,6,7,8,9,11,13,14,15,16,23,24,25]
        Return: [[1,4], [6,9], [13,16], [23,25]]
        '''
        if idx_list is None:
            return None
        ret_list = []
        con_flag = False
        i = 0
        start = 0
        while i < len(idx_list):
            for j in range(i + 1, len(idx_list)):
                if idx_list[j] - idx_list[j - 1] == 1:
                    if con_flag == False:
                        start = j - 1
                    con_flag = True
                else:
                    if con_flag:
                        ret_list.append([idx_list[start], idx_list[j - 1]])
                    con_flag = False
                    i = j  # update i
                    break
            i += 1
        # final range
        if con_flag:
            ret_list.append([idx_list[start], idx_list[-1]])

        return ret_list

    def find_different_set_csv_png(self, csv_fp_list, png_fp_list):
        '''
        Find the files that are not processed.
        = Find the element of 1st list that are not in 2nd list
        csv_fp_list: list of current files (csv format)
        png_fp_list: list of output fig files (png format)
        Note: each element in the list is a full absolute path
        '''
        csv_fn_list = [x.split('/')[-1].split('.')[0] for x in csv_fp_list]
        png_fn_list = [x.split('/')[-1].split('.')[0] for x in png_fp_list]
        csv_fn_set = set(csv_fn_list)
        processed_idx_list = []
        for pfn in png_fn_list:
            if pfn in csv_fn_set:
                processed_idx_list.append(csv_fn_list.index(pfn))
        all_index_set = set(range(len(csv_fn_list)))
        untouched_idx_set = all_index_set - set(processed_idx_list)
        untouched_idx_list = list(untouched_idx_set)
        untouched_idx_list.sort()
        csv_untouched_list = []
        for idx in untouched_idx_list:
            csv_untouched_list.append(csv_fp_list[idx])
        return csv_untouched_list

    def load_path_or_names_to_list(self, f_name):
        '''f_name: absolute path'''
        fn_list = []
        with open(f_name, 'r') as ff:
            for l in ff:
                fn = l.split('\n')[0]
                if fn:
                    fn_list.append(fn)
            ff.close()
        return fn_list

    def move_files_to_subfolder_by_name(self, folder_path, sub_f_name, fn_list, ext=None):
        """
        folder path: absolute path
        ext: 'png', 'csv' .etc. No dot needed
        Make sure the subfolder is not exist yet!.
        """
        candidates = self.get_file_list(folder_path)
        if ext is not None:
            fn_list = ['{0}.{1}'.format(x, ext) for x in fn_list]  # append file extension
        fn_set = set(fn_list)
        subf_dir = folder_path + sub_f_name + '/'

        print(len(candidates), candidates[:5])
        print(len(fn_list), fn_list[:5])
        # return

        fc = 0
        Path(subf_dir).mkdir(parents=True, exist_ok=True)
        for ff in candidates:
            if ff in fn_set:
                shutil.move(folder_path+ff, subf_dir+ff)
                fc += 1
        print(INFO, 'Moved file count: {0}'.format(fc))

    def append_src_to_dst_csv(self, src_df, dst_df):
        '''PLEASE use absolute path in both path'''
