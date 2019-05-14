import sys
import socket
from threading import Thread
import traceback
import numpy as np
from os import listdir
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from load_sign_model import KerasLinear

if len(sys.argv) !=2:
    print(f'Usage: {sys.argv[0]} <port number>')
    sys.exit(2)
port = int(sys.argv[1])

def load_sign_model():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))    
    tf.reset_default_graph()
    model = load_model('donkey_sign.h5')
    return model

def img_in_model(model):
    image_size_width = 50
    image_size_height = 50
    num_labels = 4
    num_channels = 3 # RGB
    epochs = 20

    a_counter = 0
    b_counter = 0
    c_counter = 0
    s_counter = 0
    flag = 0

    test_data = 'mask_img'
    for test_img in listdir(test_data):
        print('{}/{}'.format(test_data, test_img))
        load_img = Image.open('{}/{}'.format(test_data, test_img))
        # load_img_gray = load_img.convert("L")
        load_img01 = load_img.resize((image_size_height,image_size_width))
        load_img02 =  np.asarray(load_img01, dtype=np.float32)
        my_img = np.reshape(load_img02, [-1,image_size_height,image_size_width,num_channels]) / 255
        pre_label = model.predict(my_img)
        pre_label = np.argmax(pre_label,1)
        print(pre_label)
        return pre_label

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 1024):

    print('Loading model...')
    my_model = load_sign_model()
    print('model is loaded !!')

    input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
    siz = sys.getsizeof(input_from_client_bytes)
    if  siz >= MAX_BUFFER_SIZE:
        print("The length of input is probably too long: {}".format(siz))
    ##
    input_from_client = input_from_client_bytes.decode("utf8").rstrip()
    if input_from_client == 'quit':
        res = 'quit'
    else:    
        print('gogogogogogoggogogogogogogogog')
        pre_label = img_in_model(my_model)
        if pre_label == 0:
            str_label='A'
            print('這是A')
        elif pre_label == 1:
            str_label='B'
            print('這是B')
        elif pre_label == 2:
            str_label='C'
            print('這是C')
        elif pre_label == 3:
            str_label='STOP'
            print('這是STOP')
        res = str_label
    ##

    print("Result of processing {} is: {}".format(input_from_client, res))
    vysl = res.encode("utf8")  # encode the result string
    conn.sendall(vysl)  # send it to client
    conn.close()  # close connection
    print('Connection ' + ip + ':' + port + " ended")

def start_server(port):


    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    try:
        soc.bind(('', port))
        print('Socket bind complete')
    except socket.error as msg:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    soc.listen(10)
    print('Server now listening')

    # for handling task in separate jobs we need threading
    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            traceback.print_exc()
    soc.close()

start_server(port)  