import socket
import os
import sys

if len(sys.argv) != 2:
    print('STOP Point: {} <stop point>'.format(sys.argv[0]))
    sys.exit(1)

obj = socket.socket()
obj.connect(('192.168.32.171', 8001))


stop_point = 'go_{}'.format(sys.argv[1])
obj.send(stop_point.encode('ascii'))
obj.close()
