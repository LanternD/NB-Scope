from matplotlib import pyplot as plt
import csv

def plot_line_graph():
    file_location = './output_raw_data/20180116_ue_send_success_rate.csv'
    with open(file_location, newline='') as csv_raw_f:
        csv_reader = csv.reader(csv_raw_f, delimiter=',')
        total_list = list(csv_reader)
        csv_raw_f.close()
        print(total_list)
    delay_list = [float(x[0]) for x in total_list]
    rate_list = [float(y[1].strip()) for y in total_list]
    print(delay_list, rate_list)
    plt.plot(delay_list, rate_list, 'g-')
    plt.xlim([0, 0.25])
    plt.ylim([35, 100])
    plt.xlabel('Delay between packets (s)')
    plt.ylabel('Deliver Rate (%)')
    plt.savefig('./generated_figures/deliver_rate_vs_delay.png')
    plt.show()

if __name__ == '__main__':
    plot_line_graph()
