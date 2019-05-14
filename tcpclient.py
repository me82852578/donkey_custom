import socket
import sys
import time
# import c_my_traffic_detector_mask_capture_send as tdmc

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
    server_res = sserver.recv(1024)
    server_res = server_res.decode('ascii')
    print(server_res)

    # Get message from keyboard
    data = input('img path input !! : ')        
    sserver.send(data.encode('ascii'))
    if data=='quit': break


    if server_res == 'STOP':
        print('donkey stop 5s !')
        time.sleep(5)
        print('after 5s donkey go !')


sserver.close()
