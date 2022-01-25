import datetime
import subprocess
from pathlib import Path

import branca.colormap as cm
import folium
import geojsoncontour
import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
import scipy.ndimage
import seaborn as sns
from folium import plugins
from matplotlib import collections as matcoll
from matplotlib import style
from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnchoredText
from matplotlib.patches import Circle, Patch
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import griddata

from Utils import *


class DataVisualizer(object):
    def __init__(self, whoami):
        self.u = Utils()
        self.config = self.u.load_config("./config.json")

        self.global_path = self.config["env_prefix"][whoami][self.u.os]
        # print(INFO, 'Global prefix', self.global_path)

        self.figure_dir = self.global_path + self.config["figure_output_path"]
        # Store large volumn output png files.
        self.mid_out_dir = self.config["middle_file_dir_by_host"][self.u.hostname]

        self.paper_pdf_buf_path = "LaTeX Papers/assets_buffer/"

        sns.set_style(
            {"font.sans-serif": ["DejaVu Sans", "Liberation Sans", "Open Sans"]}
        )
        mpl.rc("pdf", fonttype=42)  # IMPORTANT: embed fonts to the PDF figure.
        self.text_size = 14  # default font weight for paper figure plot
        self.bar_palette = [
            "#78C850",  # Grass
            "#F08030",  # Fire
            "#6890F0",  # Water
            "#A8B820",  # Bug
            "#A8A878",  # Normal
            "#A040A0",  # Poison
            "#F8D030",  # Electric
            "#E0C068",  # Ground
            "#EE99AC",  # Fairy
            "#C03028",  # Fighting
            "#F85888",  # Psychic
            "#B8A038",  # Rock
            "#705898",  # Ghost
            "#98D8D8",  # Ice
            "#7038F8",  # Dragon
        ]

    def gs_opt(self, filename):
        """Optimize the exported pdf size by embedding only a subset of the fonts into the document."""
        filenameTmp = filename.split(".")[-2] + "_tmp.pdf"
        gs = [
            "gs",
            "-sDEVICE=pdfwrite",
            "-dEmbedAllFonts=false",
            "-dSubsetFonts=true",  # Create font subsets (default)
            "-dDetectDuplicateImages=true",  # Embeds images used multiple times only once
            "-dCompressFonts=true",  # Compress fonts in the output (default)
            "-dNOPAUSE",  # No pause after each image
            "-dQUIET",  # Suppress output
            "-dBATCH",  # Automatically exit
            "-sOutputFile=" + filenameTmp,  # Save to temporary output
            filename,
        ]  # Input file

        subprocess.run(gs)  # Create temporary file
        subprocess.run(["rm", filename], shell=True)  # Delete input file
        subprocess.run(
            ["mv", filenameTmp, filename], shell=True
        )  # Rename temporary to input file

    def plot_throughput_bler_timeline(self, df):
        sns.lineplot(df["time"], df["bler"])

    def plot_time_ticks(self, time_ticks_list, name):
        # time_ticks vs sample
        plt.figure()
        x = np.linspace(0, len(time_ticks_list) - 1, len(time_ticks_list))
        sns.lineplot(x=x, y=time_ticks_list)
        plt.xlabel("Samples")
        plt.ylabel("Second")
        plt.tight_layout()
        # plt.show()
        plt.savefig(self.figure_dir + "timeticks/" + name, dpi=300)
        plt.close()

    def plot_measurement_ecl_vs_time(self, df, df_ecl, name):
        print(df.head(5))
        print(df_ecl.head(5))

        # Preprocessing before plotting
        df_ecl["ecl"] += 1  # biased for better visualization

        ecl_time = df_ecl["time_ticks"].tolist()
        ecl_list = df_ecl["ecl"].tolist()
        by_meas_ecl_lines = []
        by_next_ecl_lines = []
        for i in range(len(ecl_time)):
            if df_ecl["ecl_selection_reason"].loc[i] == "m":  # selection reason
                pair = [(ecl_time[i], 0), (ecl_time[i], ecl_list[i])]
                by_meas_ecl_lines.append(pair)
            elif df_ecl["ecl_selection_reason"].loc[i] == "n":
                pair = [(ecl_time[i], 0), (ecl_time[i], ecl_list[i])]
                by_next_ecl_lines.append(pair)
        by_meas_color = ListedColormap(["#61cfdc"])
        by_next_color = ListedColormap(["#dc6161"])
        linecoll_m = matcoll.LineCollection(by_meas_ecl_lines, colors="#61cfdc")
        linecoll_n = matcoll.LineCollection(by_next_ecl_lines, colors="#dc6161")

        raw_m_count = [0, 0, 0]
        raw_n_count = [0, 0, 0]
        emc_dict = (
            df_ecl["ecl"]
            .where(df_ecl["ecl_selection_reason"] == "m")
            .value_counts()
            .to_dict()
        )  # ecl by measurement count
        enc_dict = (
            df_ecl["ecl"]
            .where(df_ecl["ecl_selection_reason"] == "n")
            .value_counts()
            .to_dict()
        )
        for i in (1, 2, 3):
            if i in emc_dict:
                raw_m_count[i - 1] = emc_dict[i]
            if i in enc_dict:
                raw_n_count[i - 1] = enc_dict[i]

        print(DBG, "by measurement/next count", raw_m_count, raw_n_count)
        bar_ind = (1, 2, 3)
        ecl_size = len(df_ecl)
        emc = [0, 0, 0]
        enc = [0, 0, 0]
        for i in range(len(raw_m_count)):
            emc[i] = raw_m_count[i] / ecl_size
            enc[i] = raw_n_count[i] / ecl_size
        print(DBG, "by measurement/next frequency", emc, enc)

        # Plotting
        f, axes = plt.subplots(
            3,
            2,
            figsize=(8, 4.8),
            sharey="row",
            sharex="col",
            gridspec_kw={"width_ratios": [4, 1]},
        )

        sns.lineplot(
            data=df,
            x="time_ticks",
            y="rsrp",
            linewidth=1,
            ax=axes[0, 0],
            color="#6190dc",
        )
        sns.distplot(df["rsrp"], kde=True, vertical=True, ax=axes[0, 1])
        sns.lineplot(
            data=df,
            x="time_ticks",
            y="snr",
            linewidth=1,
            ax=axes[1, 0],
            color="#61dc9e",
        )
        sns.distplot(df["snr"], kde=True, vertical=True, ax=axes[1, 1])
        axes[2, 0].add_collection(linecoll_m)
        axes[2, 0].add_collection(linecoll_n)
        axes[2, 0].scatter(
            df_ecl["time_ticks"],
            df_ecl["ecl"].where(df_ecl["ecl_selection_reason"] == "m"),
            color="#61cfdc",
            s=15,
            alpha=1,
        )
        axes[2, 0].scatter(
            df_ecl["time_ticks"],
            df_ecl["ecl"].where(df_ecl["ecl_selection_reason"] == "n"),
            color="#dc6161",
            marker="x",
            s=15,
            alpha=1,
        )
        # axes[2, 1].hist(df_ecl['ecl'], bins=3, density=True, color='#71e1f3', align='mid', orientation='horizontal')
        axes[2, 1].barh(bar_ind, emc, height=0.5, align="center", color="#4daadc")
        axes[2, 1].barh(
            bar_ind, enc, height=0.5, align="center", left=emc, color="#dca54d"
        )
        # Add the count to the plot
        axes[2, 1].text(0.02, 0.45, raw_m_count[0], fontsize=8)
        axes[2, 1].text(
            0.02, 1.45, "{0}, {1}".format(raw_m_count[1], raw_n_count[1]), fontsize=8
        )
        axes[2, 1].text(
            0.02, 2.45, "{0}, {1}".format(raw_m_count[2], raw_n_count[2]), fontsize=8
        )

        axes[0, 0].set_ylabel("RSRP (dB)", fontsize=14)
        axes[1, 0].set_ylabel("SNR (dB)", fontsize=14)
        axes[1, 0].yaxis.set_major_locator(MultipleLocator(10))
        axes[2, 0].set_ylabel("ECL", fontsize=14)
        axes[0, 1].set_ylabel("")
        axes[1, 1].set_ylabel("")
        axes[2, 1].set_ylabel("")
        axes[2, 0].set_xlabel("Time (s)", fontsize=14)
        axes[2, 0].set_ylim([0, 3.5])
        axes[2, 1].set_xlabel("Probability", fontsize=12)
        axes[2, 1].set_xlim([0, max(emc[0], emc[1] + enc[1], emc[2] + enc[2]) * 1.15])

        plt.sca(axes[2, 0])
        plt.yticks(np.arange(0, 4, 1), ["", "ECL0", "ECL1", "ECL2"])
        plt.tight_layout()
        plt.subplots_adjust(wspace=0.05, hspace=0.05)
        # plt.show()
        plt.savefig(self.figure_dir + "measurement_ecl_vs_time/" + name, dpi=300)
        plt.close()

    def plot_seq_num_scatter(self, file_1, file_2):

        list_1 = []
        list_2 = []
        f_1 = open(file_1, "r")
        next(f_1)
        for line in f_1:
            list_1.append(int(line.split(";")[0]))
        f_2 = open(file_2, "r")
        for line in f_2:
            list_2.append(int(line.split(",")[0]))

        print(DBG, len(list_1), len(list_2))
        print(len(set(list_1).intersection(set(list_2))))
        fig = plt.figure()
        plt.scatter(list_1, list_1)
        plt.scatter(list_2, [x + 1 for x in list_2])
        # plt.show()
        plt.close()

    def plot_bler_report_vs_time(self, df):
        fig = plt.figure()
        plt.plot(df["time_ticks"], df["rate"])
        plt.show()

    def plot_map(self, csv_file_path):
        # file.csv中存储需要标注的测试地点的信息，格式化为：
        # ;operator;latitude;longitude;rsrp;ecl
        # 文件有header
        f_r = open(csv_file_path, "r")
        df = pd.read_csv(f_r, sep=";")
        print(DBG, df)

        ## map type 1
        m = folium.Map(
            location=[31.9396, 118.7855],
            zoom_start=18,
            tiles="CartoDB PositronNoLabels",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            no_touch=False,
        )
        ## map type 2
        # m = folium.Map(
        #     location=[31.9396, 118.7855],
        #     zoom_start=14,
        #     tiles='HikeBike HikeBike',
        #     attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        # )

        color_list = ["green", "blue", "red"]
        marker_list = ["doughnut", "circle-dot", "rectangle-dot"]
        for i in range(0, len(df["latitude"])):
            # # marker type 1
            # num = int(df.iloc[i]['ecl'])
            # folium.Marker([df.iloc[i]['latitude'], df.iloc[i]['longitude']],
            #               popup=df.iloc[i]['rsrp'],
            #               icon=folium.plugins.BeautifyIcon(
            #                   icon_shape='circle',
            #                   border_color=color_list[df.iloc[i]['ecl']],
            #                   border_width=2,
            #                   number=num
            #               )
            #               ).add_to(m)

            # # marker type 2
            folium.Marker(
                [df.iloc[i]["latitude"], df.iloc[i]["longitude"]],
                popup=df.iloc[i]["rsrp"],
                icon=folium.plugins.BeautifyIcon(
                    icon_shape=marker_list[df.iloc[i]["ecl"]],
                    border_color=color_list[df.iloc[i]["ecl"]],
                    border_width=5,
                ),
            ).add_to(m)

        # Export
        html_path = self.figure_dir + "outdoor_map/map.html"
        # map_png = m._to_png(4)
        # with open(self.figure_dir + 'outdoor_map/map.png', 'wb') as f:
        #     f.write(map_png)
        m.save(html_path)
        # self.convert_html_to_png(html_path)
        f_r.close()

    def convert_html_to_png(self, html_path):
        # Assume the outpu dir is the same as the HTML file
        import selenium.webdriver, time

        driver = selenium.webdriver.PhantomJS()
        driver.set_window_size(4000, 3000)  # choose a resolution
        driver.get(html_path)
        # You may need to add time.sleep(seconds) here
        time.sleep(5)  # waiting for the map loading
        driver.save_screenshot(html_path.split(".")[0] + "4k.png")
        driver.close()

    """Cell Coverage Measurement Plots"""

    def plot_cell_coverage_contour(self, df):
        """
        df columns: time, long, lat, rsrp
        API reference:
        - https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html
        - https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.ndimage.filters.gaussian_filter.html
        """
        export_html_flag = True
        rsrp_min = np.min(df["rsrp"])
        rsrp_max = np.max(df["rsrp"])

        long_range = np.max(df["long"]) - np.min(df["long"])
        lat_range = np.max(df["lat"]) - np.min(df["lat"])

        levels = 4
        colors_list = [
            "#d7191c",
            "#fdae61",
            "#ffffbf",
            "#abdda4",
            "#579caf",
            "#66a075",
            "#bb7e8c",
            "#a5b3c9",
            "#d17bc8",
        ]
        grayscale_list = [
            "#FFFFFF",
            "#EEEEEE",
            "#DDDDDD",
            "#CCCCCC",
            "#BBBBBB",
            "#AAAAAA",
            "#999999",
            "#888888",
            "#777777",
            "#666666",
            "#555555",
            "#444444",
            "#333333",
            "#222222",
            "#111111",
        ]

        colors = grayscale_list[::2][1 : levels + 1][::-1]
        print(colors)
        map_granularity = 200
        coarse_level = 50  # the larger, the less smooth

        # print(DBG, np.min(df['long']), np.max(df['long']))
        long_arr = np.linspace(
            np.min(df["long"]) - 0.05 * long_range,
            np.max(df["long"]) + 0.05 * long_range,
            map_granularity,
        )
        lat_arr = np.linspace(
            np.min(df["lat"]) - 0.05 * lat_range,
            np.max(df["lat"]) + 0.05 * lat_range,
            map_granularity,
        )
        long_mesh, lat_mesh = np.meshgrid(long_arr, lat_arr)

        # Map the traces to a 2D plane.
        z_mesh = griddata(
            (df["long"], df["lat"]),
            df["rsrp"],
            (long_mesh, lat_mesh),
            method="linear",
            fill_value=np.min(df["rsrp"]),
            rescale=True,
        )

        # Smoothing the contour edge
        sigma = 2 * [map_granularity / coarse_level]  # [5,5]
        z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode="nearest")
        # Plot the trace and the contour color map.
        fig = plt.figure()
        plt.scatter(df["long"], df["lat"], s=10, c=df["rsrp"] + 130)
        contourf = plt.contourf(
            long_mesh, lat_mesh, z_mesh, levels=levels, alpha=0.5, colors=colors
        )
        plt.xlim(
            [
                np.min(df["long"]) - 0.05 * long_range,
                np.max(df["long"]) + 0.05 * long_range,
            ]
        )
        plt.ylim(
            [np.min(df["lat"]) - 0.05 * lat_range, np.max(df["lat"]) + 0.05 * lat_range]
        )
        plt.show()
        plt.close()

        if export_html_flag:
            # Convert matplotlib contourf to geojson
            geojson = geojsoncontour.contourf_to_geojson(
                contourf=contourf,
                min_angle_deg=3.0,
                ndigits=5,
                stroke_width=1,
                fill_opacity=0.5,
            )

            # Create the folium map
            geomap = folium.Map(
                [df.lat.mean(), df.long.mean()],
                zoom_start=16,
                tiles="CartoDB PositronNoLabels"
                # "cartodbpositron"
            )

            # Plot the contour plot on folium
            folium.GeoJson(
                geojson,
                style_function=lambda x: {
                    "color": x["properties"]["stroke"],
                    "weight": x["properties"]["stroke-width"],
                    "fillColor": x["properties"]["fill"],
                    "opacity": 0.6,
                },
            ).add_to(geomap)

            # Add the colormap legend
            cm = branca.colormap.LinearColormap(
                colors, vmin=rsrp_min, vmax=rsrp_max
            ).to_step(levels)
            cm.caption = "RSRP (dBm)"
            geomap.add_child(cm)

            # Fullscreen mode
            plugins.Fullscreen(position="topright", force_separate_button=True).add_to(
                geomap
            )

            # Plot the data
            geomap.save(
                self.global_path
                + self.config["coverage_measurement_folder_prefix"]
                + "folium_contour_rsrp_map.html"
            )

    ### TODO: Plot figure plans
    def plot_power_consumption_vs_app(self, df):
        # df columns: operator, app, power_consumption_list(unit: J)
        fig = plt.figure()
        sns.boxplot(x="app", y="power", hue="operator", data=df)
        plt.show()

    def plot_bler_vs_app(self, df):
        # df columns: operator, app, bler_list
        fig = plt.figure()
        sns.boxplot(x="app", y="power", hue="operator", data=df)
        plt.show()

    def plot_app_ecl_percent_bar(self, df, fig_name):
        # every app has one bar.
        # input df: app type, ECL0, ECL1, ECL2
        p1 = plt.bar(
            df["app"],
            df["ecl0"],
            width=0.35,
            color=["#bcecac"],
            edgecolor=["black"],
            linewidth=0.3,
        )
        p2 = plt.bar(
            df["app"],
            df["ecl1"],
            bottom=df["ecl0"],
            width=0.35,
            color=["steelblue"],
            edgecolor=["black"],
            linewidth=0.3,
        )
        p3 = plt.bar(
            df["app"],
            df["ecl2"],
            bottom=df["ecl1"] + df["ecl0"],
            width=0.35,
            color=["sandybrown"],
            edgecolor=["black"],
            linewidth=0.3,
        )

        plt.ylim((0, 1.3))
        plt.xticks(df["app"])
        plt.yticks(np.arange(0, 1.1, 0.2))
        plt.grid(axis="y", ls="-.")
        plt.legend((p1[0], p2[0], p3[0]), ("ECL0", "ECL1", "ECL2"))
        # plt.show()
        plt.savefig(self.figure_dir + fig_name, dpi=300)
        plt.close()

    def plot_current_debug(self, df, figname, show_flag):
        fig, axes = plt.subplots(2, 1, sharex=True)
        axes[0].plot(df["time"], "*")
        axes[0].set_ylabel("time (ms)")
        axes[0].axhline(65536, color="r")
        axes[1].plot(df["current"], "*")
        axes[1].set_ylabel("current (mA)")
        axes[1].axhline(0, color="r")
        plt.show()
        if show_flag:
            plt.show()
        else:
            # Export to PNG
            fig_out_path = self.figure_dir + "current/" + figname
            fig.savefig(fig_out_path, dpi=300)
        plt.close()

    def plot_current(self, df, figname, show_flag, stats_dict=None, is_amarisoft=False):
        fig, ax = plt.subplots(1, 1, figsize=(12, 7))
        if max(df["time"]) > 1000:
            df["time"] = df["time"] / 1000
        plt.plot(df["time"], df["current"], linewidth=0.6)
        plt.xlabel("time (s)")
        plt.ylabel("current (mA)")
        plt.axhline(0, ls=":", lw=0.5)
        plt.axvline(-0.01, ls=":", lw=0.5)
        plt.xlim([min(df["time"] - 0.1), max(df["time"] + 0.1)])
        # plt.axhline(reference_line[ue_type])
        if stats_dict is not None:
            # print(stats_dict)
            plt.axhline(stats_dict["i_tx_threshold"], ls=":", lw=0.5)
            for p in stats_dict["tx_intervals"]:
                plt.plot(
                    [df["time"].iloc[p[0]], df["time"].iloc[p[1]]],
                    [stats_dict["i_max"], stats_dict["i_max"]],
                    "g-",
                    lw=0.6,
                )
            plt.axvline(
                df["time"].iloc[stats_dict["last_tx_idx"]] + 0.05, ls=":", lw=0.5
            )
            energy_txt_str = "\t".join(
                [
                    "$E_{Tx}$=" + "{0:.3f} mJ".format(stats_dict["tx_energy"]),
                    "$E_{Active}$=" + "{0:.3f} mJ".format(stats_dict["active_energy"]),
                    "$E_{between-dash-line}$="
                    + "{0:.3f} mJ".format(stats_dict["till_last_tx_energy"]),
                ]
            )
            i_stats_str = "\t".join(
                [
                    "$I_{max}$=" + "{0:.3f} mA".format(stats_dict["i_max"]),
                    "$I_{min}$=" + "{0:.3f} mA".format(stats_dict["i_min"]),
                ]
            )
            energy_txt_str += "\n" + i_stats_str
            anchored_text = AnchoredText(energy_txt_str, loc=1)
            ax.add_artist(anchored_text)
            # props = dict(facecolor='wheat', alpha=0.5)
            # plt.text(right, top, energy_txt_str,
            #          horizontalalignment='right',
            #          fontsize=12, verticalalignment='top', bbox=props)
        plt.title(figname)
        plt.tight_layout()

        if show_flag:
            plt.show()
        else:
            # Export to PNG
            node_id, test_id, _ = self.u.get_info_from_filename(figname)
            if node_id[0] == "A":
                suffix = "us"
            elif node_id[0] == "C":
                suffix = "cn"
            elif node_id[0] == "D":
                suffix = "cn"
            else:
                suffix = "xx"
            if is_amarisoft:
                # override the above
                suffix = "opt"

            # Note: save the figures to local drive instead of Nutstore
            fig_out_path = self.mid_out_dir + "current_fig_{0}/{1}/".format(
                suffix, node_id
            )
            # fig_out_path = self.mid_out_dir + 'current_buf_{0}/{1}/'.format(suffix, node_id)
            Path(fig_out_path).mkdir(parents=True, exist_ok=True)
            fig_out_path += figname
            # plt.show()
            # fig.savefig(fig_out_path, dpi=100)
            fig.savefig("D:/temp/sz/" + figname.split(".")[0] + ".png")
            plt.close()

    def plot_current_distributions(self, df):
        sns.kdeplot(df["current"])
        plt.show()

    def convert_color_tuple_to_str_code(self, c_tuple):
        R = hex(int(c_tuple[0] * 255))[2:4].zfill(2).upper()
        G = hex(int(c_tuple[1] * 255))[2:4].zfill(2).upper()
        B = hex(int(c_tuple[2] * 255))[2:4].zfill(2).upper()
        return "#{0}{1}{2}".format(R, G, B)

    def test_plot_map_indoor(self, df):
        # fig_path = 'C:\\Users\\lenovo\\Desktop/indoor_map/indoor_map_us.png'
        fig_path = (
            self.global_path
            + "Docs/LaTeX Papers/paper_assets_generator/Figures/maps/eb_floor_plan.png"
        )
        import cv2

        img = cv2.imread(fig_path)
        fig, ax = plt.subplots()
        plt.subplots_adjust(0.12, 0.11, 0.83, 0.88)
        # plt.subplots_adjust(left=0.02, bottom=0.06, right=0.87, top=1)
        ximg = cv2.flip(img, 0, dst=None)
        ax.imshow(ximg)
        # ax = plt.gca()
        ax.invert_yaxis()  # y轴反向
        # plt.show()

        df_building = df[
            (df["long"] < -84.4795)
            & (df["long"] > -84.4820)
            & (df.lat > 42.7237)
            & (df.lat < 42.726)
        ]
        # & (df['cell_id_num']==1)].copy()# only one cell

        df_building["long"] = df_building.long - min(df_building.long)
        df_building["lat"] = df_building.lat - min(df_building.lat)
        df_building["long"] *= 1000000  # xscale 1000000
        df_building["lat"] *= 1350000  # yscale 1400000
        df_building["long"] += 100  # xoffset 80
        df_building["lat"] += 210  # yoffset 150
        app_to_mk_dict = {"SL": "s", "WM": "^", "IP": "+", "SD": "o"}
        app_short_to_label_dict = {
            "SL": "Smart lock",
            "WM": "Water meter",
            "SD": "Smoke detection",
        }

        cell_to_marker_dict = {"1": "s", "2": "^", "3": "+", "4": "o", "5": "*"}
        # cell_num_to_label_dict = {'1': '<=2', '2': '2<x<=3',
        #                            'c': '3<x<=4', 'd': '4<x<=5'}

        cm = plt.cm.get_cmap("Reds")
        # plt.show()
        marker = "app"
        if marker == "app":
            for app, group in df_building.groupby("app"):
                group = group.copy().reset_index(drop=True)
                for i in range(0, len(group)):
                    if group.iloc[i]["e_packet_mean"] > 1500:
                        group.loc[i, "e_packet_mean"] = 1500
                plt.scatter(
                    group.long,
                    group.lat,
                    marker=app_to_mk_dict[app],
                    c=group.e_packet_mean,
                    cmap=cm,
                    edgecolors="k",
                    linewidths=1.0,
                    label=app_short_to_label_dict[app],
                )

        # elif marker == 'cell_id':
        #     distinct_cells = df_building['cell_id_list'].unique()
        #     id = 0
        #     cell_short_label_dict = {}
        #     for cell in distinct_cells:
        #         id += 1
        #         cell_short_label_dict[cell] = str(id)
        #     print(cell_short_label_dict)
        #     for cell_id, group in df_building.groupby('cell_id_list'):
        #         group = group.copy().reset_index(drop=True)
        #         for i in range(0, len(group)):
        #             if group.iloc[i]['e_packet_mean'] > 1500:
        #                 group.loc[i, 'e_packet_mean'] = 1500
        #         plt.scatter(group.long, group.lat, marker=cell_to_marker_dict[cell_short_label_dict[cell_id]], c=group.e_packet_mean, cmap=cm,
        #                     edgecolors='k', linewidths=0.5, label=cell_short_label_dict[cell_id])

        cb = plt.colorbar(
            ticks=[0, 500, 1000, 1500],
            fraction=0.03,
            pad=0.03,
            label="Mean Energy Per Packet (mJ)",
            extend="max",
        )

        plt.clim(0, 1500)
        plt.axis("off")
        plt.legend(loc=(0.0, -0.05), ncol=3)
        # plt.legend()

        # plt.scatter([529.358, 518.936, 742.595, 2467.87, 2794.41, 2409.71],
        #             [1203.11, 971.518, 472.942, 1416.35, 821.873, 750.794])   # buidling south-35

        plt.savefig(
            self.global_path
            + "Docs/LaTeX Papers/nbiot_paper_first_draft/assets/indoor_measurement_map.png",
            dpi=300,
        )
        plt.show()

    def plot_packet_energy_map(self, df):
        # print(DBG, df)
        # print(df['app'].unique())

        # if abs(np.mean(df['long'])-84) < 5:
        #     df['long'] = -df['long']  # In USA
        # map type 1
        m = folium.Map(
            # location=[31.9396, 118.7855],
            location=[np.mean(df["lat"]), np.mean(df["long"])],
            zoom_start=15,  # 16
            tiles="CartoDB PositronNoLabels",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            no_touch=False,
        )

        color_list = ["green", "blue", "red"]
        app_to_mk_dict = {
            "OP": "circle-dot",
            "SL": "circle-dot",
            "WM": "rectangle-dot",
            "IP": "rectangle-dot",
            "SD": "circle-dot",
        }

        app_to_icon_dict = {
            "OP": "fa-parking",
            "SL": "circle-dot",
            "WM": "rectangle-dot",
            "IP": "triangle",
            "SD": "triangle",
        }
        # cm_old = plt.get_cmap(('Reds_r'))
        # cs = branca.colormap.linear.YlGnBu_09.scale(0, 1)
        cs = cm.LinearColormap(
            ["green", "yellow", "orange", "red"], index=[0, 0.25, 0.75, 0.9]
        )
        df["color_scale"] = (df["e_packet_mean"] - min(df["e_packet_mean"])) / (
            max(df["e_packet_mean"]) - min(df["e_packet_mean"])
        )

        for i in range(0, len(df["lat"])):
            # for i in range(0, 2):
            # # marker type 2
            point_color = cs(df["color_scale"].iloc[i])
            # point_color = self.convert_color_tuple_to_str_code(point_color)
            # print(point_color)
            e_icon = plugins.BeautifyIcon(
                prefix="fa",
                icon=None,  # app_to_icon_dict[df['app'].iloc[i]],
                icon_shape=app_to_mk_dict[df["app"].iloc[i]],
                icon_size=[12, 12],
                # boarder_color=point_color,
                text_color="#000",
                background_color=point_color,
                border_width=1,
            )
            print(DBG, i, e_icon.options["iconShape"], point_color)
            folium.Marker(
                [df.iloc[i]["lat"], df.iloc[i]["long"]],
                popup=df.iloc[i]["e_packet_mean"],
                icon=e_icon,
            ).add_to(m)
        # icon_plane = plugins.BeautifyIcon( icon='plane', border_color='#b3334f', text_color='#b3F34f', icon_shape='triangle')
        # folium.Marker(location=[46, -122], popup='Portland, OR', icon=icon_plane).add_to(m)

        # plt.show()
        # Export
        html_path = self.figure_dir + "outdoor_map/map.html"
        m.save(html_path)
        # self.convert_html_to_png(html_path)

    def plot_energy_vs_location_pf(self, df, e_type, fig_name):
        mpl.rc("pdf", fonttype=42)
        separate_by_op = True

        sns.set_style("whitegrid")

        fig, ax = plt.subplots(1, 1, figsize=(4, 4))
        # (4, 4) for small form-factor (8, 4) for wide one.
        y_lb_dict = {
            "e_tx_mean": "Mean Tx energy in a test (mJ)",
            "e_active_mean": "Mean active energy in a test (J)",
            "e_packet_mean": "Mean packet energy in a test (mJ)",
        }
        if e_type in y_lb_dict.keys():
            y_lb = y_lb_dict[e_type]
        else:
            y_lb = e_type

        # order_list = ['OP', 'IP', 'SD', 'SL', 'WM']
        order_list = ["OP", "SL", "WM", "SD", "IP"]

        if separate_by_op:
            sns.boxplot("app", e_type, data=df, hue="operator", order=order_list)

            sns.stripplot(
                "app",
                e_type,
                data=df,
                hue="operator",
                order=order_list,
                size=3,
                jitter=0.28,
                linewidth=0.1,
                edgecolor="gray",
                alpha=0.3,
                marker="^",
            )
        else:
            sns.boxplot("app", e_type, data=df, order=order_list, alpha=0.7)
            sns.stripplot(
                "app",
                e_type,
                data=df,
                order=order_list,
                size=2,
                jitter=0.28,
                linewidth=0.5,
                edgecolor="gray",
                alpha=0.98,
                palette="Set2",
            )

        ax.axhline(0, ls=":", lw=0.6)
        # Add transparency to colors
        for patch in ax.artists:
            r, g, b, a = patch.get_facecolor()
            patch.set_facecolor((r, g, b, 0.8))
        ax.set_xlabel("Application scenarios", fontsize=self.text_size)
        ax.set_xticklabels(
            [
                "Outdoor-\nOP",
                "Indoor-\nSL",
                "Indoor-\nWM",
                "Indoor-\nSD",
                "Indoor-\nIP",
                # "Outdoor-\nParking",
                # "Indoor-\nSmart lock",
                # "Indoor-\nWater meter",
                # "Indoor-\nSmoke sensing",
                # "Indoor-\nParking",
            ]
        )
        ax.set_ylabel(y_lb, fontsize=self.text_size)
        plt.tick_params(axis="both", which="major", labelsize=self.text_size - 3)
        handles, labels = ax.get_legend_handles_labels()
        new_lb = ["US-OP1", "CN-OP1", "CN-OP2"]
        ax.legend(handles[:3], new_lb)
        plt.tight_layout()

        plt.savefig(self.global_path + self.paper_pdf_buf_path + fig_name)
        plt.show()
        plt.close()

    def plot_ecl_distribution_by_app_v1(self, df_ecl):
        order_list = ["OP", "IP", "SD", "SL", "WM"]
        sns.set(font_scale=1.2)
        sns.set_style("whitegrid")

        # Plot categorical figure
        g = sns.catplot(
            x="app",
            y="ratio",
            hue="ECL",
            col="operator",
            data=df_ecl,
            kind="bar",
            palette="Set3",
            order=order_list,
            legend_out=False,
            linewidth=0.5,
            edgecolor=".4",
        )

        # Tweak the figure
        g.set_axis_labels("", "")
        g.set_titles("Operator={col_name}")
        # g.set_xlabel('Location profile', fontsize=self.text_size)
        g.set_xticklabels(
            [
                "Outdoor-\nParking",
                "Indoor-\nParking",
                "Indoor-\nSmoke\nsensing",
                "Indoor-\nSmart\nlock",
                "Indoor-\nWater\nmeter",
            ],
            fontsize=self.text_size + 3,
        )
        g.set(ylim=(0, 1))
        g.axes[0, 1].set_xlabel("Location Profile", fontsize=self.text_size + 7)
        g.axes[0, 0].set_ylabel("Percentage", fontsize=self.text_size + 7)
        g.fig.tight_layout()

        plt.savefig(
            self.global_path
            + "Docs/LaTeX Papers/nbiot_paper_first_draft/assets/ecl_dist_by_app_op.pdf"
        )
        plt.show()
        plt.close()

    def plot_ecl_distribution_by_app_v2(self, df_ecl):
        # Define control parameters
        order_list = ["OP", "SL", "WM", "SD", "IP"]
        hue_order_list = ["US-OP1", "CN-OP1", "CN-OP2"]
        num_app = len(order_list)
        num_op = 3
        num_hatch_cycle = 15
        hatch_list = [None, "+", "x"]
        # hatch_list = [None, None, None, '+', 'x', None, '++', 'xx', None, '++', 'xx']
        sns.set(font_scale=1.2)
        sns.set_style("white")
        sns.set_style(
            {"font.sans-serif": ["DejaVu Sans", "Liberation Sans", "Open Sans"]}
        )
        color_list = ["#348dd6", "#d6c434", "#d66534"]  # for ECL0-1-2
        alpha = 0.7
        patch_color_list = [
            "#88bfe6",  # (0.2833, 0.5450, 0.7598, alpha),
            "#d5d56e",  # (0.7598, 0.7068, 0.2833, alpha),
            "#ef9ebd",  # (0.7598, 0.4274, 0.2833, alpha)
        ]

        # Plot the figure
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))  # originally ()8,5)
        sns.set_palette("Reds")
        for i, g in enumerate(df_ecl.groupby("ECL")):
            print(g[1]["operator"])
            sns.barplot(
                data=g[1],
                x="app",
                y="ratio",
                hue="operator",
                hatch=hatch_list[i],
                order=order_list,
                hue_order=hue_order_list,
                zorder=-i,  # so first bars stay on top
                edgecolor="k",
            )

        # Tweak plot
        # Add hatch and color to the bars
        for i, thisbar in enumerate(ax.patches):
            # Set a different hatch for each bar
            # print(i, thisbar.get_facecolor())
            # x, y = thisbar.get_xy()
            # cx = x + thisbar.get_width()/2.0
            # cy = y + thisbar.get_height()/2.0
            # ax.annotate(str(i), (cx, cy))
            if 0 <= i < num_hatch_cycle:
                thisbar.set_facecolor(patch_color_list[0])
            elif num_hatch_cycle <= i < num_hatch_cycle * 2:
                thisbar.set_facecolor(patch_color_list[1])
            elif num_hatch_cycle * 2 <= i < num_hatch_cycle * 3:
                thisbar.set_facecolor(patch_color_list[2])

            thisbar.set_alpha(0.9)

            if i % num_hatch_cycle < num_app:
                thisbar.set_hatch(hatch_list[0])
            elif num_app <= i % num_hatch_cycle < 2 * num_app:
                thisbar.set_hatch(hatch_list[1])
            elif 2 * num_app <= i % num_hatch_cycle < 3 * num_app:
                thisbar.set_hatch(hatch_list[2])

        # ax.set_xlabel('Location profile', fontsize=self.text_size)
        ax.set_xlabel("", fontsize=self.text_size - 1)
        ax.set_xticklabels(
            [
                "Outdoor-\nParking",
                "Indoor-\nSmart\nlock",
                "Indoor-\nWater\nmeter",
                "Indoor-\nSmoke\nsensing",
                "Indoor-\nParking",
            ],
            fontsize=self.text_size - 1,
        )
        ax.set_ylabel("Ratio", fontsize=self.text_size + 1)
        plt.tick_params(axis="both", which="major", labelsize=self.text_size + 1)
        handles, labels = ax.get_legend_handles_labels()
        new_lb = hue_order_list
        ecl_lgd_handler = [
            Patch(hatch=hatch_list[0], facecolor="w", edgecolor="k", label=new_lb[0]),
            Patch(facecolor=patch_color_list[0], edgecolor="k", label="ECL0"),
            Patch(hatch=hatch_list[1], facecolor="w", edgecolor="k", label=new_lb[1]),
            Patch(facecolor=patch_color_list[1], edgecolor="k", label="ECL1"),
            Patch(hatch=hatch_list[2], facecolor="w", edgecolor="k", label=new_lb[2]),
            Patch(facecolor=patch_color_list[2], edgecolor="k", label="ECL2"),
        ]
        ax.axhline(1.005, ls=":", lw=1)

        # Create another legend for the second line.
        ax.legend(
            handles=ecl_lgd_handler,
            loc="lower left",
            ncol=3,
            bbox_to_anchor=(0.00, 1.02),
            fontsize=self.text_size - 2,
        )
        plt.subplots_adjust(top=0.858, bottom=0.16, left=0.15, right=0.985)
        plt.savefig(
            self.global_path + self.paper_pdf_buf_path + "ecl_dist_by_app_op.pdf"
        )
        plt.show()
        return

    def plot_rsrp_snr_kde_by_app(self, df, allowed_app_set=None):
        def truncate_cmap(cmap, minval=0.0, maxval=1.0, n=100):
            new_cmap = colors.LinearSegmentedColormap.from_list(
                "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
                cmap(np.linspace(minval, maxval, n)),
            )
            return new_cmap

        if allowed_app_set is not None:
            df = df[df["app"].isin(allowed_app_set)].copy()
        app_short_to_full_dict = {
            "OP": "Outdoor parking",
            "IP": "Indoor parking",
            "SD": "Smoke sensing",
            "SL": "Smart lock",
            "WM": "Water meter",
        }
        sns.set_style("white")
        fig, axes = plt.subplots(
            2,
            2,
            sharex="col",
            sharey="row",
            figsize=(5, 4),
            squeeze=True,
            gridspec_kw={"width_ratios": [5, 1], "height_ratios": [1, 5]},
        )
        app_list = []
        ls_list = ["solid", "dashed", "dashdot", "solid", "dotted"]
        # sns.set_palette("Set1")
        cmap_list = ["Reds", "Blues", "Greens", "Purples", "Oranges"]
        # color_list = ['#4E1A3D', '#CFEED1', '#FF2768', '#05E0E9', '#B175FF']
        cmap_min = 0.4
        cmap_max = 0.8
        t_cmap_list = [
            truncate_cmap(plt.get_cmap(x), cmap_min, cmap_max) for x in cmap_list
        ]

        color_1d_list = ["red", "blue", "green", "purple", "orange"]
        j = 0
        for i, subdata in df.groupby("app"):
            subdata = subdata.dropna()
            app_list.append(app_short_to_full_dict[subdata["app"].iloc[0]])
            print(INFO, "Num of point in {0}: {1}".format(app_list[-1], len(subdata)))
            # 2D kde
            sns.kdeplot(
                subdata["snr"],
                subdata["rsrp"],
                ax=axes[1, 0],
                n_levels=15,
                shade=False,
                shade_lowest=False,
                legend=True,
                cmap=t_cmap_list[j],
                # alpha=0.8,
                label=app_list[-1],
                linestyles=ls_list[j],
            )
            # 1D kde - SNR
            sns.kdeplot(
                subdata["snr"],
                ax=axes[0, 0],
                shade=True,
                color=color_1d_list[j],
                legend=False,
                # alpha=0.3,
                linestyle=ls_list[j],
            )
            # 1D kde - RSRP
            sns.kdeplot(
                subdata["rsrp"],
                ax=axes[1, 1],
                vertical=True,
                shade=True,
                color=color_1d_list[j],
                legend=False,
                # alpha=0.3,
                linestyle=ls_list[j],
            )
            j += 1

        for ax in axes.flat:
            if ax.is_first_col():
                if ax.is_first_row():
                    sns.despine(bottom=False, left=False, ax=ax)
            if ax.is_last_col():
                if ax.is_first_row():
                    sns.despine(left=True, bottom=True, ax=ax)
                if ax.is_last_row():
                    sns.despine(left=False, bottom=False, ax=ax)

        # Tweak main figure
        axes[1, 0].set_xlabel("SNR (dB)", fontsize=self.text_size + 1)
        axes[1, 0].set_ylabel("RSRP (dBm)", fontsize=self.text_size + 1)
        axes[1, 0].set_ylim([-125, -55])
        axes[1, 0].set_xlim([-20, 35])
        axes[1, 0].xaxis.set_major_locator(plt.MaxNLocator(6))
        axes[1, 0].yaxis.set_major_locator(plt.MaxNLocator(7))
        axes[1, 0].tick_params(axis="both", labelsize=self.text_size - 1)

        # Tweak upper density
        axes[0, 0].set_ylabel("Prob.", fontsize=self.text_size - 1)
        axes[1, 1].set_xlabel("Prob.", fontsize=self.text_size - 1)

        # Handcrafted legend
        rsrp_snr_lgd_handler = []
        for k in range(len(app_list)):  # number of apps
            rsrp_snr_lgd_handler.append(
                Circle(
                    (0, 0),
                    edgecolor="k",
                    facecolor=color_1d_list[k],
                    label=app_list[k],
                    linestyle=ls_list[k],
                    alpha=0.7,
                )
            )
        axes[1, 0].legend(
            handles=rsrp_snr_lgd_handler,
            loc="upper left",
            bbox_to_anchor=(0.02, 0.98),
            fontsize=self.text_size - 4,
        )
        plt.subplots_adjust(
            top=0.984, bottom=0.162, left=0.187, right=0.977, hspace=0.01, wspace=0.01
        )

        # plt.tight_layout()
        pdf_out_suffix = ""
        if allowed_app_set:
            pdf_out_suffix = "_" + "_".join(
                sorted([x.lower() for x in allowed_app_set])
            )
        # plt.savefig(self.global_path+'Docs/LaTeX Papers/nbiot_paper_first_draft/assets/rsrp_snr_kde_by_app{0}.pdf'.format(pdf_out_suffix))
        plt.show()

    def plot_msg3_data_rep_scatter(self, df):
        x = np.linspace(0, len(df), len(df), endpoint=False)
        y = np.linspace(0, len(df), len(df), endpoint=False)
        for i in range(0, len(df)):
            if df["msg3_rep"].iloc[i] > df["data_rep"].iloc[i]:
                y[i] += 500
            elif df["msg3_rep"].iloc[i] < df["data_rep"].iloc[i]:
                y[i] -= 1
            else:
                pass
        # print(x, y)
        plt.scatter(x, y)
        plt.show()

    def plot_msg3_data_rep_pie(self, df):
        style.use("seaborn-pastel")
        more_msg3_count = len(df[df["msg3_rep_1st"] > df["data_rep_1st"]])
        more_data_count = len(df[df["msg3_rep_1st"] < df["data_rep_1st"]])
        equal_count = len(df[df["msg3_rep_1st"] == df["data_rep_1st"]])
        print(more_msg3_count, more_data_count, equal_count)
        lb_list = ["MSG3>Data", "MSG3<Data", "MSG3=Data"]

        fig1, ax1 = plt.subplots(figsize=(4, 3))
        patches, texts, autotexts = ax1.pie(
            [more_msg3_count, more_data_count, equal_count],
            labels=lb_list,
            autopct="%1.1f%%",
        )
        print(texts)
        for p in patches:
            p.set_edgecolor("k")
            p.set_linewidth(0.3)
        for t in texts:
            t.set_fontsize(self.text_size - 2)
        for at in autotexts:
            at.set_fontsize(self.text_size - 3)
        ax1.axis("equal")
        # plt.subplots_adjust(top=0.9, bottom=0.2, left=0, right=1)
        plt.tight_layout()
        # plt.savefig(self.global_path+'Docs/LaTeX Papers/nbiot_paper_first_draft/assets/msg3_data_rep_pie.pdf')
        plt.show()

    def plot_msg3_data_rep_3d(self, mesh_dict):
        from mpl_toolkits.mplot3d import Axes3D

        x = []
        y = []
        top = []
        for k3 in mesh_dict.keys():
            # print(k3, mesh_dict.keys())
            for kd in mesh_dict[k3].keys():
                x.append(k3 - 0.25)
                y.append(kd - 0.25)
                top.append(mesh_dict[k3][kd])
        # Length of x, y, and top = # of bars you have
        bottom = np.zeros(len(top))
        width = depth = 0.5
        style.use("seaborn-paper")
        fig = plt.figure(figsize=(6, 4.2))
        ax0 = fig.add_subplot(111, projection="3d")
        ax0.bar3d(
            x,
            y,
            bottom,
            width,
            depth,
            top,
            shade=True,
            alpha=0.6,
            color="#00ceaa",
            edgecolor="k",
            linewidth=1,
        )
        for bar_patch in ax0.patches:
            bar_patch.set_alpha(0.5)
        ax0.set_xlabel("MSG3 Repetition Gain (dB)", fontsize=self.text_size - 2)
        ax0.set_ylabel("Data Block Repetition Gain (dB)", fontsize=self.text_size - 2)
        ax0.set_zlabel("Count", fontsize=self.text_size - 2)
        plt.subplots_adjust(
            top=0.963, bottom=0.103, left=0.0, right=0.945, hspace=0.2, wspace=0.2
        )
        # Annotation
        for xt, yt, zt in zip(x, y, top):
            ax0.text(
                xt,
                yt,
                zt + 35,
                "%d" % zt,
                color="k",
                horizontalalignment="center",
                verticalalignment="bottom",
            )
        # No plt.savefig() here because need to rotate the angle manually.
        plt.show()

    def timestamp_str_to_series(self, df):
        """Note: the df should only contain one test's data, otherwise the timestamps are messed up."""

        def lmda_timestamp_to_dt(ts):
            if ts[0] == "_":
                return datetime.datetime.strptime(ts, "_%Y%m%d_%H%M_%S")
            else:
                return datetime.datetime.strptime(ts, "%Y%m%d_%H%M%S")

        df["packet_timestamp"] = df["packet_timestamp"].astype("str").copy()
        df = df[df["packet_timestamp"] != "nan"]
        df["t_packet"] = df["packet_timestamp"].apply(lambda x: lmda_timestamp_to_dt(x))
        t_start = df["t_packet"].iloc[0]
        df["t_packet"] = df["t_packet"] - t_start
        return df

    def plot_long_term_energy_stats(self, df_lt, var_name):
        """M1: BG96, M2: SARA, M3: BC66, M4: ME3616, M5: BC28, M6: BC26"""
        tuple_to_label_dict = {
            2202: {
                "A01": "WM, M1",
                "A02": "WM, M2",
                "A03": "WM, M3",
                "A04": "SD, M1",
                "A05": "SD, M2",
                "A06": "SD, M3",
            },
            2401: {
                "A01": "SD, M1",
                "A02": "SD, M2",
                "A03": "SD, M3",
                "A04": "OP, M1",
                "A05": "OP, M2",
                "A06": "OP, M3",
            },
        }
        tuple_to_linestyle_dict = {
            2202: {
                "A01": "-",
                "A02": "-",
                "A03": "-",
                "A04": "-.",
                "A05": "-.",
                "A06": "-.",
            },
            2401: {"A04": ":", "A05": ":", "A06": ":"},
        }
        line_color_dict = {
            "A01": "k",
            "A04": "k",
            "A02": "b",
            "A05": "b",
            "A03": "y",
            "A06": "y",
        }
        ignored_list = {(2401, "A01"), (2401, "A02"), (2401, "A03")}
        fig, ax = plt.subplots(figsize=(7.0, 3.8))  # mobicom(3.8, 3.8)
        for i, g in enumerate(df_lt.groupby(["test_id", "node_id"])):
            """Note: g[0] is the group_id tuple, g[1] is the actual df"""
            if g[0] in ignored_list:
                continue
            new_df = self.timestamp_str_to_series(g[1])
            if var_name == "e_active" or var_name == "e_packet":
                new_df[var_name] = new_df[var_name].divide(1000)
            print(g[0])
            # Convert ns to seconds
            new_df["t_packet"] = new_df["t_packet"].astype("timedelta64[s]")
            # Trim the time range
            new_df = new_df[new_df["t_packet"] < 80000]

            # sns.lineplot(x='t_packet',
            #              y=var_name,
            #              data=new_df,
            #              label=tuple_to_label_dict[g[0][0]][g[0][1]],
            #              linewidth=0.8,
            #              ax=ax)
            # sns.kdeplot(new_df[var_name], label=tuple_to_label_dict[g[0][0]][g[0][1]], cumulative=True, ax=ax)
            cnt, edges = np.histogram(
                new_df[var_name],
                bins=len(new_df[var_name]),
                density=False,
                weights=np.ones(len(new_df)) / len(new_df),
            )
            # plot the data as a step plot.
            ax.step(
                edges[:-1],
                cnt.cumsum(),
                color=line_color_dict[g[0][1]],
                label=tuple_to_label_dict[g[0][0]][g[0][1]],
                linestyle=tuple_to_linestyle_dict[g[0][0]][g[0][1]],
            )
            # ax.hist(new_df[var_name], normed=True, histtype='step', bins=len(new_df[var_name]), label=tuple_to_label_dict[g[0][0]][g[0][1]], cumulative=True)
        # get current axis
        # ax = plt.gca()
        # get current xtick labels
        # xticks = ax.get_xticks()
        # convert all xtick labels to selected format from ms timestamp
        # df['t_packet'] = pd.to_datetime(new_df['t_packet'], unit='s')
        # ax.set_xticklabels([pd.to_datetime(tm, unit='ms').strftime('%H:%M') for tm in xticks],
        #            rotation=50)
        plt.axhline(1, ls=":", lw=0.8)
        plt.legend()
        plt.xlabel("Packet energy (J)", fontsize=self.text_size)
        plt.ylabel("CDF", fontsize=self.text_size)
        plt.xlim(left=0, right=10.2)
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.savefig(self.global_path + self.paper_pdf_buf_path + "e_pkt_long_term.pdf")
        plt.show()

    def plot_long_term_energy_vs_time(self, df_lt, var_name):
        """For analysis only, will not be in paper."""
        tuple_to_label_dict = {
            2202: {
                "A01": "Water meter - M1",
                "A02": "Water meter - M2",
                "A03": "Water meter - M3",
                "A04": "Smoke detection - M1",
                "A05": "Smoke detection - M2",
                "A06": "Smoke detection - M3",
            },
            2401: {
                "A01": "Smoke detection - M1",
                "A02": "Smoke detection - M2",
                "A03": "Smoke detection - M3",
                "A04": "Outdoor parking - M1",
                "A05": "Outdoor parking - M2",
                "A06": "Outdoor parking - M3",
            },
        }
        tuple_to_linestyle_dict = {
            2202: {
                "A01": "-",
                "A02": "-",
                "A03": "-",
                "A04": "-.",
                "A05": "-.",
                "A06": "-.",
            },
            2401: {"A04": ":", "A05": ":", "A06": ":"},
        }
        line_color_dict = {
            "A01": "k",
            "A04": "k",
            "A02": "b",
            "A05": "b",
            "A03": "y",
            "A06": "y",
        }
        ignored_list = {(2401, "A01"), (2401, "A02"), (2401, "A03")}
        fig, ax = plt.subplots(figsize=(16, 9))
        for i, g in enumerate(df_lt.groupby(["test_id", "node_id"])):
            """Note: g[0] is the group_id tuple, g[1] is the actual df"""
            if g[0] in ignored_list:
                continue
            new_df = self.timestamp_str_to_series(g[1])
            if var_name == "e_active" or var_name == "e_packet":
                new_df[var_name] = new_df[var_name].divide(1000)
            print(g[0])
            # Convert ns to seconds
            new_df["t_packet"] = new_df["t_packet"].astype("timedelta64[s]")
            # Trim the time range
            new_df = new_df[new_df["t_packet"] < 80000]

            ax.plot(
                new_df["t_packet"],
                new_df[var_name],
                label=tuple_to_label_dict[g[0][0]][g[0][1]],
                color=line_color_dict[g[0][1]],
                linestyle=tuple_to_linestyle_dict[g[0][0]][g[0][1]],
                linewidth=0.8,
            )
            # sns.lineplot(x='t_packet',
            #              y=var_name,
            #              data=new_df,
            #              label=tuple_to_label_dict[g[0][0]][g[0][1]],
            #              color=line_color_dict[g[0][1]],
            #              dashes=True,
            #              markers=True,
            #              linewidth=0.8,
            #              ax=ax)
            # sns.kdeplot(new_df[var_name], label=tuple_to_label_dict[g[0][0]][g[0][1]], cumulative=True, ax=ax)
            # sns.lineplot(x='t_packet', y=var_name, ax=ax, data=new_df)
        plt.axhline(1, ls=":", lw=0.8)
        plt.legend()
        plt.xlabel("Time", fontsize=self.text_size)
        plt.ylabel("Packet energy (J)", fontsize=self.text_size)
        # plt.ylim(bottom=0)
        plt.tight_layout()
        plt.show()

    def plot_energy_breakdown_pie(self, e_dict, phases, ecl_to_plot="0"):
        # inner function
        def generate_portion_legend(e_list, lb_list):
            s = sum(e_list)
            res_list = []
            for i in range(len(e_list)):
                res_list.append("{0} {1:.2f}%".format(lb_list[i], 100 * e_list[i] / s))
            return res_list

        style.use("seaborn-muted")

        fig1, ax1 = plt.subplots(figsize=(6, 3))
        e_list = []
        lb_list = []
        explode_list = [0, 0.3, 0.3, 0.3, 0.3, 0, 0.3, 0]
        for p in phases:
            e_list.append(e_dict["ecl" + ecl_to_plot]["e_{0}_mean".format(p)])
            lb_list.append(p.upper())

        print('Length compare:', len(e_list), len(explode_list))
        wedges, texts = ax1.pie(
            e_list,
            explode=explode_list,
            counterclock=False,
            wedgeprops=dict(width=0.6, linewidth=1),
            startangle=90,
        )

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(
            arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center"
        )

        # Link: https://matplotlib.org/3.1.1/gallery/pie_and_polar_charts/pie_and_donut_labels.html

        wedge_color_dict = {5: "#dfdfdf", 6: "#ef6fa6", 7: "#6fe1ef"}
        for i, p in enumerate(wedges):
            p.set_edgecolor("k")
            p.set_linewidth(0.3)
            if i in [0]:
                ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                connectionstyle = "angle,angleA=0,angleB={}".format(ang)
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                ax1.annotate(
                    lb_list[i],
                    xy=(x, y),
                    xytext=(1.05 * np.sign(x), 1.3 * y),
                    horizontalalignment=horizontalalignment,
                    **kw
                )
            if i in {5, 6, 7}:
                p.set_facecolor(wedge_color_dict[i])
        plt.legend(
            wedges,
            generate_portion_legend(e_list, lb_list),
            loc="best",
            bbox_to_anchor=(0.75, 0.7),
            fontsize=9,
        )

        ax1.axis("equal")
        plt.savefig(
            self.global_path + self.paper_pdf_buf_path
            + "energy_breakdown_pie_ecl{0}.pdf".format(
                ecl_to_plot
            )
        )
        plt.tight_layout()
        plt.show()

    def plot_delivery_rate_vs_modules(self, df):
        mpl.rc("pdf", fonttype=42)
        ue_dict = {
            "BG96": "M1",
            "SARA": "M2",
            "BC66": "M3",
            "ME3616": "M4",
            "BC28": "M5",
            "BC26": "M6",
        }
        ue_plot_order = ["BG96", "SARA", "BC66", "ME3616", "BC28", "BC26"]
        fig = plt.figure(figsize=(8, 6))
        plt.grid(axis="y", linewidth=0.5)
        ax1 = sns.boxenplot(
            x="ue_type",
            y="delivery_rate",
            data=df,
            palette="muted",
            linewidth=2.5,
            order=ue_plot_order,
        )
        ax1.set_xticklabels(["M1", "M2", "M3", "M4", "M5", "M6"], size=19)
        ax1.set_yticks(np.arange(0, 1.1, 0.2))
        ax1.set_yticklabels([0, 0.2, 0.4, 0.6, 0.8, 1.0], size=19)
        ax1.set_xlabel("NB-IoT module", size=23)
        ax1.set_ylabel("Packet delivery rate", size=23)
        plt.subplots_adjust(left=0.12, bottom=0.12, right=0.96, top=0.96)
        plt.savefig(
            self.global_path
            + "/LaTeX Papers/MobiCom 2020 Submission/assets_buffer/delivery_rate_vs_module_type.pdf"
        )
        plt.show()

    def plot_i_max_vs_modules(self, df):
        mpl.rc("pdf", fonttype=42)

        ue_dict = {
            "BG96": "M1",
            "SARA": "M2",
            "BC66": "M3",
            "ME3616": "M4",
            "BC28": "M5",
            "BC26": "M6",
        }
        fig = plt.figure(figsize=(8, 6))
        plt.grid(axis="y", linewidth=0.5)
        df = df[(df.i_max > 20)].copy()
        ax1 = sns.boxenplot(
            x="ue_type", y="i_max", data=df, palette="muted", hue="ecl", linewidth=2.5
        )

        ax1.set_xticklabels(["M1", "M3", "M4", "M5", "M6"], size=19)
        ax1.set_yticklabels(labels=range(-100, 700, 100), size=19)
        ax1.set_xlabel("NB-IoT module", size=23)
        ax1.set_ylabel("Maximum current in a packet (mA)", size=22)

        legend = ax1.legend(title=None, fontsize=18)
        # legend.get_title().set_fontsize(fontsize=16)
        legend.texts[0].set_text("ECL0")
        legend.texts[1].set_text("ECL1")
        legend.texts[2].set_text("ECL2")

        plt.subplots_adjust(left=0.14, bottom=0.13, right=0.96, top=0.96)
        plt.savefig(
            self.global_path
            + "/LaTeX Papers/MobiCom 2020 Submission/assets_buffer/i_max_vs_module_type.pdf"
        )
        plt.show()

    def plot_e_active_vs_modules(self, df):
        ue_dict = {
            "BG96": "M1",
            "SARA": "M2",
            "BC66": "M3",
            "ME3616": "M4",
            "BC28": "M5",
            "BC26": "M6",
        }
        ue_plot_order = ["BG96", "BC66", "ME3616", "BC28", "BC26"]
        fig = plt.figure(figsize=(8, 6))
        plt.grid(axis="y", linewidth=0.5)
        df = df[df["e_active"] < 30]
        ax1 = sns.boxenplot(
            x="ue_type",
            y="e_active",
            data=df,
            palette="muted",
            hue="ecl",
            linewidth=2.5,
            order=ue_plot_order,
        )
        # ax1.set_yticklabels(labels=range(-100, 700, 100), size=16)
        ax1.set_xticklabels(["M1", "M3", "M4", "M5", "M6"], size=18)
        ax1.set_yticklabels(range(-5, 35, 5), size=20)
        ax1.set_xlabel("NB-IoT module", size=20)
        ax1.set_ylabel("Packet active energy (J)", size=20)

        legend = ax1.legend(title=None, fontsize=18)
        # legend.get_title().set_fontsize(fontsize=16)
        legend.texts[0].set_text("ECL0")
        legend.texts[1].set_text("ECL1")
        legend.texts[2].set_text("ECL2")

        plt.subplots_adjust(left=0.12, bottom=0.12, right=0.96, top=0.96)
        plt.savefig(
            self.global_path
            + "/LaTeX Papers/MobiCom 2020 Submission/assets_buffer/e_active_vs_module_type.pdf"
        )
        plt.show()

    def plot_pack_delta_t_vs_module_type(self, df):
        fig = plt.figure(figsize=(8, 6))
        ax1 = sns.boxenplot(
            x="ue_type", y="pack_seconds", data=df, palette="muted", linewidth=2.5
        )
        # ax1.set_xticklabels(['M1', 'M3', 'M4', 'M5', 'M6'], size=18)
        # ax1.set_yticklabels(range(-5, 35, 5), size=20)
        ax1.set_xlabel("NB-IoT module", size=20)
        # ax1.set_ylabel('Packet Active Energy(J)', size=20)

        # legend = ax1.legend(title=None, fontsize=18)
        # legend.texts[0].set_text("ECL0")
        # legend.texts[1].set_text("ECL1")
        # legend.texts[2].set_text("ECL2")
        # plt.grid(axis='y', linewidth=0.5)
        plt.subplots_adjust(left=0.12, bottom=0.12, right=0.96, top=0.96)
        # plt.savefig(self.global_path+'Docs/LaTeX Papers/nbiot_paper_first_draft/assets/e_active_vs_module_type.pdf')
        plt.show()

    def plot_test_delta_t(self, df):
        ue_dict = {
            "BG96": "M1",
            "SARA": "M2",
            "BC66": "M3",
            "ME3616": "M4",
            "BC28": "M5",
            "BC26": "M6",
        }
        ue_plot_order = ["BG96", "SARA", "BC66", "ME3616", "BC28", "BC26"]
        fig = plt.figure(figsize=(8, 6))
        plt.grid(axis="y", linewidth=0.5)
        ax1 = sns.boxenplot(
            x="ue_type",
            y="test_time_estimated",
            data=df,
            palette="muted",
            linewidth=2.5,
            order=ue_plot_order,
        )

        ax1.set_xlabel("NB-IoT module", size=20)
        ax1.set_ylabel("Time duration for 20 UL packets (min)", size=20)
        ax1.set_xticklabels(["M1", "M2", "M3", "M4", "M5", "M6"], size=18)
        ax1.set_yticks(np.arange(0, 65, 10))
        ax1.set_yticklabels(range(0, 65, 10), size=20)
        plt.subplots_adjust(left=0.14, bottom=0.12, right=0.96, top=0.96)
        plt.savefig(
            self.global_path
            + "/LaTeX Papers/MobiCom 2020 Submission/assets_buffer/test_duration_vs_module_type.pdf"
        )
        plt.show()

    def plot_msg3_reschedule_count_bar(self, df):
        mpl.rcParams["ytick.labelsize"] = 14
        mpl.rcParams["xtick.labelsize"] = 14
        fig = plt.figure(figsize=(5, 4.2))
        plt.grid(axis="y", linewidth=0.5)

        ax1 = sns.barplot(
            x="node_id",
            y="retx_rate",
            data=df,
            hue="msg3_rep",
            linewidth=1.5,
            # facecolor=(1, 1, 1, 0),
            palette="Pastel1",
            edgecolor=".2",
            hue_order=[32, 16, 8],
            order=["C11", "C10", "C04", "C02"],
        )
        hatches = [" ", "+", "x", "\\", "*", "o"]

        # Loop over the bars
        for i, thisbar in enumerate(ax1.patches):
            # Set a different hatch for each bar
            thisbar.set_hatch(hatches[(i // 4) % 6])
            # thisbar.set_width(0.07)
        ax1.set_xlabel("NB-IoT node in ECL2", size=16)
        ax1.set_ylabel("Packet with MSG3 retry prob.", size=16)
        ax1.set_xticklabels(["#1", "#2", "#3", "#4"])
        plt.legend(title="MSG3 Repetition in ECL2", fontsize=12, ncol=3)
        # ax1.set_yticks(range(0, 150, 20))
        # ax1.set_yticklabels(range(0, 150, 20), size=20)
        plt.ylim([0, 1])
        plt.tight_layout()

        plt.savefig(
            self.global_path + self.paper_pdf_buf_path
            + "msg3_retx_rate_bar.pdf"
        )

        plt.show()

    def plot_msg3_reschedule_count_box(self, df):
        """Deprecated"""

        df = df[df["msg2_rx"] != 0]
        fig = plt.figure(figsize=(8, 4))
        plt.grid(axis="y", linewidth=0.5)

        ax1 = sns.boxenplot(
            x="node_id",
            y="msg2_rx",
            data=df,
            hue="msg3_rep",
            hue_order=[32, 16, 8],
            order=["C11", "C10", "C01", "C02", "C04"],
        )

        # ax1.set_xlabel('NB-IoT module', size=20)
        # ax1.set_ylabel('Test Duration(min)', size=20)
        # ax1.set_xticklabels(['M1', 'M2', 'M3', 'M4', 'M5', 'M6'], size=18)
        # ax1.set_yticks(range(0, 150, 20))
        # ax1.set_yticklabels(range(0, 150, 20), size=20)
        plt.ylim(bottom=0)
        plt.tight_layout()

        # plt.savefig(self.global_path+
        #     'Docs/LaTeX Papers/nbiot_paper_first_draft/assets/msg3_retx_bar.pdf')

        plt.show()

    def plot_field_test_msg3_reschedule_count(self, df):

        mpl.rcParams["ytick.labelsize"] = 14
        mpl.rcParams["xtick.labelsize"] = 14
        fig = plt.figure(figsize=(8, 4.2))
        plt.grid(axis="y", linewidth=0.5)

        ax1 = sns.barplot(
            x="node_id",
            y="retx_rate",
            data=df,
            linewidth=1.5,
            # facecolor=(1, 1, 1, 0),
            palette="Pastel1",
            edgecolor=".2",
            # hue_order=[32, 16, 8],
            # order=['C11', 'C10', 'C04', 'C02']
        )
        # hatches = [' ', '+', 'x', '\\', '*', 'o']

        # # Loop over the bars
        # for i, thisbar in enumerate(ax1.patches):
        #     # Set a different hatch for each bar
        #     print(i)
        #     thisbar.set_hatch(hatches[(i//4)%6])
        #     # thisbar.set_width(0.07)
        ax1.set_xlabel("NB-IoT node", size=16)
        ax1.set_ylabel("Packet with MSG3 retry prob.", size=16)
        # ax1.set_xticklabels(['ECL2-#1', 'ECL2-#2', 'ECL2-#3', 'ECL2-#4'])
        plt.legend(title="MSG3 Repetition in ECL2", fontsize=12, ncol=3)
        # ax1.set_yticks(range(0, 150, 20))
        # ax1.set_yticklabels(range(0, 150, 20), size=20)
        plt.ylim([0, 1])
        plt.tight_layout()

        # plt.savefig(self.global_path+'Docs/LaTeX Papers/nbiot_paper_first_draft/assets/msg3_retx_rate_bar.pdf')

        plt.show()
