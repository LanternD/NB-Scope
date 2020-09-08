# __author__ = 'Deliang Yang & Xianghui'
# __create__ = '2019.04.11'
# __update__ = '2020.01.18'
import csv
import json
import os
import re
import socket
import threading
import time
from datetime import datetime

import pytz
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log_file_path_g = "./log_files/file_test_log/"

###UP
HTTP_IP = "0.0.0.0"
UDP_IP = ""
UDP_PORT = 9678
HTTP_PORT = 9456
local_timezone = "America/Detroit"
udp_sock = ""  # udp socket

Operator_dic = {
    "SECRET_2": "002",
    "SECRET_1": "001",
}  # We omit this to be consistent with the paper.
App_Type_dic = {
    "Water Meter": "001",
    "Basement": "002",
    "Fire Hydrant": "003",
    "Street Light": "004",
    "Palyground": "005",
    "Corridor": "006",
    "Brige Hole": "007",
    "Above-ground Parking": "008",
    "Else": "009",
}

# Update this part
#####
app_type_g = "001"  # must be 3 digits.
sleep_timer_g = "00005"
ul_total_pack_g = "030"
test_id_g = "01"
ul_pack_size_g = "0256"
####

operator_dict_dy = {"001": "SECRET_1", "002": "SECRET_2", "003": "SECRET_3"}

ue_type_dict_dy = {
    "000": "Undefined",
    "001": "BC28",
    "002": "BC35",
    "003": "BC95",
    "004": "BC26",
    "005": "BC66",
    "006": "BG36",
    "007": "BG96",
    "008": "SARAR410M02B",
    "009": "ME3616",
}

app_type_dict_dy = {
    "001": "Water meter",
    "002": "Smoke sensor",
    "003": "Door lock",
    "004": "Underground parking",
    "005": "Street light",
    "006": "Parking lot",
    "007": "Else",
}

response_text = b"""HTTP/1.1 200 OK
Date: Wed, 10 Apr 2019 13:00:57 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 450
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
Reason: You're speaking plain HTTP to an SSL-enabled server port.<br />
 Instead use the HTTPS scheme to access this URL, please.<br />
</p>
<hr>
<address>Apache/2.4.18 (Ubuntu) Server at localhost.localdomain Port 443</address>
</body></html>
"""
log_file = None
SUM = 0
counter = 0
random = ""

url_access = "https://180.101.147.89:8743/iocm/app/sec/v1.1.0/login"
url_down = "https://180.101.147.89:8743/iocm/app/cmd/v1.4.0/deviceCommands"
Authertication_message = (
    "appId=VQLomf4wsBJ439Vyq3XDygGureAa&secret=P7PAMbjp_B9NuuAEaGRsu0pcXpEa"
)
header = {"app_key": "", "Authorization": "", "Content-Type": "application/json"}

down_message = {
    "deviceId": "***",
    "command": {
        "serviceId": "UP_DOWN",
        "method": "DOWN",
        "paras": {"V_Down_Data": "",},
    },
    "callbackUrl": "http://129.211.125.101/na/iocm/devNotify/v1.1.0/reportCmdExecResult",
    "maxRetransmit": "1",
    "expireTime": "0",
}

Authorization_value = ""
appID = "VQLomf4wsBJ439Vyq3XDygGureAa"
###
def get_key_by_value(dic, value):
    index = 0
    for k, v in dic.items():
        if value == v:
            return k
        else:
            pass
    return None


def Write_log_head(log_file_path, log_head):
    with open(log_file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(log_head)


def Write_log(log_file_path, log):
    with open(log_file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(log)


def Get_Lsit_info(list_file_path, list):
    list = []
    file = open(list_file_path, "r")
    for line in file:
        list.append(line.split("\n")[0])
    file.close()
    # print('---get')
    # print(list)
    return list


def Put_List_info(list_file_path, list):
    # print('---put')
    # print(list)
    file = open(list_file_path, "w")
    for item in list:
        file.write(item + "\n")
    file.close()


def get_log_dic(file_path, log_dic):

    file = open(file_path, "r")
    js = file.read()
    log_dic = json.loads(js)
    file.close()
    return log_dic


def put_log_dic(file_path, log_dic):
    js = json.dumps(log_dic)
    file = open(file_path, "w")
    file.write(js)
    file.close()


def print_interesting_1():
    length = 2
    str1 = " "
    str2 = "*"
    for I in range(-length, length + 1):
        if I < 0:
            print(str1 * abs(I) + str2 * (length - abs(I) + 1))
        elif I == 0:
            print(str2 * (length * 2 + 1))
        else:
            print(str1 * length + str2 * (length - abs(I) + 1))


def print_interesting_2():
    for i in range(0, 5):
        shixin = chr(9679)
        kongxin = chr(9711)
        for j in range(0, 5):
            if i == 0 or i == 4:
                print(shixin + " ", end="")
            else:
                if j == 0:
                    print(" " * (j + i + i + i) + shixin, end="")


def Show_history(log_dic):
    print("\n\n============= Packet History ==============")
    print("UE_ID\tTest_id\t\tPack_index\tReceived Timestamp")
    for i in range(len(log_dic["ue_id"])):
        print(
            "{0}\t{1}\t\t{2}\t\t{3}".format(
                log_dic["ue_id"][i],
                log_dic["test_id"][i],
                log_dic["pack_index"][i],
                log_dic["pack_time"][i],
            )
        )


def show_log_dy(Pack_items, log_dic):
    print("===================================")
    print(
        "Current Time: {0}".format(
            datetime.now(pytz.timezone(local_timezone)).strftime(
                "%Y-%m-%d %H:%M:%S (%z)"
            )
        )
    )
    print(
        "Basic: \033[93m{0}\033[00m | \033[93m{1}\033[00m | {2} | {3}".format(
            Pack_items["UE_ID"],
            ue_type_dict_dy[Pack_items["UE_Type"]],
            operator_dict_dy[Pack_items["Operator"]],
            app_type_dict_dy[Pack_items["App_Type"]],
        )
    )
    print(
        "Test ID: \033[94m{0}\033[00m | Packet#: \033[94m{1}/{2}\033[00m".format(
            Pack_items["Test_ID"], int(Pack_items["Pack_index"]), int(ul_total_pack_g)
        )
    )
    print(
        "Radio info: ECL=\033[92m{0}\033[00m CSQ={1} SNR=\033[92m{2}\033[00m RSRP=\033[92m{3}\033[00m RSRQ={4} EARFCN={5} CID={6} PCI={7}".format(
            Pack_items["ECl"],
            Pack_items["CSQ"],
            Pack_items["SNR"],
            Pack_items["RSRP"],
            Pack_items["RSRQ"],
            Pack_items["Earfcn"],
            Pack_items["Cell_Id"],
            Pack_items["Pci"],
        )
    )
    print(
        "Sensor reading: T={0}Deg | RH={1}% | V_Batt={2} mV".format(
            Pack_items["Temperature"], Pack_items["Humidity"], Pack_items["V_Bat"]
        )
    )
    print(
        "Versions: Base board HW={0} | Module board HW={1} | MCU SW={2}".format(
            Pack_items["UBHV"], Pack_items["UMHV"], Pack_items["MSV"]
        )
    )
    print(
        "Error code last run: \033[91m{0}\033[00m | Sleep timer: {1} s".format(
            Pack_items["ERROR_CODE"], int(Pack_items["Sleep_Timer"])
        )
    )
    print("===================================")


def Show_Log(Pack_items, log_dic):
    print_interesting_1()
    print("\n***_ Real-Time Log _***")
    print(
        "Current Time:{0}\n".format(
            time.strftime("%Hh_%Mm_%Ss", time.localtime(time.time()))
        )
    )
    print(
        "-Node_ID: {0}    -----------     "
        "-Pack_index: {1}\n"
        "-Test_ID: {2}    -----------     "
        "-UE_Type: {3}\n"
        "-Operator: {4}    -----------     "
        "-APP_type: {5}\n"
        "-CSQ: {6}    -----------     "
        "-ECL: {7}\n"
        "-SNR: {8}    -----------     "
        "-RSRP: {9}\n"
        "-RSRQ: {10}    -----------     "
        "-Earfcn: {11}\n"
        "-Pci: {12}    -----------     "
        "-Cell_Id: {13}\n"
        "-Temperature: {14}    -----------     "
        "-Humidity: {15}\n"
        "-V-Bat: {16}    -----------     "
        "-UBHV: {17}\n"
        "-UMHV: {18}    -----------     "
        "-MSV: {19}\n"
        "-ERROR_CODE: {20}    -----------     "
        "-Sleep_Timer: {21}\n".format(
            Pack_items["UE_ID"],
            Pack_items["Pack_index"],
            Pack_items["Test_ID"],
            Pack_items["UE_Type"],
            Pack_items["Operator"],
            Pack_items["App_Type"],
            Pack_items["CSQ"],
            Pack_items["ECl"],
            Pack_items["SNR"],
            Pack_items["RSRP"],
            Pack_items["RSRQ"],
            Pack_items["Earfcn"],
            Pack_items["Pci"],
            Pack_items["Cell_Id"],
            Pack_items["Temperature"],
            Pack_items["Humidity"],
            Pack_items["V_Bat"],
            Pack_items["UBHV"],
            Pack_items["UMHV"],
            Pack_items["MSV"],
            Pack_items["ERROR_CODE"],
            Pack_items["Sleep_Timer"],
        )
    )


def Make_init_msg(Pack_items):
    global Sleep_Timer_g, UL_total_pack_g, app_type_g, test_id_g
    # now_day = int(time.strftime("%Y%m%d", time.localtime(time.time())))
    # day_counter = (now_day - int("20200101")) % 1000

    # By DY:
    day_counter = (
        datetime.now(pytz.timezone(local_timezone)).timetuple().tm_yday
    )  # int type

    if day_counter != int(Pack_items["Test_ID"][0:3]):
        down_test_id = (str(day_counter) + "01").zfill(5)
    else:
        down_test_id = (str(int(Pack_items["Test_ID"]) + 1)).zfill(5)
    Pack_items["Test_ID"] = down_test_id
    # print(down_test_id)
    down_pack = (
        "downflag"
        + app_type_g
        + "|"
        + sleep_timer_g
        + "|"
        + down_test_id
        + "|"
        + ul_total_pack_g
        + "|"
        + ul_pack_size_g
    )
    print("\n*** Configured Node *- {0} -* as below ***".format(Pack_items["UE_ID"]))
    print_interesting_2()
    print(
        "\n- App Type:\t {0}\n"
        "- Pack_len: \t {1}\n"
        "- UL Total:\t {2}\n"
        "- Test ID:\t {3}\n"
        "- Sleep Timer \t {4}".format(
            app_type_g, ul_pack_size_g, ul_total_pack_g, down_test_id, sleep_timer_g
        )
    )
    print_interesting_2()
    return down_pack  # Init msg for Node


def get_accesstoken(url, Authertication_message):
    response = requests.post(
        url,
        data=Authertication_message,
        verify=False,
        cert=("client.crt", "client.key"),
    ).text
    # print(response)
    t_Authorization = response.split('"')[3]
    global Authorization_value
    Authorization_value = t_Authorization


def post_down_command(url, dl_msg):
    header["app_key"] = appID
    header["Authorization"] = "Bearer " + Authorization_value
    time_down_start = time.time()
    down_message["command"]["paras"]["V_Down_Data"] = dl_msg
    response = requests.post(
        url,
        data=json.dumps(down_message),
        verify=False,
        cert=("client.crt", "client.key"),
        headers=header,
    )
    if response.text.find("SENT") != -1:
        print("Down Data Sent")


def send_down_http(dl_msg):
    get_accesstoken(url_access, Authertication_message)
    post_down_command(url_down, dl_msg)


def send_down_udp(dl_msg, addr):
    global udp_sock
    udp_sock.sendto(dl_msg.encode("utf-8"), addr)


def get_pack_items(msg, Pack_Time):
    # print(Pack_Time+':'+ msg)
    Pack_items = {
        "UE_ID": "",
        "Pack_index": "",
        "UE_Type": "",
        "Operator": "",
        "App_Type": "",
        "Sleep_Timer": "",
        "Earfcn": "",
        "Pci": "",
        "Cell_Id": "",
        "ECl": "",
        "RSRP": "",
        "SNR": "",
        "Temperature": "",
        "Humidity": "",
        "V_Bat": "",
        "UBHV": "",
        "UMHV": "",
        "MSV": "",
        "ERROR_CODE": "",
        "Test_ID": "",
        "RSRQ": "",
        "CSQ": "",
    }
    msg = msg.split("|")
    Pack_items["UE_ID"] = msg[0]
    Pack_items["Pack_index"] = msg[1]
    Pack_items["UE_Type"] = msg[2]
    Pack_items["Operator"] = msg[3]
    Pack_items["App_Type"] = msg[4]
    Pack_items["Sleep_Timer"] = msg[5]
    Pack_items["CSQ"] = msg[6]
    Pack_items["Earfcn"] = msg[7]
    Pack_items["Pci"] = msg[8]
    Pack_items["Cell_Id"] = msg[9]
    Pack_items["ECl"] = msg[10]
    Pack_items["RSRQ"] = msg[11]
    Pack_items["RSRP"] = msg[12]
    Pack_items["SNR"] = msg[13]
    Pack_items["Temperature"] = msg[14]
    Pack_items["Humidity"] = msg[15]
    Pack_items["V_Bat"] = msg[16]
    Pack_items["UBHV"] = msg[17]
    Pack_items["UMHV"] = msg[18]
    Pack_items["MSV"] = msg[19]
    Pack_items["ERROR_CODE"] = msg[20]
    Pack_items["Test_ID"] = msg[21]
    # print(Pack_items);
    return Pack_items


def parse_http(data, addr):
    Pack_items = {
        "UE_ID": "",
        "Pack_index": "",
        "UE_Type": "",
        "Operator": "",
        "App_Type": "",
        "Sleep_Timer": "",
        "Earfcn": "",
        "Pci": "",
        "Cell_Id": "",
        "ECl": "",
        "RSRP": "",
        "SNR": "",
        "Temperature": "",
        "Humidity": "",
        "V_Bat": "",
        "UBHV": "",
        "UMHV": "",
        "MSV": "",
        "ERROR_CODE": "",
        "Test_ID": "",
        "RSRQ": "",
        "CSQ": "",
    }
    UE_ID_List = []
    Operator = []
    Log_File_List = []
    Show_item = []
    UE_ID_List_fp = "./list_file/UE_ID.txt"
    Log_File_List_fp = "./list_file/log_file.txt"
    flag = 0
    UE_ID_List = Get_Lsit_info(UE_ID_List_fp, UE_ID_List)
    Log_File_List = Get_Lsit_info(Log_File_List_fp, Log_File_List)
    log_file_path = ""
    log_file_head = [
        "UE_ID",
        "Pack_index",
        "UE_Type",
        "Operator",
        "App_Type",
        "Sleep_Timer",
        "CSQ",
        "Earfcn",
        "Pci",
        "Cell_Id",
        "ECL",
        "RSRQ",
        "RSRP",
        "SNR",
        "Temperature",
        "Humidity",
        "V_Bat",
        "UBHV",
        "UMHV",
        "MSV",
        "ERROR_CODE",
        "Test_ID",
        "Pack Len",
        "Pack Timer",
    ]
    msg_tmp = str(data, encoding="utf-8")
    pattern = re.compile(r"[0-9]{3}|[0-9]{3}|")
    match = pattern.findall(msg_tmp)
    if not match or msg_tmp.find("|") == -1:
        print("Rcv msg:", data[0], "\nfrom", addr, "Len:", len(data))
        print("=================================================")
    else:
        # msg_tmp = str(data,encoding = 'utf-8').split(',')[6]
        down_message["deviceId"] = re.findall(r'"deviceId":"(.+?)"', msg_tmp)[0]
        try:
            msg = re.findall(r'"data":{"UP":"(.+?)"}', msg_tmp)[0]
            # print(msg)
        except IndexError:
            print("Some Error Happened while getting msg\n")
            return
        # print(msg[:115])
        # Pack_Time = time.strftime("_%Y%m%d_%H%M_%S", time.localtime(time.time()))
        Pack_Time = datetime.now(pytz.timezone(local_timezone)).strftime(
            "%Y%m%d_%H%M%S"
        )  # Added by DY
        Pack_items = get_pack_items(msg, Pack_Time)
        if int(Pack_items["Pack_index"]) == 0:  # Init pack
            Init_msg = Make_init_msg(Pack_items)
            if Init_msg != None:
                send_down_http(Init_msg)
                print("Sended Init Message\n")
        elif 1 <= int(Pack_items["Pack_index"]) <= 999:
            if int(Pack_items["Pack_index"]) == 1:  # First packet
                if Pack_items["UE_ID"] not in UE_ID_List:  # New node
                    log_file_path = (
                        log_file_path_g
                        + "{0}_{1}_T_{2}_App_{3}_UE_{4}_Op_{5}{6}".format(
                            Pack_items["UE_ID"],
                            Pack_items["Test_ID"],
                            Pack_Time,
                            Pack_items["App_Type"],
                            Pack_items["UE_Type"],
                            Pack_items["Operator"],
                            ".csv",
                        )
                    )
                    UE_ID_List.append(Pack_items["UE_ID"])  # Add UE_ID to the list
                    Log_File_List.append(log_file_path)
                else:
                    i = 0
                    for item in Log_File_List:
                        if item.find(Pack_items["UE_ID"]) != -1:
                            log_file_path = (
                                log_file_path_g
                                + "{0}_{1}_T_{2}_App_{3}_UE_{4}_Op_{5}{6}".format(
                                    Pack_items["UE_ID"],
                                    Pack_items["Test_ID"],
                                    Pack_Time,
                                    Pack_items["App_Type"],
                                    Pack_items["UE_Type"],
                                    Pack_items["Operator"],
                                    ".csv",
                                )
                            )
                            Log_File_List[i] = log_file_path  # Update log file name
                            break
                        i += 1
                flag = 1
                Write_log_head(log_file_path, log_file_head)
            else:
                for item in UE_ID_List:
                    if item.find(Pack_items["UE_ID"]) != -1:
                        i = 0
                        for item in Log_File_List:
                            if item.find(Pack_items["UE_ID"]) != -1:
                                log_file_path = Log_File_List[i]
                                break
                            i += 1
                        flag = 1
            if flag == 1:
                flag = 0
                for item in Log_File_List:  # Match UE_ID by log filename
                    if item.find(Pack_items["UE_ID"]) != -1:
                        log_file_path = item
                        break
                # 存储文件和显示信息
                log = [
                    Pack_items["UE_ID"],
                    Pack_items["Pack_index"],
                    Pack_items["UE_Type"],
                    Pack_items["Operator"],
                    Pack_items["App_Type"],
                    Pack_items["Sleep_Timer"],
                    Pack_items["CSQ"],
                    Pack_items["Earfcn"],
                    Pack_items["Pci"],
                    Pack_items["Cell_Id"],
                    Pack_items["ECl"],
                    Pack_items["RSRQ"],
                    Pack_items["RSRP"],
                    Pack_items["SNR"],
                    Pack_items["Temperature"],
                    Pack_items["Humidity"],
                    Pack_items["V_Bat"],
                    Pack_items["UBHV"],
                    Pack_items["UMHV"],
                    Pack_items["MSV"],
                    Pack_items["ERROR_CODE"],
                    Pack_items["Test_ID"],
                    str(len(msg)),
                    Pack_Time,
                ]
                print(log)
                Write_log(log_file_path, log)
                # Show_Log(UE_ID_List, Show_item)
                Put_List_info(UE_ID_List_fp, UE_ID_List)
                Put_List_info(Log_File_List_fp, Log_File_List)
            else:
                print("\n\n*** !!! Received an invalid message !!! ***\n\n")
        else:
            pass


def parse_udp(data, addr):
    flag = 0
    msg = str(data, encoding="utf-8")
    # print(msg)
    Pack_items = {
        "UE_ID": "",
        "Pack_index": "",
        "UE_Type": "",
        "Operator": "",
        "App_Type": "",
        "Sleep_Timer": "",
        "Earfcn": "",
        "Pci": "",
        "Cell_Id": "",
        "ECl": "",
        "RSRP": "",
        "SNR": "",
        "Temperature": "",
        "Humidity": "",
        "V_Bat": "",
        "UBHV": "",
        "UMHV": "",
        "MSV": "",
        "ERROR_CODE": "",
        "Test_ID": "",
        "RSRQ": "",
        "CSQ": "",
    }

    Show_item = []
    Operator = []

    log_dic = {
        "ue_id": [],
        "log_file_list": [],
        "test_id": [],
        "pack_index": [],
        "pack_time": [],
    }
    log_dic_file_path = "./list_file/log_list_1.txt"
    # put_log_dic(log_dic_file_path, log_dic) #only once

    log_dic = get_log_dic(log_dic_file_path, log_dic)
    Show_history(log_dic)

    UE_ID_List = log_dic["ue_id"]
    Log_File_List = log_dic["log_file_list"]
    Test_id_list = log_dic["test_id"]
    Pack_index_list = log_dic["pack_index"]
    Pack_Time_list = log_dic["pack_time"]

    log_file_path = ""
    log_file_head = [
        "UE_ID",
        "Pack_index",
        "UE_Type",
        "Operator",
        "App_Type",
        "Sleep_Timer",
        "CSQ",
        "Earfcn",
        "Pci",
        "Cell_Id",
        "ECL",
        "RSRQ",
        "RSRP",
        "SNR",
        "Temperature",
        "Humidity",
        "V_Bat",
        "UBHV",
        "UMHV",
        "MSV",
        "ERROR_CODE",
        "Test_ID",
        "Pack Len",
        "Pack Timer",
    ]
    # Pack_Time = time.strftime("_%Y%m%d_%H%M_%S", time.localtime(time.time()))

    # By DY
    Pack_Time = datetime.now(pytz.timezone(local_timezone)).strftime("%Y%m%d_%H%M%S")

    Pack_items = get_pack_items(msg, Pack_Time)
    if msg.find("|") == -1:
        return
    if int(Pack_items["Pack_index"]) == 0:  # Init pack
        Init_msg = Make_init_msg(Pack_items)
        if Init_msg != None:
            send_down_udp(Init_msg, addr)
        if Pack_items["UE_ID"] not in UE_ID_List:  # Existing node
            log_file_path = (
                log_file_path_g
                + "{0}_{1}_T_{2}_App_{3}_UE_{4}_Op_{5}{6}".format(
                    Pack_items["UE_ID"],
                    Pack_items["Test_ID"],
                    Pack_Time,
                    Pack_items["App_Type"],
                    Pack_items["UE_Type"],
                    Pack_items["Operator"],
                    ".csv",
                )
            )
            UE_ID_List.append(Pack_items["UE_ID"])
            Log_File_List.append(log_file_path)
            Test_id_list.append(Pack_items["Test_ID"])
            Pack_index_list.append(Pack_items["Pack_index"])
            Pack_Time_list.append(
                datetime.now(pytz.timezone(local_timezone)).strftime("%H:%M:%S")
            )

        else:  # Existing node
            log_file_path = (
                log_file_path_g
                + "{0}_{1}_T_{2}_App_{3}_UE_{4}_Op_{5}{6}".format(
                    Pack_items["UE_ID"],
                    Pack_items["Test_ID"],
                    Pack_Time,
                    Pack_items["App_Type"],
                    Pack_items["UE_Type"],
                    Pack_items["Operator"],
                    ".csv",
                )
            )
            i = 0
            for i in range(len(UE_ID_List)):
                if UE_ID_List[i] == Pack_items["UE_ID"]:
                    Log_File_List[i] = log_file_path  # Update log file name
                    Test_id_list[i] = Pack_items["Test_ID"]
                    Pack_index_list[i] = Pack_items["Pack_index"]
                    Pack_Time_list[i] = datetime.now(
                        pytz.timezone(local_timezone)
                    ).strftime("%H:%M:%S")
                    break
            if i >= len(UE_ID_List):
                print("the UE_ID is fly 000")

        Write_log_head(log_file_path, log_file_head)
        log_dic["ue_id"] = UE_ID_List
        log_dic["log_file_list"] = Log_File_List
        log_dic["test_id"] = Test_id_list
        log_dic["pack_index"] = Pack_index_list
        log_dic["pack_time"] = Pack_Time_list
        put_log_dic(log_dic_file_path, log_dic)
    elif 1 <= int(Pack_items["Pack_index"]) <= 999:
        for i in range(len(UE_ID_List)):
            if UE_ID_List[i] == Pack_items["UE_ID"]:
                log_file_path = Log_File_List[i]
                Pack_index_list[i] = Pack_items["Pack_index"]
                # DY:
                Pack_Time_list[i] = datetime.now(
                    pytz.timezone(local_timezone)
                ).strftime("%Y-%m-%d %H:%M:%S")
                flag = 1
                break
        i = 0
        if i >= len(UE_ID_List):
            print("the UE_ID is fly 1-999")
            flag = 0
        if flag == 1:
            # Storing and updating information
            log = [
                Pack_items["UE_ID"],
                Pack_items["Pack_index"],
                Pack_items["UE_Type"],
                Pack_items["Operator"],
                Pack_items["App_Type"],
                Pack_items["Sleep_Timer"],
                Pack_items["CSQ"],
                Pack_items["Earfcn"],
                Pack_items["Pci"],
                Pack_items["Cell_Id"],
                Pack_items["ECl"],
                Pack_items["RSRQ"],
                Pack_items["RSRP"],
                Pack_items["SNR"],
                Pack_items["Temperature"],
                Pack_items["Humidity"],
                Pack_items["V_Bat"],
                Pack_items["UBHV"],
                Pack_items["UMHV"],
                Pack_items["MSV"],
                Pack_items["ERROR_CODE"],
                Pack_items["Test_ID"],
                str(len(msg)),
                Pack_Time,
            ]
            Write_log(log_file_path, log)
            log_dic["ue_id"] = UE_ID_List
            log_dic["log_file_list"] = Log_File_List
            log_dic["test_id"] = Test_id_list
            log_dic["pack_index"] = Pack_index_list
            log_dic["pack_time"] = Pack_Time_list
            put_log_dic(log_dic_file_path, log_dic)
            # Show_Log(Pack_items, log_dic)
            show_log_dy(Pack_items, log_dic)
        else:
            print("\n\n*** !!! Received an invalid message !!! ***\n\n")

    else:
        print("pack index is not in 0-999")
        pass


def udp_receiver():
    global udp_sock
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = udp_sock.recvfrom(1024)
        parse_udp(data, addr)


def http_receiver():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HTTP_IP, HTTP_PORT))
    sock.listen(4)
    while True:
        c, addr = sock.accept()
        try:
            data = c.recv(1024)
            c.send(response_text)
            parse_http(data, addr)
        except socket.error as e:
            print(e)
        finally:
            c.close()


def run():
    # creat 2 thread for udp port and http port

    try:
        thread_udp_receiver = threading.Thread(target=udp_receiver)
        thread_http_receriver = threading.Thread(target=http_receiver)
        thread_http_receriver.start()
        thread_udp_receiver.start()
    except:
        print("Error: unable to start thread\n")


if __name__ == "__main__":
    run()
