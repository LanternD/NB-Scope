# __author__ = 'Deliang Yang'
# __create__ = '2018.01.11'

import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 9234

def run():
    SUM = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))
    counter = 0
    random = ''

    while True:
        SUM +=1
        data, addr = sock.recvfrom(1024)
        msg = str(data,encoding = 'utf-8')
        sum = int(msg[0:3])
        number = int(msg[4:7])

        if msg[8:11] != random:
            counter = 1
        else:
            counter +=1
        if len(data)<16:
            print('=============')
            print('Rcv msg:', msg, '\n--from', addr, 'Len:',len(data))
        else:
            print('Rcv msg:', msg[0:17] ,'\n--from', addr, 'Len:', len(data))
        print('Total:',sum,'\tIndex:',number,'\tPercent:', (counter/sum*100),'%')
        print('--No.%d'%SUM)
        print('===========================================')
        random = msg[8:11]
#    sock.sendto(MSG, (UDP_IP, UDP_PORT))

if __name__ == '__main__':
    run()
