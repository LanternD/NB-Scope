# __author__ = 'Deliang Yang'
# __create__ = '2018.01.11'

import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 9234

def run():
    SUM = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))

    while True:
        SUM +=1
        data, addr = sock.recvfrom(1024)
        msg = str(data,encoding = 'utf-8')
        sum = 11 # int(msg[0:3])
        number = 12 #int(msg[4:7])
        if len(data)<512:
            print('=============')
            print('Rcv msg:', data, '\n--from', addr, 'Len:',len(data))
        else:
            print('Rcv msg:FFFFFFFF...', '\n--from', addr, 'Len:', len(data))
        print('Sum:',sum,'\tIndex:',number)
        print('--No.%d'%SUM)
        print('===================================')
        if msg[:7] == 'A01|000':
            sock.sendto('downflag001|005|01001|030|256'.encode('utf-8'), addr)
        else:
            sock.sendto(msg.encode('utf-8'), addr)

if __name__ == '__main__':
    run()
