import socket
import sys

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
serversocket.bind(('', port))
print('Server started...')

# queue up to 5 requests
serversocket.listen(5)
while True:
    # establish a connection
    sclient,addr = serversocket.accept()
    
    print(f'Got a connection from {addr}')
    msg='Thank you for connecting'+ "\r\n"
    sclient.send(msg.encode('ascii'))
    
    while True:
        msg = sclient.recv(1024)
        msg = msg.decode('ascii')
        
        if msg=='quit': break
        
        msg=f'{msg.upper()} received!'
        sclient.send(msg.encode('ascii'))
        
    sclient.close()
    print(f'Connection from {addr} is closed')
