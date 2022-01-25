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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###UP
HTTP_IP = '0.0.0.0'
UDP_IP = ''
UDP_PORT = 9678
HTTP_PORT = 9456
udp_sock = ''	#udp socket

Operator_dic = {'China Telecom':'001', 'China Mobile':'002'}
App_Type_dic = {'Water Meter':'001', 'Basement':'002', 'Fire Hydrant':'003',
				'Street Light':'004', 'Palyground':'005', 'Corridor':'006',
				'Brige Hole':'007', 'Above-ground Parking':'008', 'Else':'009'}
Sleep_Timer_g = '010'

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

###

###Down


url_access = 'https://180.101.147.89:8743/iocm/app/sec/v1.1.0/login'
url_down   = 'https://180.101.147.89:8743/iocm/app/cmd/v1.4.0/deviceCommands'
Authertication_message = "appId=VQLomf4wsBJ439Vyq3XDygGureAa&secret=P7PAMbjp_B9NuuAEaGRsu0pcXpEa"
header = {
"app_key":"",
"Authorization":"",
"Content-Type":"application/json"
}

# down_message = {
# "deviceId": "***",
# "command": {
# "serviceId": "UP_DOWN",
# "method": "DOWN",
# "paras": {
# "Down_data": '',
# }
# },
# "callbackUrl": "http://129.211.125.101/na/iocm/devNotify/v1.1.0/reportCmdExecResult",
# "maxRetransmit":"1",
# "expireTime":"0"
# }
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
def Show_Log(UE_ID_List, Show_item):
	print('==========================================')
	print('UE_ID\tIndex\tStandBy_Timer\tOperator\tPackLen\t\tPack_Time\t\tIt`s You?')
	for item in UE_ID_List:
		if Show_item[0] == item:	#当前UE
			print('{0}\t{1}\t{2}\t\t{3}\t\t{4}\t\t{5}\t{6}'.format(Show_item[0], Show_item[1], Show_item[2], Show_item[3], Show_item[4], Show_item[5], '*-.-*'))
		else:
			print(item)
	print('==========================================\n')
def Make_init_msg(Pack_items):
	global Operator_dic, App_Type_dic, Sleep_Timer_g
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
	App_Type_c = "002";
	Sleep_Timer_c ="000010";
	down_pack = 'downflag'+ App_Type_c+'|'+Sleep_Timer_c+'|'+ Pack_items['Test_ID'] + '|'
	down_pack = down_pack+str(len(down_pack)) 
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
	print('Sending dl udp msg',dl_msg)
	global udp_sock
	udp_sock.sendto(dl_msg.encode('utf-8'), addr)
def get_pack_items(msg, Pack_Time):
	print(Pack_Time+':'+ msg)
	Pack_items = {'UE_ID':'', 'Pack_index':'', 'UE_Type':'', 'Operator':'', 'App_Type':'', 'Sleep_Timer':'',
					'Earfcn':'', 'Pci':'', 'Cell_Id':'', 'ECl':'', 'RSRP':'', 'SNR':'', 'Temperature':'', 'Humidity':'', 'V_Bat':'', 
					'UBHV':'', 'UMHV':'', 'MSV':'', 'ERROR_CODE':'', 'Test_ID':''}
	msg = msg.split('|')
	print(msg[0])
	print(msg[-1])
	Pack_items['UE_ID'] = msg[0]
	Pack_items['Pack_index'] = msg[1]
	Pack_items['UE_Type'] = msg[2]
	Pack_items['Operator'] = msg[3]
	Pack_items['App_Type'] = msg[4]
	Pack_items['Sleep_Timer'] = msg[5]
	Pack_items['Earfcn'] = msg[6]
	Pack_items['Pci'] = msg[7]
	Pack_items['Cell_Id'] = msg[8]
	Pack_items['ECl'] = msg[9]
	Pack_items['RSRP'] = msg[10]
	Pack_items['SNR'] = msg[11]
	Pack_items['Temperature'] = msg[12]
	Pack_items['Humidity'] = msg[13]
	Pack_items['V_Bat'] = msg[14]
	Pack_items['UBHV'] = msg[15]
	Pack_items['UMHV'] = msg[16]
	Pack_items['MSV'] = msg[17]
	Pack_items['ERROR_CODE'] = msg[18]
	Pack_items['Test_ID'] = msg[19]

	return Pack_items
def parse_http(data, addr):
	Pack_items = {'UE_ID':'', 'Pack_index':'', 'UE_Type':'', 'Operator':'', 'App_Type':'', 'Sleep_Timer':'',
					'Earfcn':'', 'Pci':'', 'Cell_Id':'', 'ECl':'', 'RSRP':'', 'SNR':'', 'Temperature':'', 'Humidity':'', 'V_Bat':'', 
					'UBHV':'', 'UMHV':'', 'MSV':'', 'ERROR_CODE':'', 'Test_ID':''}
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
					'Earfcn',\
					'Pci',\
					'Cell_Id',\
					'ECL',\
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
			if Pack_items['Pack_index']=='001':		#首次发包
				if Pack_items['UE_ID'] not in UE_ID_List:	# 全新的节点
					log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Pack_Len_{5}_Pack_Time{6}_{7}" \
					.format('./log_files/', Pack_items['App_Type'] , Pack_items['UE_Type'] \
					, Pack_items['Operator'] , Pack_items['UE_ID'], str(len(msg)),Pack_Time ,'.csv')
					UE_ID_List.append(Pack_items['UE_ID'])	#UE_ID加入列表中
					Log_File_List.append(log_file_path)
				else:
					i = 0
					for item in Log_File_List:
						if item.find(Pack_items['UE_ID'])!=-1:
							log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Pack_Len_{5}_Pack_Time{6}_{7}" \
											.format('./log_files/', Pack_items['App_Type'] , Pack_items['UE_Type'] \
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
						Pack_items['Earfcn'],\
						Pack_items['Pci'],\
						Pack_items['Cell_Id'],\
						Pack_items['ECl'],\
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
	msg = str(data,encoding = 'utf-8')
	Pack_items = {'UE_ID':'', 'Pack_index':'', 'UE_Type':'', 'Operator':'', 'App_Type':'', 'Sleep_Timer':'',
					'Earfcn':'', 'Pci':'', 'Cell_Id':'', 'ECl':'', 'RSRP':'', 'SNR':'', 'Temperature':'', 'Humidity':'', 'V_Bat':'', 
					'UBHV':'', 'UMHV':'', 'MSV':'', 'ERROR_CODE':'', 'Test_ID':''}
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
					'Earfcn',\
					'Pci',\
					'Cell_Id',\
					'ECL',\
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
			print("Sended Init Message\n")
	elif 1<=int(Pack_items['Pack_index'])<=999:
		if Pack_items['Pack_index']=='001':		#首次发包
			if Pack_items['UE_ID'] not in UE_ID_List:	# 全新的节点
				log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Pack_Len_{5}_Pack_Time{6}_{7}" \
				.format('./log_files/', Pack_items['App_Type'] , Pack_items['UE_Type'] \
				, Pack_items['Operator'] , Pack_items['UE_ID'], str(len(msg)),Pack_Time ,'.csv')
				UE_ID_List.append(Pack_items['UE_ID'])	#UE_ID加入列表中
				Log_File_List.append(log_file_path)
			else:
				i = 0
				for item in Log_File_List:
					if item.find(Pack_items['UE_ID'])!=-1:
						log_file_path  = "{0}App_Type_{1}_UE_Type_{2}_Operator_{3}_UE_ID_{4}_Pack_Len_{5}_Pack_Time{6}_{7}" \
										.format('./log_files/', Pack_items['App_Type'] , Pack_items['UE_Type'] \
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
					Pack_items['Earfcn'],\
					Pack_items['Pci'],\
					Pack_items['Cell_Id'],\
					Pack_items['ECl'],\
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
