# __author__ = 'Deliang Yang'
# __create__ = '2018.01.11'

import socket

UDP_IP = '96.126.124.91' # '123.207.22.183'# '25.56.5.62'  # '123.207.22.183'

UDP_PORT = 9235 #3030 # 9234
MSG = b'Hello, world!'

def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind(('', UDP_PORT))

    # while True:
    #     data, addr = sock.recvfrom(1024)
    #     print('Rcv msg:', data, 'from', addr)
    sock.sendto(MSG, (UDP_IP, UDP_PORT))

if __name__ == '__main__':
    run()
