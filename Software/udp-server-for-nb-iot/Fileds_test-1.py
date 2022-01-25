# __author__ = 'Deliang Yang & Xianghui'
# __create__ = '2019.04.11'
import re
import socket
import time
import json
import requests
import threading
import urllib3
import os
import csv
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log_file_path_g = "./log_files/file_test_log/"

###UP
HTTP_IP = '0.0.0.0'
UDP_IP = ''
UDP_PORT = 9678
HTTP_PORT = 9456
udp_sock = ''	#udp socket

Operator_dic = {'China Telecom':'002', 'China Mobile':'001'}
App_Type_dic = {'Water Meter':'001', 'Basement':'002', 'Fire Hydrant':'003',
				'Street Light':'004', 'Palyground':'005', 'Corridor':'006',
				'Brige Hole':'007', 'Above-ground Parking':'008', 'Else':'009'}

# 修改这里的东西
#####
app_type_g = '001'	#必须是3位
sleep_timer_g = '00010'
ul_total_pack_g = '300'
test_id_g = '01'
ul_pack_size_g = '0256'
####

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
random = ''

url_access = 'https://180.101.147.89:8743/iocm/app/sec/v1.1.0/login'
url_down   = 'https://180.101.147.89:8743/iocm/app/cmd/v1.4.0/deviceCommands'
Authertication_message = "appId=VQLomf4wsBJ439Vyq3XDygGureAa&secret=P7PAMbjp_B9NuuAEaGRsu0pcXpEa"
header = {
"app_key":"",
"Authorization":"",
"Content-Type":"application/json"
}

down_message = {
"deviceId": "***",
"command": {
"serviceId": "UP_DOWN",
"method": "DOWN",
"paras": {
"V_Down_Data": '',
}
},
"callbackUrl": "http://129.211.125.101/na/iocm/devNotify/v1.1.0/reportCmdExecResult",
"maxRetransmit":"1",
"expireTime":"0"
}

Authorization_value = ''
appID = 'VQLomf4wsBJ439Vyq3XDygGureAa'
###
def get_key_by_value(dic, value):
	index = 0
	for k, v in dic.items():
		if value==v:
			return k
		else:
			pass
	return None

def Write_log_head(log_file_path, log_head):
	with open(log_file_path, mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(log_head)

def Write_log(log_file_path, log):
	with open(log_file_path, mode='a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(log)

def Get_Lsit_info(list_file_path, list):
	list = []
	file = open(list_file_path, 'r')
	for line in file:
		list.append(line.split('\n')[0])
	file.close()
	# print('---get')
	# print(list)
	return list

def Put_List_info(list_file_path, list):
	# print('---put')
	# print(list)
	file = open(list_file_path, 'w')
	for item in list:
		file.write(item+'\n')
	file.close()


def get_log_dic(file_path, log_dic):

	file = open(file_path, 'r')
	js = file.read()
	log_dic = json.loads(js)   
	file.close()
	return log_dic

def put_log_dic(file_path, log_dic):
	js = json.dumps(log_dic)
	file = open(file_path, 'w')
	file.write(js)
	file.close()

def print_interesting_1():
	length = 5
	str1=" "
	str2="*"
	for I in range(-length,length+1):
		if I < 0:
			print(str1*abs(I)+str2*(length-abs(I)+1))
		elif I == 0:
			print(str2*(length*2+1))
		else:
			print(str1*length+str2*(length-abs(I)+1))
def print_interesting_2():
	for i in range(0,5):
		shixin=chr(9679)
		kongxin = chr(9711)
		for j in range(0,5):
			if i==0 or i==4:
				print(shixin + " ",end="")
			else:
				if j==0:
					print(" "*(j+i+i+i)+shixin,end="")
def Show_Log(Pack_items, log_dic):
	print('\n\n=============历史测试节点信息==================')
	print("UE_ID\tTest_id")
	for i in range(len(log_dic['ue_id'])):
		print("{0}\t{1}".format(log_dic['ue_id'][i], log_dic['test_id'][i]))
	print_interesting_1()
	print("\n***_ Real-Time Log _***\n")
	print("-Node_ID: {0}\n" \
		"-Pack_index: {1}\n" \
		"-Test_ID: {2}\n" \
		"-UE_Type: {3}\n" \
		"-Operator: {4}\n" \
		"-APP_type: {5}\n" \
		"-CSQ: {6}\n" \
		"-ECL: {7}\n" \
		"-SNR: {8}\n" \
		"-RSRP: {9}\n" \
		"-RSRQ: {10}\n" \
		"-Earfcn: {11}\n" \
		"-Pci: {12}\n" \
		"-Cell_Id: {13}\n" \
		"-Temperature: {14}\n" \
		"-Humidity: {15}\n"\
		"-V-Bat: {16}\n" \
		"-UBHV: {17}\n" \
		"-UMHV: {18}\n" \
		"-MSV: {19}\n" \
		"-ERROR_CODE: {20}\n" \
		"-Sleep_Timer: {21}\n" \
		.format(
		Pack_items['UE_ID'],
		Pack_items['Pack_index'],
		Pack_items['Test_ID'], 
		Pack_items['UE_Type'],
		Pack_items['Operator'],
		Pack_items['App_Type'], 
		Pack_items['CSQ'],
		Pack_items['ECl'], 
		Pack_items['SNR'], 
		Pack_items['RSRP'], 
		Pack_items['RSRQ'],
		Pack_items['Earfcn'], 
		Pack_items['Pci'], 
		Pack_items['Cell_Id'], 
		Pack_items['Temperature'], 
		Pack_items['Humidity'], 
		Pack_items['V_Bat'], 
		Pack_items['UBHV'], 
		Pack_items['UMHV'],
		Pack_items['MSV'], 
		Pack_items['ERROR_CODE'],
		Pack_items['Sleep_Timer'],))

def Make_init_msg(Pack_items):
	global Sleep_Timer_g, UL_total_pack_g, app_type_g, test_id_g
	# print("\nDo you want to start up the test for Node-{0}\n Yes (y/Y) or No(Any key except y)?\n".format(Pack_items['UE_ID']))
	# Start_up_c = input('Input your choice:')	# choice for initing test or not
	# if Start_up_c!='y' and Start_up_c!='Y':
	# 	print('Pity! You abandoned her\n')
	# 	return None
	# else:
	# 	print('Let`s configure it!')
	# 	print('What is is the Operator? Choose from belows\n{0}'.format(Operator_dic))
	# 	Operator_c = '000'
	# 	while (get_key_by_value(Operator_dic, Operator_c))==None:
	# 		Operator_c = input('Input your choice:')	# choice for Operator
	# 	print('Yeah! Your choice is: {0}'.format(get_key_by_value(Operator_dic, Operator_c)))

	# 	print('=====================\n')
	# 	print('What is is the APP_type? Choose from belows\n{0}'.format(App_Type_dic))
	# 	App_Type_c = '000'
	# 	while (get_key_by_value(App_Type_dic, App_Type_c))==None:
	# 		App_Type_c = input('Input your choice:')	# choice for APP_type
	# 	print('Yeah! Your choice is: {0}'.format(get_key_by_value(App_Type_dic, App_Type_c)))

	# 	print('=====================\n')
	# 	print('How long do you want the Node sleep?')
	# 	Sleep_Timer_c = '012345'
	# 	tmp_flag = 0
	# 	while not tmp_flag:
	# 		Sleep_Timer_c = input('Input the Sleep_Timer(HMS时分秒，eg:010):')	# choice for APP_type
	# 		if Sleep_Timer_c!='000000' and len(Sleep_Timer_c)==6:
	# 			if 0<=int(Sleep_Timer_c[0:2])<=24 and 0<=int(Sleep_Timer_c[2:4])<=60 and 0<=int(Sleep_Timer_c[4:6])<=60:
	# 				break
	# 			else:
	# 				continue
	# 		else:
	# 			pass
	# 	print('Yeah! Your choice is: {0} Hour-{1} Min-{2} Sec\n'.format(int(Sleep_Timer_c[0:2]),
	# 		int(Sleep_Timer_c[2:4]), int(Sleep_Timer_c[4:6])))
	now_day = int(time.strftime('%Y%m%d',time.localtime(time.time())))
	day_counter = (now_day- int('20200101'))%1000
	if(day_counter != int(Pack_items['Test_ID'][0:3])):
		down_test_id = (str(day_counter) + '01').zfill(5)
	else:
		down_test_id = (str(int(Pack_items['Test_ID'])+1)).zfill(5)
	Pack_items['Test_ID'] = down_test_id
	# print(down_test_id)
	down_pack = 'downflag'+ app_type_g+'|'+sleep_timer_g+'|'+ down_test_id + '|' + ul_total_pack_g + '|' + ul_pack_size_g
	print("*** Configured Node *- {0} -* as below ***".format(Pack_items['UE_ID']))
	print_interesting_2()
	print("\n-App_Type: {0}\n"\
		"-Pack_len: {1}\n"\
		"-UL_Total: {2}\n"\
		"-Test_ID: {3}\n"\
		"-Sleep_Time: {4}"\
		.format(app_type_g, ul_pack_size_g, ul_total_pack_g, down_test_id, sleep_timer_g)
		)
	print_interesting_2()
	return down_pack# Init msg for Node

def get_accesstoken(url, Authertication_message):
	#response = requests.post(url, data= json.dumps(Authertication_message), verify=False, cert=('1.crt', '1.key'), headers=header).text
	response = requests.post(url, data=Authertication_message, verify=False, cert=('client.crt', 'client.key')).text
	#print(response)
	t_Authorization = response.split('"')[3]
	global Authorization_value
	Authorization_value = t_Authorization

def post_down_command(url, dl_msg):
	header['app_key'] = appID
	header['Authorization'] = "Bearer "+Authorization_value
	time_down_start = time.time()
	down_message['command']['paras']['V_Down_Data'] = dl_msg
	response = requests.post(url, data = json.dumps(down_message), verify=False, cert=('client.crt', 'client.key'), headers=header)
	if response.text.find('SENT')!=-1:
		print("Down Data Sent")

def send_down_http(dl_msg):
	get_accesstoken(url_access, Authertication_message)
	post_down_command(url_down, dl_msg)

def send_down_udp(dl_msg, addr):
	print('\n\n*.!.* Sended down init msg *.!.*\n\n')
	global udp_sock
	udp_sock.sendto(dl_msg.encode('utf-8'), addr)

def get_pack_items(msg, Pack_Time):
	# print(Pack_Time+':'+ msg)
	Pack_items = {'UE_ID':'', 'Pack_index':'', 'UE_Type':'', 'Operator':'', 'App_Type':'', 'Sleep_Timer':'',
					'Earfcn':'', 'Pci':'', 'Cell_Id':'', 'ECl':'', 'RSRP':'', 'SNR':'', 'Temperature':'', 'Humidity':'', 'V_Bat':'', 
					'UBHV':'', 'UMHV':'', 'MSV':'', 'ERROR_CODE':'', 'Test_ID':'', 'RSRQ':'', 'CSQ':''}
	msg = msg.split('|')
	Pack_items['UE_ID'] = msg[0]
	Pack_items['Pack_index'] = msg[1]
	Pack_items['UE_Type'] = msg[2]
	Pack_items['Operator'] = msg[3]
	Pack_items['App_Type'] = msg[4]
	Pack_items['Sleep_Timer'] = msg[5]
	Pack_items['CSQ'] = msg[6]
	Pack_items['Earfcn'] = msg[7]
	Pack_items['Pci'] = msg[8]
	Pack_items['Cell_Id'] = msg[9]
	Pack_items['ECl'] = msg[10]
	Pack_items['RSRQ'] = msg[11]
	Pack_items['RSRP'] = msg[12]
	Pack_items['SNR'] = msg[13]
	Pack_items['Temperature'] = msg[14]
	Pack_items['Humidity'] = msg[15]
	Pack_items['V_Bat'] = msg[16]
	Pack_items['UBHV'] = msg[17]
	Pack_items['UMHV'] = msg[18]
	Pack_items['MSV'] = msg[19]
	Pack_items['ERROR_CODE'] = msg[20]
	Pack_items['Test_ID'] = msg[21]
	# print(Pack_items);
	return Pack_items

def parse_http(data, addr):
	Pack_items = {'UE_ID':'', 'Pack_index':'', 'UE_Type':'', 'Operator':'', 'App_Type':'', 'Sleep_Timer':'',
					'Earfcn':'', 'Pci':'', 'Cell_Id':'', 'ECl':'', 'RSRP':'', 'SNR':'', 'Temperature':'', 'Humidity':'', 'V_Bat':'', 
					'UBHV':'', 'UMHV':'', 'MSV':'', 'ERROR_CODE':'', 'Test_ID':'', 'RSRQ':'', 'CSQ':''}
	UE_ID_List = []
	Operator = []
	Log_File_List = []
	Show_item = []
	UE_ID_List_fp = './list_file/UE_ID.txt'
	Log_File_List_fp = './list_file/log_file.txt'
	flag = 0
	UE_ID_List = Get_Lsit_info(UE_ID_List_fp, UE_ID_List)
	Log_File_List = Get_Lsit_info(Log_File_List_fp, Log_File_List)
	log_file_path = ''
	log_file_head = ['UE_ID',\
					'Pack_index',\
					'UE_Type',\
					'Operator',\
					'App_Type',\
					'Sleep_Timer',\
					'CSQ',\
					'Earfcn',\
					'Pci',\
					'Cell_Id',\
					'ECL',\
					'RSRQ',\
					'RSRP',\
					'SNR',\
					'Temperature',\
					'Humidity',\
					'V_Bat',\
					'UBHV',\
					'UMHV',\
					'MSV',\
					'ERROR_CODE',\
					'Test_ID',\
					'Pack Len',\
					'Pack Timer']
	msg_tmp = str(data, encoding = 'utf-8')
	pattern = re.compile(r'[0-9]{3}|[0-9]{3}|')
	match = pattern.findall(msg_tmp)
	if not match or msg_tmp.find('|')==-1:
		print('Rcv msg:', data[0], '\nfrom', addr, 'Len:',len(data))
		print('=================================================')
	else:
		#msg_tmp = str(data,encoding = 'utf-8').split(',')[6]
		down_message['deviceId'] = re.findall(r'"deviceId":"(.+?)"',msg_tmp)[0]
		try:
			msg = re.findall(r'"data":{"UP":"(.+?)"}',msg_tmp)[0]
			# print(msg)
		except IndexError:
			print('Some Error Happened while getting msg\n')
			return
		print(msg)
		Pack_Time = time.strftime('_%Y%m%d_%H%M_%S',time.localtime(time.time()))
		Pack_items = get_pack_items(msg, Pack_Time)
		if int(Pack_items['Pack_index']) == 0:	# Init pack
			Init_msg = Make_init_msg(Pack_items)
			if Init_msg!=None:
				send_down_http(Init_msg)
				print("Sended Init Message\n")
		elif 1<=int(Pack_items['Pack_index'])<=999:
			if int(Pack_items['Pack_index'])== 1:		#首次发包
				if Pack_items['UE_ID'] not in UE_ID_List:	# 全新的节点
					log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Pack_Len_{5}_Pack_Time{6}_{7}" \
					.format(log_file_path_g, Pack_items['App_Type'] , Pack_items['UE_Type'] \
					, Pack_items['Operator'] , Pack_items['UE_ID'], str(len(msg)),Pack_Time ,'.csv')
					UE_ID_List.append(Pack_items['UE_ID'])	#UE_ID加入列表中
					Log_File_List.append(log_file_path)
				else:
					i = 0
					for item in Log_File_List:
						if item.find(Pack_items['UE_ID'])!=-1:
							log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Pack_Len_{5}_Pack_Time{6}_{7}" \
											.format(log_file_path_g, Pack_items['App_Type'] , Pack_items['UE_Type'] \
											, Pack_items['Operator'] , Pack_items['UE_ID'], str(len(msg)), Pack_Time , '.csv')
							Log_File_List[i] = log_file_path	#更新log文件名
							break
						i +=1
				flag = 1
				Write_log_head(log_file_path, log_file_head)
			else:
				for item in UE_ID_List:
					if item.find(Pack_items['UE_ID'])!=-1:
						i = 0
						for item in Log_File_List:
							if item.find(Pack_items['UE_ID'])!=-1:
								log_file_path = Log_File_List[i]
								break
							i +=1
						flag = 1
			if flag==1:
				flag = 0
				for item in Log_File_List:	#根据UE_ID匹配log_file(文件名)
					if item.find(Pack_items['UE_ID']) != -1:
						log_file_path = item
						break
				#存储文件和显示信息
				log = [Pack_items['UE_ID'], \
						Pack_items['Pack_index'], \
						Pack_items['UE_Type'],\
						Pack_items['Operator'],\
						Pack_items['App_Type'],\
						Pack_items['Sleep_Timer'],\
						Pack_items['CSQ'],\
						Pack_items['Earfcn'],\
						Pack_items['Pci'],\
						Pack_items['Cell_Id'],\
						Pack_items['ECl'],\
						Pack_items['RSRQ'],\
						Pack_items['RSRP'],\
						Pack_items['SNR'],\
						Pack_items['Temperature'],\
						Pack_items['Humidity'],\
						Pack_items['V_Bat'],\
						Pack_items['UBHV'],\
						Pack_items['UMHV'],\
						Pack_items['MSV'],\
						Pack_items['ERROR_CODE'],\
						Pack_items['Test_ID'],\
						str(len(msg)),\
						Pack_Time]
				print(log)
				Write_log(log_file_path, log)
				#Show_Log(UE_ID_List, Show_item)
				Put_List_info(UE_ID_List_fp, UE_ID_List)
				Put_List_info(Log_File_List_fp, Log_File_List)
			else:
				print("***Received an invalid message***")
				print("***------***\n")
		else:
			pass

def parse_udp(data, addr):
	flag = 0
	msg = str(data,encoding = 'utf-8')
	Pack_items = {'UE_ID':'', 'Pack_index':'', 'UE_Type':'', 'Operator':'', 'App_Type':'', 'Sleep_Timer':'',
					'Earfcn':'', 'Pci':'', 'Cell_Id':'', 'ECl':'', 'RSRP':'', 'SNR':'', 'Temperature':'', 'Humidity':'', 'V_Bat':'', 
					'UBHV':'', 'UMHV':'', 'MSV':'', 'ERROR_CODE':'', 'Test_ID':'', 'RSRQ':'', 'CSQ':''}

	Show_item = []
	Operator = []

	log_dic = {'ue_id':[], 'log_file_list':[], 'test_id':[]}
	log_dic_file_path = './list_file/log_list.txt'
	# put_log_dic(log_dic_file_path, log_dic)
	log_dic = get_log_dic(log_dic_file_path, log_dic)
	UE_ID_List = log_dic['ue_id']
	Log_File_List = log_dic['log_file_list']
	Test_id_list = log_dic['test_id']

	log_file_path = ''
	log_file_head = ['UE_ID',\
					'Pack_index',\
					'UE_Type',\
					'Operator',\
					'App_Type',\
					'Sleep_Timer',\
					'CSQ',\
					'Earfcn',\
					'Pci',\
					'Cell_Id',\
					'ECL',\
					'RSRQ',\
					'RSRP',\
					'SNR',\
					'Temperature',\
					'Humidity',\
					'V_Bat',\
					'UBHV',\
					'UMHV',\
					'MSV',\
					'ERROR_CODE',\
					'Test_ID',\
					'Pack Len',\
					'Pack Timer']
	Pack_Time = time.strftime('_%Y%m%d_%H%M_%S',time.localtime(time.time()))
	Pack_items = get_pack_items(msg, Pack_Time)
	if msg.find('|')==-1:
		return
	if int(Pack_items['Pack_index']) == 0:	# Init pack
		Init_msg = Make_init_msg(Pack_items)
		if Init_msg!=None:
			send_down_udp(Init_msg, addr)
		if Pack_items['UE_ID'] not in UE_ID_List:	# 全新的节点
			log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Test_id_{5}_Pack_Time{6}_{7}" \
			.format(log_file_path_g, Pack_items['App_Type'] , Pack_items['UE_Type'] \
			, Pack_items['Operator'] , Pack_items['UE_ID'], Pack_items['Test_ID'], Pack_Time ,'.csv')
			UE_ID_List.append(Pack_items['UE_ID'])	#UE_ID加入列表中
			Log_File_List.append(log_file_path)
			Test_id_list.append(Pack_items['Test_ID'])
		else:	# 非全新节点
			log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Test_id_{5}_Pack_Time{6}_{7}" \
							.format(log_file_path_g, Pack_items['App_Type'] , Pack_items['UE_Type'] \
							, Pack_items['Operator'] , Pack_items['UE_ID'], Pack_items['Test_ID'], Pack_Time , '.csv')
			for i in range(len(UE_ID_List)):
				if UE_ID_List[i] == Pack_items['UE_ID']:
					Log_File_List[i] = log_file_path	#更新log文件名
					Test_id_list[i] = Pack_items['Test_ID']
					break
			if i>=len(UE_ID_List):
				print('the UE_ID is fly 000')
		Write_log_head(log_file_path, log_file_head)
		log_dic['ue_id'] = UE_ID_List
		log_dic['log_file_list'] = Log_File_List
		log_dic['test_id'] = Test_id_list
		put_log_dic(log_dic_file_path, log_dic)
	elif 1<=int(Pack_items['Pack_index'])<=999:
		for i in range(len(UE_ID_List)):
			if UE_ID_List[i] == Pack_items['UE_ID']:
				log_file_path = Log_File_List[i]	#更新log文件名
				flag = 1
				break
		if i>=len(UE_ID_List):
			print('the UE_ID is fly 1-999')
			flag = 0;
		if flag == 1:
			#存储文件和显示信息
			log = [Pack_items['UE_ID'], \
						Pack_items['Pack_index'], \
						Pack_items['UE_Type'],\
						Pack_items['Operator'],\
						Pack_items['App_Type'],\
						Pack_items['Sleep_Timer'],\
						Pack_items['CSQ'],\
						Pack_items['Earfcn'],\
						Pack_items['Pci'],\
						Pack_items['Cell_Id'],\
						Pack_items['ECl'],\
						Pack_items['RSRQ'],\
						Pack_items['RSRP'],\
						Pack_items['SNR'],\
						Pack_items['Temperature'],\
						Pack_items['Humidity'],\
						Pack_items['V_Bat'],\
						Pack_items['UBHV'],\
						Pack_items['UMHV'],\
						Pack_items['MSV'],\
						Pack_items['ERROR_CODE'],\
						Pack_items['Test_ID'],\
						str(len(msg)),\
						Pack_Time]
			Write_log(log_file_path, log)
			log_dic['ue_id'] = UE_ID_List
			log_dic['log_file_list'] = Log_File_List
			log_dic['test_id'] = Test_id_list
			put_log_dic(log_dic_file_path, log_dic)
			Show_Log(Pack_items, log_dic)
			# Put_List_info(UE_ID_List_fp, UE_ID_List)
			# Put_List_info(Log_File_List_fp, Log_File_List)
		else:
			print("***Received an invalid message***")
			print("***------***\n")
	else:
		print('pack index is not in 0-999')
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
			parse_http(data,addr)
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

if __name__ == '__main__':
	run()
