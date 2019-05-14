#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from os import listdir
from random import shuffle
from PIL import Image
import matplotlib.pyplot as plt

from tensorflow.python.framework import graph_util
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.losses import sparse_categorical_crossentropy
from tensorflow.keras.optimizers import Adam


gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.9)
sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))    
tf.reset_default_graph()


# In[2]:


model = load_model('donkey_sign.h5')


# In[3]:


image_size_width = 50
image_size_height = 50
num_labels = 4
num_channels = 3 # RGB
batch_size = 40
epochs = 20


# In[4]:


test_data = 'test_data/'    
a_counter = 0
b_counter = 0
c_counter = 0
s_counter = 0
all_data = 0
flag = 0
fig=plt.figure()

for test_img in listdir(test_data):
    
    if flag == 12:
        break
    all_data = all_data + 1
    load_img = Image.open(f'{test_data}{test_img}')
    load_img_gray = load_img.convert("L")
    load_img01 = load_img.resize((image_size_height,image_size_width))
    load_img02 =  np.asarray(load_img01, dtype=np.float32)
    my_img = np.reshape(load_img02, [-1,image_size_height,image_size_width,num_channels]) / 255
      
    pre_label = model.predict(my_img)
    pre_label = np.argmax(pre_label,1)
    print(pre_label)
   
    y = fig.add_subplot(3,4,flag+1)
    if pre_label == 0:
        a_counter = a_counter + 1
        str_label='A'
        print(f'這是A')
    elif pre_label == 1:
        b_counter = b_counter + 1
        str_label='B'
        print(f'這是B')
    elif pre_label == 2:
        c_counter = c_counter + 1
        str_label='C'
        print(f'這是C')
    elif pre_label == 3:
        s_counter = s_counter + 1
        str_label='STOP'
        print(f'這是STOP')

        
    y.imshow(load_img)
    plt.title(str_label)
    y.axes.get_xaxis().set_visible(False)
    y.axes.get_yaxis().set_visible(False)  
    flag += 1
    
plt.show()
        
        
    
print('a: {}\nb: {}\nc: {}\ns: {}\nall: {}'.format(a_counter,b_counter,c_counter,s_counter,all_data))

xxx = (a_counter/all_data)*100
print('{:.2f}%'.format(xxx))


# In[ ]:




