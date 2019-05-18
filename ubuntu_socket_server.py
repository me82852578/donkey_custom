import select
import socket
import queue
import sys
import final_donkey_sign_model as fm
import numpy as np
import command_donkey as cdky
 
print('Loading model...')
model = fm.load_sign_model()
print('model is loaded !!')
#create a socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(False)
#set option reused
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
 
server_address= ('0.0.0.0',8001)
server.bind(server_address)
 
server.listen(10)
print('socket listen')
 
#sockets from which we except to read
inputs = [server]
 
#sockets from which we expect to write
outputs = []
 
#Outgoing message queues (socket:Queue)
message_queues = {}
 
#A optional parameter for select is TIMEOUT
timeout = 0 
 
while inputs:
    str_label = ''
    print("waiting for next event")
    readable , writable , exceptional = select.select(inputs, outputs, inputs)#, timeout)
    print('#################################')
 
    # When timeout reached , select return three empty lists
    if not (readable or writable or exceptional) :
        print("Time out ! ")
        break;    
    for s in readable :
        print('readable')
        if s is server:
            # A "readable" socket is ready to accept a connection
            connection, client_address = s.accept()
            print("    connection from ", client_address)
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
            print('===='*10)
            print(inputs)
            print('===='*10)
        else:
            try:
                data = s.recv(1024)
            except ConnectionResetError:
                print('some one exit')
                break
            data = data.decode('ascii')
            print(" received " , data , "from ",s.getpeername())

            if 'go_' in data:
                print(data)
            
            elif 'gogogo' in data:
                
                print("load model.....")
                pre_label = fm.img_in_model(model)
                if pre_label == 0:
                    str_label='A'
                    print('A')
                elif pre_label == 1:
                    str_label='B'
                    print('B')
                elif pre_label == 2:
                    str_label='C'
                    print('C')
                elif pre_label == 3:
                    str_label='STOP'
                    print('STOP')
                elif pre_label == 4:
                    str_label='red'
                    print('Red light')
                elif pre_label == 5:
                    str_label='green'
                    print('Green light')
                elif pre_label == 6:
                    str_label='left'
                    print('left')
                elif pre_label == 7:
                    str_label='right'
                    print('right')

            else:
                print(data)
                print('pass !')
                pass
            if data :
                print(" received " , data , "from ",s.getpeername())
                if str_label != '':
                    message_queues[s].put(str_label.encode('ascii'))
                else:
                    message_queues[s].put(data.encode('ascii'))
                # Add output channel for response    
                if s not in outputs:
                    outputs.append(s)
            else:
                #Interpret empty result as closed connection
                print("  closing", client_address)
                if s in outputs :
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                #remove message queue 
                #del message_queues[s]
    for s in writable:
        print('writable')
        try:
            next_msg = message_queues[s].get_nowait()
        except KeyError:
            print('KeyError !!')
        except queue.Empty:
            print(" " , s.getpeername() , 'queue empty')
            outputs.remove(s)
        else:
            print(next_msg)
            try:
                s.send(next_msg)
            except:
                pass
            inputs[1].send(next_msg)
     
    for s in exceptional:
        print('exceptional')
        print(" exception condition on ", s.getpeername())
        #stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        #Remove message queue
        del message_queues[s]
