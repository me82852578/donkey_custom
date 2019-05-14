import socket
import sys

if len(sys.argv) != 3:
    print('Usage: {} <server ip> <port number>'.format(sys.argv[0]))
    sys.exit(2)

# create a socket object
sserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set server ip/port
host = sys.argv[1]
port = int(sys.argv[2])

# connection to hostname on the port.
sserver.connect((host, port)) 
print(host,'socket connected!')

while True:
    # Receive no more than 1024 bytes
    msg = sserver.recv(1024)
    print (msg.decode('ascii'))
        
    # Get message from keyboard
    data = input('Enter message: ')        
    sserver.send(data.encode('ascii'))
        
    if data=='quit': break

sserver.close()
