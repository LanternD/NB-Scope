import time

from PostFieldTestProcessor import PostFieldTestProcessor


def post_ft_processing_main(function_switch):
    whoami = 'dy'
    # whoami = 'ls'
    pftp = PostFieldTestProcessor(whoami)
    t0 = time.time()
    pftp.load_csv()
    pftp.calculate_overview_stats()

    if function_switch == 0:
        pftp.get_field_test_stats()
    elif function_switch == 1:
        pftp.visualize_packet_energy_outdoor_map('us')
    elif function_switch == 2:
        pftp.visualize_packet_energy_indoor_map('us')
    elif function_switch == 3:
        pftp.visualize_energy_vs_app('e_active_mean')
    elif function_switch == 31:
        pftp.visualize_energy_vs_app_bc26_bc66('e_active_mean')
    elif function_switch == 4:
        pftp.visualize_ecl_distribution_by_app('v2')
    elif function_switch == 5:
        pftp.visualize_rsrp_snr_kde_by_app_op()
    elif function_switch == 6:
        pftp.visualize_msg3_data_rep(plot_option='bar3d')
    elif function_switch == 7:
        pftp.visualize_long_term_field_test()
    elif function_switch == 8:
        pftp.get_cell_info()
    elif function_switch == 9:
        pftp.visualize_energy_breakdown()
    elif function_switch == 10:
        pftp.visualize_msg3_reschedule_experiment_results()
    elif function_switch == 11:
        pftp.visualize_field_test_msg3_scheduling()
    elif function_switch == 50:
        pftp.reduce_pdf_figure_filesize_by_gs()

    print('Execution time: {0:.3f}'.format(time.time()-t0))


if __name__ == '__main__':
    post_ft_processing_main(function_switch=31)
