import socket

obj = socket.socket()
#obj.connect(('192.168.32.171', 8001))
obj.connect(('192.168.32.187', 8001))

while True:
    inp = input('>>>')
    obj.sendall(bytes(inp, encoding='utf-8'))
    ret = str(obj.recv(1024),encoding='utf-8')
    print(ret)

obj.close()
