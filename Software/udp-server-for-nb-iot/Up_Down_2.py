# __author__ = 'Deliang Yang & Xianghui'
# __create__ = '2019.04.11'
import re
import socket
import time
import json
import requests
#import certifi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###UP
UDP_IP = '0.0.0.0'
UDP_PORT = 9345
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

down_message = {
"deviceId": "***",
"command": {
"serviceId": "UP_DOWN",
"method": "DOWN",
"paras": {
"Down_data": '',
}
},
"callbackUrl": "http://129.211.125.101/na/iocm/devNotify/v1.1.0/reportCmdExecResult",
"maxRetransmit":"1",
"expireTime":"0"
}

Authorization_value = ''
appID = 'VQLomf4wsBJ439Vyq3XDygGureAa'
###
def Write_log_head(log_file_path, log_head):
	log_file = open(log_file_path, 'w')
	log_file.write(log_head)
	log_file.flush()
	log_file.close()
def Write_log(log_file_path, log):
	log_file = open(log_file_path, 'a')
	log_file.write(log)
	log_file.flush()
	log_file.close()
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

def parse_up(data,addr):
	UE_ID_List = []
	Operator = []
	Log_File_List = []
	Show_item = []
	UE_ID_List_fp = './list_file/UE_ID.txt'
	Log_File_List_fp = './list_file/log_file.txt'
	flag = 0
	UE_ID_List = Get_Lsit_info(UE_ID_List_fp, UE_ID_List)
	Log_File_List = Get_Lsit_info(Log_File_List_fp, Log_File_List)
	print(UE_ID_List)
	log_file_path = ''
	log_file_head = 'UE_ID\t\tIndex\t\tStandBy_Timer\t\tOperator\t\tPackLen\t\tPack_Time\t\t\n'
	msg_tmp = str(data, encoding = 'utf-8')
	pattern = re.compile(r'[0-9]{3}/[0-9]{3}/')
	match = pattern.findall(msg_tmp)
	if not match:
		print('Rcv msg:', data[0], '\nfrom', addr, 'Len:',len(data))
		print('=================================================')
	else:
		#msg_tmp = str(data,encoding = 'utf-8').split(',')[6]
		down_message['deviceId'] = re.findall(r'"deviceId":"(.+?)"',msg_tmp)[0]
		try:
			msg = re.findall(r'"data":{"UP":"(.+?)"}',msg_tmp)[0]
		except IndexError:
			msg = '1111111111111111111111111111111111111111111111111111111'
		Index = msg[0:3]
		StandBy_timer = msg[4:7]
		UE_ID = msg[8:11]
		Operator = msg[12:15]
		PackLen = str(len(msg))
		Pack_Time = time.strftime('_%Y%m%d_%H%M_%S',time.localtime(time.time()))
		Show_item.append(UE_ID)
		Show_item.append(Index)
		Show_item.append(StandBy_timer)
		Show_item.append(Operator)
		Show_item.append(PackLen)
		Show_item.append(Pack_Time)
		log = "{0}\t\t{1}\t\t{2}\t\t\t{3}\t\t\t{4}\t\t{5}\n".format(UE_ID, Index, StandBy_timer, Operator, PackLen, Pack_Time)
		if Index=='001':	#首次发送
			if UE_ID not in UE_ID_List:		#如果UE_n不在列表中
				print('test_ue id append\n');
				log_file_path  = './log_files/'+ UE_ID+ Pack_Time+'.txt'	#初创log文件名
				UE_ID_List.append(UE_ID)	#UE_ID加入列表中
				Log_File_List.append(log_file_path)
			else:
				i = 0
				for item in Log_File_List:
					if item.find(UE_ID)!=-1:
						log_file_path  ='./log_files/'+ UE_ID + Pack_Time + '.txt'
						Log_File_List[i] = log_file_path	#更新log文件名
						break
					i +=1
			flag = 1
			Write_log_head(log_file_path, log_file_head)
		else:
			for item in UE_ID_List:
				if item.find(UE_ID)!=-1:
					i = 0
					for item in Log_File_List:
						if item.find(UE_ID)!=-1:
							log_file_path = Log_File_List[i]
							break
						i +=1
					flag = 1
		if flag==1:
			flag = 0
			for item in Log_File_List:	#根据UE_ID匹配log_file(文件名)
				if item.find(UE_ID) != -1:
					log_file_path = item
					break
			#存储文件和显示信息
			Write_log(log_file_path, log)
			Show_Log(UE_ID_List, Show_item)
			Put_List_info(UE_ID_List_fp, UE_ID_List)
			Put_List_info(Log_File_List_fp, Log_File_List)
		else:
			print("***Received an invalid message***")
			print('{0}\t{1}\t{2}\t\t{3}\t\t{4}\t\t{5}'.format(Show_item[0], Show_item[1], Show_item[2], Show_item[3], Show_item[4], Show_item[5]))
			print('UE_ID\tIndex\tStandBy_Timer\tOperator\tPackLen\t\tPack_Time\t\tIt`s You?')
			print("***------***\n")
def get_accesstoken(url, Authertication_message):
	#response = requests.post(url, data= json.dumps(Authertication_message), verify=False, cert=('1.crt', '1.key'), headers=header).text
	response = requests.post(url, data=Authertication_message, verify=False, cert=('client.crt', 'client.key')).text
	#print(response)
	t_Authorization = response.split('"')[3]
	global Authorization_value
	Authorization_value = t_Authorization

def post_down_command(url):
	header['app_key'] = appID
	header['Authorization'] = "Bearer "+Authorization_value
	time_down_start = time.time()
	down_data_size = 500	#Byte
	down_data = ''
	for i in range(0, down_data_size):
		down_data +='A'
	down_message['command']['paras']['Down_data'] = down_data
	response = requests.post(url, data = json.dumps(down_message), verify=False, cert=('client.crt', 'client.key'), headers=header)
	if response.text.find('SENT')!=-1:
		print("Down Data Sent")

def send_down():
	get_accesstoken(url_access, Authertication_message)
	post_down_command(url_down)

def run():
	global SUM
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(('0.0.0.0', UDP_PORT))
	sock.listen(4)
	while True:
		SUM +=1
	# data, addr = sock.recvfrom(1024)
		c, addr = sock.accept()
		try:
			data = c.recv(1024)
			# print(data)
			c.send(response_text)
			parse_up(data,addr)
			send_down()
			# print('--No.%d--'%SUM)
			# print('=================================================')
		except socket.error as e:
			print(e)	
		finally:
			c.close()

if __name__ == '__main__':
	run()
