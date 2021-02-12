import cv2
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pydot
import sys
from model import *


def normalize_img(image):
  return tf.cast(image , tf.float32)/255.0

#extract_in_between_folders(path1,path2)
if __name__ == "__main__":
    inbetween_net = make_model_residual_4()
    weights_path  =r""
    inbetween_net.load_weights(weights_path)

    path_line_art = r""
    path_color    = r""
    path_input    = r""
    #transform_2_key_frames_1_line_art_to_image_folder_3(path_color,path_line_art,path_input)



    red_url = r""
    green_url=r""
    blue_url = r""

    img_height, img_width = 256,384


    red_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = red_url,
    label_mode = None,
    color_mode='rgb',
    shuffle= False,
    image_size=(img_height, img_width),
    batch_size=1,
    #seed=42
    )

    green_ds=tf.keras.preprocessing.image_dataset_from_directory(
    directory = green_url,
    label_mode = None,
    color_mode='rgb',
    shuffle= False,
    image_size=(img_height, img_width),
    batch_size=1,
    #seed=42
    )

    blue_ds =tf.keras.preprocessing.image_dataset_from_directory(
    directory = blue_url,
    label_mode = None,
    color_mode='rgb',
    shuffle= False,
    image_size=(img_height, img_width),
    batch_size=1,
    #seed=42
    )
    red_ds  = red_ds.map(normalize_img)
    green_ds = green_ds.map(normalize_img)
    blue_ds = blue_ds.map(normalize_img)

    # just choose anyfolder where you want to create the images 
    url_write_image = r""



    if not os.path.exists(url_write_image):
        os.makedirs(url_write_image+"red\\")
        os.makedirs(url_write_image+"green\\")
        os.makedirs(url_write_image+"blue\\")
        os.makedirs(url_write_image+"RGB\\")


    list_names = []
    for filename in os.listdir(red_url+"\\r"):
        list_names.append(filename)
    print(list_names)
    count = 0
    for x in red_ds:
        frames = inbetween_net.predict(x)
        #print("x: ",x.shape,"frame: ", frames.shape)
        arr=np.asarray(frames[0])
        arr *= 255
        cv2.imwrite(url_write_image+ "red\\" + list_names[count],arr)
        print("working in: "+ str(count),end ="\r")
        count += 1
    count = 0
    for x in green_ds:
        frames = inbetween_net.predict(x)
        #print("x: ",x.shape,"frame: ", frames.shape)
        arr=np.asarray(frames[0])
        arr *= 255
        cv2.imwrite(url_write_image+ "green\\" + list_names[count],arr)
        print("working in: "+ str(count),end ="\r")
        count +=1
    count = 0
    for x in blue_ds:
        frames = inbetween_net.predict(x)
        #print("x: ",x.shape,"frame: ", frames.shape)
        arr=np.asarray(frames[0])
        arr *= 255
        cv2.imwrite(url_write_image+ "blue\\" + list_names[count],arr)
        print("working in: "+ str(count),end ="\r")
        count +=1

    for filename in os.listdir(url_write_image + "red"):

        red = cv2.imread(url_write_image+"red\\"+filename,0)
        green = cv2.imread(url_write_image+"green\\"+filename,0)
        blue = cv2.imread(url_write_image+"blue\\"+filename,0)

        color = cv2.merge([red,green,blue])
        cv2.imwrite(url_write_image+"RGB\\"+filename,color)
