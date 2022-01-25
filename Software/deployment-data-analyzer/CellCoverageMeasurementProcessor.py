from Utils import *
import pickle
import pandas as pd
import csv
import pandas
import numpy as np
from DataVisualizer import DataVisualizer


class CellCoverageMeasurementProcessor(object):

    def __init__(self, whoami):
        self.u = Utils()
        self.config = self.u.load_config('./config.json')

        self.global_path = self.config['env_prefix'][whoami][self.u.os]

        print(INFO, 'Global prefix', self.global_path)

        '''Change the following accordingly.'''
        self.ccm_data_dir = self.global_path + self.config['coverage_measurement_folder_prefix']
        self.covearage_measurement_csv_path = self.ccm_data_dir + 'middle_gps_rsrp_info.csv'

        self.v = DataVisualizer(whoami)

    def location_signal_fusion(self):
        pass

    def load_coverage_data_to_df(self, ph):
        df = pd.read_csv(ph)
        print(DBG, df.columns)
        return df

    def df_preprocessing(self, df):
        '''Remove abnormal data points.'''
        new_df = df[df['rsrp'] != 0]
        new_df['rsrp'] = np.round(new_df['rsrp']/10)
        new_df['rsrp'] = new_df['rsrp'].to_list() + np.abs(np.min(new_df['rsrp']))

        # Do a subsampling to reduce the load of computation.
        new_df = new_df.sample(frac=0.5, replace=False)
        return new_df

    def pipeline(self):
        coverage_df = self.load_coverage_data_to_df(self.covearage_measurement_csv_path)
        coverage_df = self.df_preprocessing(coverage_df)
        print(coverage_df.describe())
        self.v.plot_cell_coverage_contour(coverage_df)
