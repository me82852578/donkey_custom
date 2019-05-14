import socket
import sys
import final_donkey_sign_model as fm
import numpy as np

import command_donkey as cdky

if len(sys.argv) !=2:
    print(f'Usage: {sys.argv[0]} <port number>')
    sys.exit(2)
    
# create a socket object
serversocket = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
# host = socket.gethostname()
port = int(sys.argv[1])

# bind to the port
# serversocket.bind((host, port))
serversocket.bind(('0.0.0.0', port))
print('Server started...')
print('Loading model...')
model = fm.load_sign_model()
print('model is loaded !!')

# queue up to 5 requests
serversocket.listen(5)
while True:
    # establish a connection
    sclient,addr = serversocket.accept()
    # msg='Thank you for connecting'+ "\r\n"
    # sclient.send(msg.encode('ascii'))
    print('Got a connection from {}'.format(addr))
    
    while True:
        msg = sclient.recv(1024)
        msg = msg.decode('ascii')
        pre_label = fm.img_in_model(model)
        if pre_label == 0:
            str_label='A'
            print('這是A')
        elif pre_label == 1:
            str_label='B'
            print('這是B')
            cdky.command_to_car("/home/pi/cust_func/donkey_PWM.py {}".format('run'))
        elif pre_label == 2:
            str_label='C'
            print('這是C')
        elif pre_label == 3:
            str_label='STOP'
            print('這是STOP')
            cdky.command_to_car("/home/pi/cust_func/donkey_PWM.py {}".format('STOP'))
        sclient.send(str_label.encode('ascii'))


    sclient.close()
    print('Connection from {} is closed'.format(addr))
