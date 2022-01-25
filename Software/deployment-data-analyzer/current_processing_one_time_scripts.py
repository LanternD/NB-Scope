import csv
import os

from CurrentLogProcessor import CurrentLogProcessor
from DataVisualizer import DataVisualizer
from Utils import *

nut_path = '/home/dlyang-zmly/NutstoreAll/Nutstore/'

def correct_timestamp_in_filename():
    '''Switch UTC+0 to UTC-5'''
    csv_dir = '/home/dlyang/NutstoreX/Field Test/STM32 Node Deployment - US/Renamed Server Log (T)/'
    u = Utils()
    csv_fn_list = u.get_file_list(csv_dir)
    print(len(csv_fn_list))
    rename_count = 0
    for fn in csv_fn_list:
        fn_buf = fn.split('_')
        if int(fn_buf[1]) < 1899:
            # print(fn)
            date = fn_buf[3]
            timestamp = fn_buf[4]
            h = timestamp[:2]
            if int(h) <= 4:
                new_h = int(h) - 5 + 24
                n_h_s = str(new_h).zfill(2)
                fn_buf[3] = str(int(date) - 1)
            else:
                n_h_s = str(int(h)-5).zfill(2)
            fn_buf[4] = n_h_s + timestamp[2:]
            new_fn = '_'.join(fn_buf)
            print(fn[:28], new_fn[:28])
            rename_count += 1
            os.rename(csv_dir+fn, csv_dir+new_fn)
    print(rename_count)
    return


def scale_field_test_meta():
    '''The logs in evernote has only one line, we need to duplicate them.'''
    nut_path = '/home/dlyang-zmly/NutstoreAll/Nutstore/'
    fp = nut_path + 'Field Test/STM32 Node Deployment - US/'
    fn = 'USA Field Test Meta Info Evernote - Round3.csv'
    fon = 'USA Field Test Meta Info Scaled - Round3.csv'

    f_in = open(fp+fn, 'r')
    f_out = open(fp+fon, 'w')
    cr = csv.reader(f_in)
    cw = csv.writer(f_out)
    for l in cr:
        print(l)
        if l[0] == 'Date':
            cw.writerow(l)
            continue
        if l[8] == '123':
            for app in ['A01', 'A02', 'A03']:
                cw.writerow(l + [app])
        elif l[8] == '456':
            for app in ['A04', 'A05', 'A06']:
                cw.writerow(l + [app])
    f_in.close()
    f_out.flush()
    f_out.close()


def correct_energy_stats_in_batch():

    clp = CurrentLogProcessor(whoami='dy2', region='cndy')
    task_list = []
    with open('/home/dlyang-zmly/Desktop/fn_temp.txt', 'r') as f_t:
        cr = csv.reader(f_t)
        for row in cr:
            task_list.append(row)
        f_t.close()

    for task in task_list:
        fp = task[0]
        th = int(task[1])
        # print(fp[-15:], th)
        df = clp.load_current_data_from_csv(fp)
        stats_dict = clp.calculate_energy_one_df(df, th)

        fn = clp.u.get_filename_from_path(fp)
        if df.node_id[0] == 'C':
            suffix = 'cn'
        elif df.node_id[1] == 'A':
            suffix = 'us'
        else:
            suffix = 'xx'
        clp.export_stats_dict(stats_dict, fn, clp.output_dir + 'packet_energy_stats_{0}_{1}.csv'.format(suffix, fn[:3]))

        local_vis = DataVisualizer('dy2')
        local_vis.plot_current(df, fn, show_flag=False, stats_dict=stats_dict)


def replace_energy_stats_with_new_ones():
    '''Paste the new packet stats at the end of the original ones, and run this function.'''
    csv_path = nut_path + 'Field Test/Deployment Experiment Output/packet_energy_stats/packet_energy_stats_us_A06'
    clp = CurrentLogProcessor(whoami='dy2', region='us')
    df = clp.load_packet_energy_stats_csv(csv_path+'.csv')
    print('Len df before dropping:', len(df))
    df_dup = df.drop_duplicates(subset=['test_id', 'packet_index'], keep='last', inplace=False)
    print('Len df after dropping:', len(df_dup))

    df_dup = df_dup.sort_values(by=['test_id', 'packet_index'])
    # Export to file
    df_dup.to_csv(csv_path+'_1.csv', sep=',', index=None, header=None)  # no header to be consistent


def sort_csv_file():
    fp = '/home/dlyang/NutstoreX/Field Test/Deployment Experiment Output/packet_stats_us_A01.csv'
    clp = CurrentLogProcessor(whoami='dy', region='us')
    df = clp.load_packet_stats_csv(fp)
    df = df.sort_values(by=['node_id', 'test_id', 'packet_index'])
    df.to_csv(fp, sep=',', index=None, header=None)


if __name__ == '__main__':
    # rename_files()
    # scale_field_test_meta()
    # correct_energy_stats_in_batch()
    replace_energy_stats_with_new_ones()
    # sort_csv_file()
