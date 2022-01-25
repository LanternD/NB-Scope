import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from DataVisualizer import DataVisualizer
from Utils import *


class PostFieldTestProcessor():
    """Statistical analysis of the current and server log data."""

    def __init__(self, whoami):
        self.u = Utils()
        self.config = self.u.load_config("./config.json")
        self.global_path = self.config["env_prefix"][whoami][self.u.os]
        self.output_dir = self.global_path + self.config["output_path"]
        self.pftp_data_dir = self.output_dir + "post_ft_processing/"
        self.merge_dir = self.output_dir + "csv_to_be_merged/"

        # Change to '_1' temporarily
        self.ft_db_csv_fn = self.pftp_data_dir + "field_test_database.csv"
        self.agg_csv_fn = self.pftp_data_dir + "stats_group_by_test.csv"
        self.v = DataVisualizer(whoami)

        self.df_db = None
        self.df_agg = None
        # For region choice
        nj_nodes = {"C" + str(x).zfill(2) for x in list(range(1, 13))}
        sz_nodes = {"D" + str(x).zfill(2) for x in list(range(1, 12))}
        self.cn_node_list = nj_nodes.union(sz_nodes)  # SZ
        self.us_node_list = {"A" + str(x).zfill(2) for x in list(range(1, 7))}
        print(self.cn_node_list)

    def load_csv(self):
        def lmda_assign_region_column(row):
            if row["node_id"] in self.cn_node_list:
                return "cn"
            elif row["node_id"] in self.us_node_list:
                return "us"
            else:
                return "other"

        if Path(self.ft_db_csv_fn).is_file():
            self.df_db = pd.read_csv(self.ft_db_csv_fn)
            self.df_db["region"] = self.df_db.apply(
                lambda row: lmda_assign_region_column(row), axis=1
            )
            print(INFO, "Field test DB DF is loaded.")
        else:
            print(ERR, "Field test DB not exists, please put it in the directory.")

        if Path(self.agg_csv_fn).is_file():
            self.df_agg = pd.read_csv(self.agg_csv_fn)
            self.df_agg["region"] = self.df_agg.apply(
                lambda row: lmda_assign_region_column(row), axis=1
            )
            print(INFO, "Aggregated DF is loaded.")
        else:
            print(ERR, "Aggregated CSV is not generated yet.")

    def calculate_overview_stats(self):
        """Based on df_db and df_agg"""
        print("\nvvvv Stats vvvv")
        if self.df_db is None and self.df_agg is None:
            print(ERR, "DF is not prepared.")
            return 
        print(INFO, "Unique modules: ", self.df_db['module'].unique())
        print(
            INFO, "# US region packet:", len(self.df_db[self.df_db["region"] == "us"])
        )
        print(
            INFO, "# CN region packet:", len(self.df_db[self.df_db["region"] == "cn"])
        )
        print(
            INFO, "# US region test:", len(self.df_agg[self.df_agg["region"] == "us"])
        )
        print(
            INFO, "# CN region test:", len(self.df_agg[self.df_agg["region"] == "cn"])
        )
        print(
            INFO,
            "# US unique locations: ",
            len(self.df_db[self.df_db["region"] == "us"]["location"].unique()),
        )
        print(
            INFO,
            "# CN unique locations: ",
            len(self.df_db[self.df_db["region"] == "cn"]["location"].unique()),
        )
        print(INFO, "Unique app:", self.df_agg["app"].unique())

        # Energy basics:
        # print(INFO, 'Energy max:min ratio:')
        # for (node_id, app), subgroup in self.df_agg.groupby(['node_id', 'app']):
        #     print(node_id, app, max(subgroup['e_active_max'])/min(subgroup['e_active_min']))

        df_eb = self.df_db[
            (self.df_db["long"] < -84.4795)
            & (self.df_db["long"] > -84.4820)
            & (self.df_db.lat > 42.7237)
            & (self.df_db.lat < 42.726)
        ]
        print(INFO, "EB cells", df_eb["cell_id"].unique())
        print("^^^^ Stats ^^^^\n")

    def calculate_mean_std_min_max(self, row_dict, df_db, column_name):
        if column_name == "snr":
            df_db = df_db[(df_db["snr"] != -127) | (df_db["snr"] != 99)]
        if column_name == "csq":
            df_db = df_db[df_db["csq"] != 99]

        df_db[column_name] = df_db[column_name].astype("float")

        row_dict[column_name + "_mean"] = np.mean(df_db[column_name])
        row_dict[column_name + "_std"] = np.std(df_db[column_name])
        row_dict[column_name + "_max"] = max(df_db[column_name])
        row_dict[column_name + "_min"] = min(df_db[column_name])

        return row_dict

    def get_field_test_stats(self):
        columns = [
            "node_id",
            "test_id",
            "packet_total",
            "packet_receive",
            "delivery_rate",
            "app",
            "op",
            "sleep_timer",
            "lat",
            "long",
            "csq_mean",
            "csq_std",
            "csq_min",
            "csq_max",
            "is_earfcn_changed",
            "is_pci_changed",
            "is_cell_id_changed",
            "distinct_earfcn_num",
            "distinct_pci_num",
            "distinct_cell_id_num",
            "ecl0_count",
            "ecl1_count",
            "ecl2_count",
            "extra_msg1_retx",
            "extra_msg3_retx",
            "rsrp_mean",
            "rsrp_std",
            "rsrp_min",
            "rsrp_max",
            "snr_mean",
            "snr_std",
            "snr_min",
            "snr_max",
            "error_code_not_00_count",
            "task_duration",
            "e_tx_mean",
            "e_tx_std",
            "e_tx_min",
            "e_tx_max",
            "e_active_mean",
            "e_active_std",
            "e_active_min",
            "e_active_max",
            "e_packet_mean",
            "e_packet_std",
            "e_packet_min",
            "e_packet_max",
        ]

        result_df = pd.DataFrame(columns=columns)
        dict_line = dict(zip(columns, [0] * len(columns)))

        df_0 = pd.read_csv(self.ft_db_csv_fn)
        df_all = df_0.dropna(
            axis=0,
            subset=[
                "csq",
                "rsrp",
                "snr",
                "ecl",
                "earfcn",
                "pci",
                "cell_id",
                "rsrq",
                "i_max",
                "i_min",
                "e_tx",
                "e_active",
                "e_packet",
            ],
        )

        location_count = {'US': 0, 'SZ': 0, 'NJ': 0}
        for (ue_id, test_id), group in df_all.groupby(["node_id", "test_id"]):
            # print(ue_id, test_id)

            # Count unique loctions
            if 'A' in ue_id:
                location_count['US'] += 1
            elif 'C' in ue_id:
                location_count['NJ'] += 1
            elif 'D' in ue_id:
                location_count['SZ'] += 1

            assigned_total_pack = 20  # default
            if max(group["packet_index"]) > 28:
                assigned_total_pack = 30
            if max(group["packet_index"]) > 100:
                assigned_total_pack = max(group["packet_index"])
            df = group[group["packet_index"] <= assigned_total_pack]
            received_num_pack = len(df["packet_index"].unique())

            # server may receive same packet twice(with same ue_id , packet_id, test_id), might be retransmission
            if ue_id in ["C05", "C06", "C07", "C08"]:
                pack_delivery_rate = len(df["packet_index"].unique()) / (
                    assigned_total_pack / 2
                )
            else:
                pack_delivery_rate = (
                    len(df["packet_index"].unique()) / assigned_total_pack
                )
            dict_line["node_id"] = ue_id
            dict_line["test_id"] = test_id
            dict_line["lat"] = group.iloc[0]["lat"]
            dict_line["long"] = group.iloc[0]["long"]
            dict_line["packet_total"] = assigned_total_pack
            dict_line["packet_receive"] = received_num_pack
            dict_line["delivery_rate"] = pack_delivery_rate
            dict_line["app"] = group.iloc[0]["app"]
            # print(ue_id, test_id, group.iloc[0]['app'])
            dict_line["operator"] = group.iloc[0]["operator"]
            dict_line["sleep_timer"] = group.iloc[0]["sleep_timer"]

            if received_num_pack == 0:
                result_df = result_df.append(dict_line, ignore_index=True)
                continue

            dict_line = self.calculate_mean_std_min_max(dict_line, df, "csq")

            if len(df["earfcn"].unique()) > 1:
                dict_line["is_earfcn_changed"] = 1
                dict_line["distinct_earfcn_num"] = len(df["earfcn"].unique())
            if len(df["pci"].unique()) > 1:
                dict_line["is_pci_changed"] = 1
                dict_line["distinct_pci_num"] = len(df["pci"].unique())
            if len(df["cell_id"].unique()) > 1:
                dict_line["is_cell_id_changed"] = 1
                dict_line["distinct_cell_id_num"] = len(df["cell_id"].unique())

            # df['ecl'] = df['ecl'].astype('int')

            dict_line["ecl0_count"] = len(df[(df["ecl"] == 0) | (df["ecl"] == "0")])
            dict_line["ecl1_count"] = len(df[(df["ecl"] == 1) | (df["ecl"] == "1")])
            dict_line["ecl2_count"] = len(df[(df["ecl"] == 2) | (df["ecl"] == "2")])

            dict_line = self.calculate_mean_std_min_max(dict_line, df, "rsrp")
            dict_line = self.calculate_mean_std_min_max(dict_line, df, "snr")

            dict_line["error_code_not_00_count"] = len(df[df["err_code"] != 0])

            # Only calculate the time to send 20 packet for fair comparison
            try:
                start_time = datetime.datetime.strptime(
                    df.iloc[0]["packet_timestamp"], "_%Y%m%d_%H%M_%S"
                )
                tfmt = "_%Y%m%d_%H%M_%S"
            except ValueError:
                start_time = datetime.datetime.strptime(
                    df.iloc[0]["packet_timestamp"], "%Y%m%d_%H%M%S"
                )
                tfmt = "%Y%m%d_%H%M%S"

            tmp = df[df["packet_index"] <= 20]
            try:
                end_time = datetime.datetime.strptime(
                    tmp.iloc[-1]["packet_timestamp"], tfmt
                )
            except IndexError:
                print(ERR, df)
                end_time = start_time

            dict_line["task_duration"] = end_time - start_time

            dict_line = self.calculate_mean_std_min_max(dict_line, df, "e_tx")
            dict_line = self.calculate_mean_std_min_max(dict_line, df, "e_active")
            dict_line = self.calculate_mean_std_min_max(dict_line, df, "e_packet")

            result_df = result_df.append(dict_line, ignore_index=True)
        print(result_df)
        print(INFO, "Unique location count:", location_count)
        result_df.to_csv(self.pftp_data_dir + "stats_group_by_test.csv", index=False)

    def get_outdoor_df(self):
        df = pd.read_csv(self.agg_csv_fn)
        outdoor_app = ["OP"]  # outdoor parking
        df_outdoor = df[df["app"].isin(outdoor_app)]
        return df_outdoor

    def get_indoor_df(self):
        df = self.df_agg.copy()  # pd.read_csv(self.agg_csv_fn)
        # df = pd.read_csv('E:/cell_id_stats.csv')
        indoor_app = [
            "WM",
            "SD",
            "SL",
            "IP",
        ]  # water meter, smoke detection, smart lock, indoor parking
        df_indoor = df[df["app"].isin(indoor_app)]
        return df_indoor

    def visualize_packet_energy_outdoor_map(self, region):
        df_outdoor = self.get_outdoor_df()
        if region == "us":
            df_outdoor = df_outdoor[df_outdoor["node_id"].isin(self.us_node_list)]
        elif region == "cn":
            df_outdoor = df_outdoor[df_outdoor["node_id"].isin(self.cn_node_list)]
        self.v.plot_packet_energy_map(df_outdoor)

    def visualize_packet_energy_indoor_map(self, region):
        df_indoor = self.get_indoor_df()

        print(INFO, df_indoor)
        if region == "us":
            df_indoor = df_indoor[df_indoor["node_id"].isin(self.us_node_list)]
        elif region == "cn":
            df_indoor = df_indoor[df_indoor["node_id"].isin(self.cn_node_list)]
        # self.v.plot_packet_energy_map(df_indoor)
        # df_2 = df_indoor.sort_index(by=['e_packet_mean'])
        self.v.test_plot_map_indoor(df_indoor)

    def visualize_energy_vs_app(self, energy_type="e_active_mean"):
        if "mean" in energy_type:
            passed_df = self.df_agg
            if energy_type == "e_active_mean":
                passed_df[energy_type] /= 1000
        else:
            passed_df = self.df_db

        # Do whatever process here.
        passed_df = passed_df[passed_df[energy_type] >= 0.3]
        passed_df = passed_df[passed_df[energy_type] < 15]
        #Exclude two tests with antenna installation issues in SZ
        passed_df = passed_df[(passed_df['test_id'] != 22109) & (passed_df['test_id'] != 21702)]

        print(INFO, "outlier in SD", passed_df[passed_df[energy_type] > 5000])

        self.v.plot_energy_vs_location_pf(passed_df, energy_type, "energy_by_app_op.pdf")

    def visualize_energy_vs_app_bc26_bc66(self, energy_type='e_active_mean'):
        if "mean" in energy_type:
            passed_df = self.df_agg
            if energy_type == "e_active_mean":
                passed_df[energy_type] /= 1000
        else:
            passed_df = self.df_db
        node_id_list = ['A03', 'A06', 'C09', 'C10', 'C11', 'C12', 'D01', 'D02', 'D07', 'D08']

        df = self.df_agg[self.df_agg['node_id'].isin(node_id_list)]

        filtered_test = [22109, 21702, 22114, 21803, 22110, 22111, 22112]
        df = df[~df['test_id'].isin(filtered_test)]
        # df = df[~((df['app']=='OP') & (df[energy_type] >= 4))]
        # df = df[df['app'] == 'OP']
        df = df[df[energy_type] >= 0.3]
        df = df[df[energy_type] < 15]
        df.to_csv('~/Desktop/bc26_bc66.csv')
        self.v.plot_energy_vs_location_pf(df, energy_type, "energy_by_app_op_bc26_bc66.pdf")

    def visualize_ecl_distribution_by_app(self, version):

        # op_dict = {'VZ': 'Verizon Wireless', 'CT': 'China Telecom', 'CM': 'China Mobile'}
        op_dict = {"VZ": "US-OP1", "CT": "CN-OP1", "CM": "CN-OP2"}
        col = ["app", "ECL", "operator", "ratio"]
        df_ecl = pd.DataFrame(columns=col)
        row = dict(zip(col, [0] * len(col)))
        # df_mid = self.df_agg[self.df_agg['node_id'] != 'A01']
        df_mid = self.df_agg[self.df_agg["ecl0_count"] < 100]

        #Exclude two tests with antenna installation issues in SZ
        df_mid = df_mid[(df_mid['test_id'] != 22109) & (df_mid['test_id'] != 21702)]

        df_mid = df_mid[df_mid["app"] != "Mobile"]

        for (app, operator), group in df_mid.groupby(["app", "operator"]):
            row["app"] = app
            row["operator"] = op_dict[operator]
            count_sum = (
                sum(group["ecl0_count"])
                + sum(group["ecl1_count"])
                + sum(group["ecl2_count"])
            )
            cum_sum = 0
            for i in range(3):
                row["ECL"] = i
                if count_sum == 0:
                    row["ratio"] = 0
                else:
                    row["ratio"] = (
                        sum(group["ecl{0}_count".format(i)]) / count_sum + cum_sum
                    )
                    if version == "v2":
                        cum_sum = row["ratio"]
                # print(row)
                df_ecl = df_ecl.append(row, ignore_index=True)

        print(df_ecl)
        if version == "v1":
            self.v.plot_ecl_distribution_by_app_v1(df_ecl)
        if version == "v2":
            self.v.plot_ecl_distribution_by_app_v2(df_ecl)

    def visualize_rsrp_snr_kde_by_app_op(self):
        def lmda_scale_rsrp_snr(row, var):
            # Only apply to BC28
            if row["module"] == "BC28":
                return float(row[var]) / 10
            else:
                return float(row[var])

        df = self.df_db.copy()
        df = df[(df["snr"] != -127) & (df["module"] != "SARA")]
        df["snr"] = df.apply(lambda x: lmda_scale_rsrp_snr(x, "snr"), axis=1)
        df["rsrp"] = df.apply(lambda x: lmda_scale_rsrp_snr(x, "rsrp"), axis=1)
        print(df)
        print(df["module"].unique())
        self.v.plot_rsrp_snr_kde_by_app(df, {"OP", "IP"})
        self.v.plot_rsrp_snr_kde_by_app(df, {"WM", "SD", "SL"})

    def visualize_msg3_data_rep(self, plot_option="pie"):
        # df = pd.read_csv(self.pftp_data_dir + "msg3_data_rep_sdio.csv")
        df = pd.read_csv(self.pftp_data_dir + "msg3_data_rep.csv")
        print(df["msg3_rep"])

        msg3_rep_sum_list = []
        data_rep_sum_list = []
        msg3_rep_1st_list = []  # the first element in the list
        data_rep_1st_list = []

        first_schedule_more_msg3_count = 0
        sum_msg3_more_than_data_count = 0
        for i in range(len(df)):
            msg3_rep_str_list = df["msg3_rep"].iloc[i].strip("][").split(",")
            msg3_rep_int_list = [int(x) for x in msg3_rep_str_list]
            msg3_rep_sum_list.append(sum(msg3_rep_int_list))

            data_rep_str_list = df["data_rep"].iloc[i].strip("][").split(",")
            data_rep_int_list = [int(x) for x in data_rep_str_list]
            one_data_rep_set = [[1, 1, 1, 1], [1, 1, 1], [1, 1], [1]]
            if data_rep_int_list in one_data_rep_set:
                data_rep_sum = 1
            else:
                data_rep_sum = sum(data_rep_int_list)
            data_rep_sum_list.append(data_rep_sum)

            if msg3_rep_int_list[0] > data_rep_int_list[0]:
                first_schedule_more_msg3_count += 1
            if sum(msg3_rep_int_list) > data_rep_sum:
                sum_msg3_more_than_data_count += 1

            msg3_rep_1st_list.append(np.log2(msg3_rep_int_list[0]))
            data_rep_1st_list.append(np.log2(data_rep_int_list[0]))
            # print(data_rep_int_list)
            # print(df['msg3_rep'].iloc[i], type(df['msg3_rep'].iloc[i]))

        # print(len(msg3_rep_sum_list), len(msg3_rep_1st_list), len(data_rep_sum_list), len(data_rep_1st_list))
        df["msg3_rep_sum"] = msg3_rep_sum_list
        df["data_rep_sum"] = data_rep_sum_list
        df["msg3_rep_1st"] = msg3_rep_1st_list
        df["data_rep_1st"] = data_rep_1st_list
        print(df["msg3_rep_sum"], df["data_rep_sum"])
        print(
            INFO, "First schedule, msg3>data:", first_schedule_more_msg3_count / len(df)
        )
        print(
            INFO, "Total schedule, msg3>data:", sum_msg3_more_than_data_count / len(df)
        )

        if plot_option == "bar3d":
            mesh_dict = dict()

            for i in range(len(df)):
                v3 = df["msg3_rep_1st"].iloc[i]
                vd = df["data_rep_1st"].iloc[i]
                if v3 not in mesh_dict:
                    mesh_dict[v3] = {}
                if vd not in mesh_dict[v3]:
                    mesh_dict[v3][vd] = 1
                else:
                    mesh_dict[v3][vd] += 1
            print(INFO, mesh_dict)
            self.v.plot_msg3_data_rep_3d(mesh_dict)

        elif plot_option == "pie":
            self.v.plot_msg3_data_rep_pie(df)
        elif plot_option == "scatter":
            self.v.plot_msg3_data_rep_scatter(df)

    def visualize_long_term_field_test(self):
        """Show how the power consumption v.s. temporal factors (time)"""
        long_term_test_id_set = {"2202", "2401"}
        df_lt = self.df_db[
            self.df_db["test_id"].isin(long_term_test_id_set)
        ].copy()  # lt = long term
        df_lt = df_lt[df_lt['e_packet']!=0]
        print(df_lt)
        df_lt.to_csv('~/long_term.csv')
        for (nid, tid), subgroup in df_lt.groupby(['node_id', 'test_id']):
            max_e = max(subgroup['e_packet'])
            min_e = min(subgroup['e_packet'])
            print(nid, tid, max_e, min_e, max_e/min_e, subgroup['app'].iloc[0])

        self.v.plot_long_term_energy_stats(df_lt, "e_packet")
        # self.v.plot_long_term_energy_vs_time(df_lt, "rsrp")

    def get_cell_info(self):
        self.load_csv()
        all_cell_id = []
        count = {"CT": [], "CM": [], "VZ": []}
        for (operator, earfcn, pci), group in self.df_db.groupby(
            ["operator", "earfcn", "pci"]
        ):
            if pci <= 0 or earfcn <= 0:
                continue
            cell_id = list(group["cell_id"])
            for i in range(0, len(cell_id)):
                if cell_id[i].find('"') >= 0:
                    cell_id[i] = cell_id[i].split('"')[1]
            cell_id = list(np.unique(cell_id))
            count[operator] += cell_id

            # print(operator, earfcn, pci, cell_id)
            # all_cell_id += cell_id
        # cell_id_unique = list(np.unique(all_cell_id))
        # print(len(all_cell_id), len(cell_id_unique), count)
        print(
            len(count["CT"]),
            len(np.unique(count["CT"])),
            len(count["CM"]),
            len(np.unique(count["CM"])),
            len(count["VZ"]),
            len(np.unique(count["VZ"])),
        )

    def visualize_energy_breakdown(self):
        """Note: the breakdown csv is calculated by
        gitlab/data-analyzer/energy-breakdown-by-phases"""
        e_df = pd.read_csv(
            self.global_path
            + "dy/Code/Gitlab/data-analyzer/energy-breakdown-by-phases/bm_phase_energy_200305.csv"
        )  # special case.

        # Scale the inactivity energy from 12s to 20s.
        e_df["e_inact"] = e_df["e_inact"] * 20 / 12

        # Calculate the total energy
        e_df["e_total"] = (
            e_df["e_wakeup"]
            + e_df["e_msg1"]
            + e_df["e_msg3"]
            + e_df["e_ack"]
            + e_df["e_data"]
            + e_df["e_inact"]
            + e_df["e_release"]
            + e_df["e_idle"]
        )
        print(e_df["e_total"])
        # print(e_df)
        phases = [
            "wakeup",
            "msg1",
            "msg3",
            "ack",
            "data",
            "inact",
            "release",
            "idle",
            # "total",
        ]
        e_dict = {"ecl0": {}, "ecl1": {}, "ecl2": {}}
        e_table = {
            "mean0": [],
            "mean1": [],
            "mean2": [],
            "std0": [],
            "std1": [],
            "std2": [],
        }
        for (ecl), g in e_df.groupby(["ecl"]):
            # print(ecl, g)
            for p in phases:
                e_dict["ecl{0}".format(ecl)]["e_" + p + "_mean"] = np.mean(g["e_" + p])
                e_dict["ecl{0}".format(ecl)]["e_" + p + "_std"] = np.std(g["e_" + p])
                e_table["mean{0}".format(ecl)].append(np.mean(g["e_" + p]))
                e_table["std{0}".format(ecl)].append(np.std(g["e_" + p]))

        # Save e_dict for the table
        agg_e_df = pd.DataFrame(e_table)
        # Swap the columns and rows
        agg_e_df = agg_e_df.T

        # Export for LaTeX table
        agg_e_df.to_csv(
            "../energy-breakdown-by-phases/aggegated_energy_table.csv",
            float_format="%.2f",
            sep="\t",
        )
        print(DBG, e_dict)

        # Plot the figure
        self.v.plot_energy_breakdown_pie(e_dict, phases, ecl_to_plot='0')
        self.v.plot_energy_breakdown_pie(e_dict, phases, ecl_to_plot='1')
        self.v.plot_energy_breakdown_pie(e_dict, phases, ecl_to_plot='2')

    def visualize_msg3_reschedule_experiment_results(self):
        m3_df = pd.read_csv(
            self.global_path
            + "Field Test/Deployment Experiment Output/post_ft_processing/opt_msg3_count.csv"
        )
        print(m3_df)
        print(m3_df["node_id"].unique())
        print(len(m3_df["test_id"].unique()))
        print("Number of rep=8:", len(m3_df[m3_df["msg3_rep"] == 8]))
        print("Number of rep=16:", len(m3_df[m3_df["msg3_rep"] == 16]))
        print("Number of rep=32:", len(m3_df[m3_df["msg3_rep"] == 32]))

        m3_agg_dict = {
            "node_id": [],
            "msg3_rep": [],
            "msg3_count": [],
            "msg3_retx": [],
            "packet_count": [],
            "retx_rate": [],
        }
        for (node, rep_num), g in m3_df.groupby(["node_id", "msg3_rep"]):
            # print('Node:', node, rep_num)
            # print('Total packet in node:', len(g))
            # print('Total MSG3 scheduled:', sum(g['msg2_rx']))
            # print('MSG3 re-scheduled:', sum(g['msg2_rx']) - len(g))
            m3_agg_dict["node_id"].append(node)
            m3_agg_dict["msg3_rep"].append(rep_num)
            m3_agg_dict["msg3_count"].append(sum(g["msg2_rx"]))
            m3_agg_dict["msg3_retx"].append(sum(g["msg2_rx"]) - len(g))
            m3_agg_dict["packet_count"].append(len(g))
            m3_agg_dict["retx_rate"].append(len(g[g["msg2_rx"] > 2]) / len(g))

        m3_agg_df = pd.DataFrame(m3_agg_dict)
        # Remove C01 node, which belongs to the ECL1
        m3_agg_df = m3_agg_df[m3_agg_df["node_id"] != "C01"]
        pd.options.display.width = 0
        print(m3_agg_df)

        self.v.plot_msg3_reschedule_count_bar(m3_agg_df)

        # self.v.plot_msg3_reschedule_count_box(m3_df)

    def visualize_field_test_msg3_scheduling(self):

        m3_df = pd.read_csv(
            self.global_path
            + "Field Test/Deployment Experiment Output/post_ft_processing/field_test_msg3_count.csv"
        )
        m3_df = m3_df[m3_df["msg4_rx"] != 0]  # for the field test one.
        print(m3_df)
        print("Number of usable logs:", len(m3_df))
        print("Unique nodes:", m3_df["node_id"].unique())
        print(len(m3_df["test_id"].unique()))

        m3_agg_dict = {
            "node_id": [],
            "msg3_count": [],
            "msg3_retx": [],
            "packet_count": [],
            "retx_rate": [],
        }
        for (node), g in m3_df.groupby(["node_id"]):
            print("Node:", node)
            print("Total packet in node:", len(g))
            print("Total MSG3 scheduled:", sum(g["msg2_rx"]))
            print("MSG3 re-scheduled:", sum(g["msg2_rx"]) - len(g))
            m3_agg_dict["node_id"].append(node)
            m3_agg_dict["msg3_count"].append(sum(g["msg2_rx"]))
            m3_agg_dict["msg3_retx"].append(sum(g["msg2_rx"]) - len(g))
            m3_agg_dict["packet_count"].append(len(g))
            m3_agg_dict["retx_rate"].append(len(g[g["msg2_rx"] > 2]) / len(g))

        m3_agg_df = pd.DataFrame(m3_agg_dict)
        # Remove C01 node, which belongs to the ECL1
        m3_agg_df = m3_agg_df[m3_agg_df["node_id"] != "C01"]
        print(m3_agg_df)
        print(m3_agg_df["retx_rate"])

        self.v.plot_field_test_msg3_reschedule_count(m3_agg_df)

    def reduce_pdf_figure_filesize_by_gs(self):
        figname_list = ['energy_breakdown_pie_ecl1']
        path_prefix = self.v.global_path + self.v.paper_pdf_buf_path + 'playground/'
        for fn in figname_list:
            full_fn = path_prefix + fn + '.pdf'
            self.v.gs_opt(full_fn)


class DistanceVsPower(PostFieldTestProcessor):
    """Create a new class to prevent the long code in its parent class"""

    def __init__(self, whoami):
        super(DistanceVsPower).__init__(whoami)
