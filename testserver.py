import socket
import sys
import numpy as np

if len(sys.argv) !=2:
    print(f'Usage: {sys.argv[0]} <port number>')
    sys.exit(2)
    
serversocket = socket.socket(
socket.AF_INET, socket.SOCK_STREAM)

port = int(sys.argv[1])

serversocket.bind(('0.0.0.0', port))
print('Server started...')
serversocket.listen(5)
while True:
    # establish a connection
    sclient,addr = serversocket.accept()
    # msg='Thank you for connecting'+ "\r\n"
    # sclient.send(msg.encode('ascii'))
    print(f'Got a connection from {addr}')
    
    while True:
        data = input('input any : ')        
        if data=='quit': break

        sclient.send(data.encode('ascii'))


    sclient.close()
    print(f'Connection from {addr} is closed')
