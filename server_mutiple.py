import sys
import socket
from threading import Thread
import traceback
import numpy as np
from os import listdir
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
import final_donkey_sign_model as fm

def do_some_stuffs_with_input(input_string):  
    """
    This is where all the processing happens.

    Let's just read the string backwards
    """

    print("Processing that nasty input!")
    return input_string[::-1]

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):


   client_input = conn.recv(MAX_BUFFER_SIZE)
   client_input_size = sys.getsizeof(client_input)
   if client_input_size > MAX_BUFFER_SIZE:
      print("The input size is greater than expected {}".format(client_input_size))
   decoded_input = client_input.decode("utf8").rstrip()
   client_input = do_some_stuffs_with_input(decoded_input)
   # if "--QUIT--" in client_input:
   #    print("Client is requesting to quit")
   #    conn.close()
   #    print("Connection " + ip + ":" + port + " closed")
   #    is_active = False
   
   print("Processed result: {}".format(client_input))
   conn.sendall(client_input.encode("utf8"))



   # input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

   # siz = sys.getsizeof(input_from_client_bytes)
   # if  siz >= MAX_BUFFER_SIZE:
   #    print("The length of input is probably too long: {}".format(siz))

   # input_from_client = input_from_client_bytes.decode("utf8").rstrip()

   # res = do_some_stuffs_with_input(input_from_client)
   # print("Result of processing {} is: {}".format(input_from_client, res))

   # vysl = res.encode("utf8")  # encode the result string
   # conn.send(vysl)  # send it to client
   # # conn.close()  # close connection
   # print('Connection ' + ip + ':' + port + " ended")

def start_server():

   soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # this is for easy starting/killing the app
   soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   print('Socket created')

   try:
      soc.bind(("0.0.0.0", 8001))
      print('Socket bind complete')
   except socket.error as msg:
      import sys
      print('Bind failed. Error : ' + str(sys.exc_info()))
      sys.exit()

   soc.listen(10)

   print('Socket now listening')
   
   while True:
      conn, addr = soc.accept()
      ip, port = str(addr[0]), str(addr[1])
      print('Accepting connection from ' + ip + ':' + port)
      for i in range(len(conn)):
         print(i)
      try:
         Thread(target=client_thread, args=(conn, ip, port)).start()
      except:
         print("Terible error!")
         traceback.print_exc()
   soc.close()

start_server()  