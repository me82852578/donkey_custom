#!/usr/bin/env python
# coding: utf-8

import numpy as np
from os import listdir
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

def load_sign_model():
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))    
    tf.reset_default_graph()
    model = load_model('donkey_sign_epoch30_label8.h5')
    return model

def img_in_model(model):
    image_size_width = 50
    image_size_height = 50
    num_labels = 5
    num_channels = 3 
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

if __name__ == '__main__':    
    model = load_sign_model()
    img_path = input('img_path : ')
    img_in_model(model)
    #     print(pre_label)
    # fig=plt.figure()
    # for test_img in listdir(test_data):
        
    #     if flag == 12:
    #         break
    #     all_data = all_data + 1
    #     load_img = Image.open(f'{test_data}{test_img}')
    #     load_img_gray = load_img.convert("L")
    #     load_img01 = load_img.resize((image_size_height,image_size_width))
    #     load_img02 =  np.asarray(load_img01, dtype=np.float32)
    #     my_img = np.reshape(load_img02, [-1,image_size_height,image_size_width,num_channels]) / 255
        
    #     pre_label = model.predict(my_img)
    #     pre_label = np.argmax(pre_label,1)
    #     print(pre_label)
    
    #     y = fig.add_subplot(3,4,flag+1)
    #     if pre_label == 0:
    #         a_counter = a_counter + 1
    #         str_label='A'
    #         print(f'這是A')
    #     elif pre_label == 1:
    #         b_counter = b_counter + 1
    #         str_label='B'
    #         print(f'這是B')
    #     elif pre_label == 2:
    #         c_counter = c_counter + 1
    #         str_label='C'
    #         print(f'這是C')
    #     elif pre_label == 3:
    #         s_counter = s_counter + 1
    #         str_label='STOP'
    #         print(f'這是STOP')

            
    #     y.imshow(load_img)
    #     plt.title(str_label)
    #     y.axes.get_xaxis().set_visible(False)
    #     y.axes.get_yaxis().set_visible(False)  
    #     flag += 1
        
    # plt.show()
            
    # print('a: {}\nb: {}\nc: {}\ns: {}\nall: {}'.format(a_counter,b_counter,c_counter,s_counter,all_data))

    # xxx = (a_counter/all_data)*100
    # print('{:.2f}%'.format(xxx))


