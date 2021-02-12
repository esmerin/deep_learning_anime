from model import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pydot
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

def normalize_img(image):
  return tf.cast(image , tf.float32)/255.0


if __name__ == "__main__":

    seraph_net = make_model_residual_4()

    weights_path =r''
    seraph_net.load_weights(weights_path)


    # loading data set
    input_url = r'C:\Users\esmerinfr\Documents\anime_all\in_between_beta\data\validation_images\input'  #r'C:\Users\esmerinfr\Documents\anime_all\in_between_beta\data\images\input_data' #r'C:\Users\esmerinfr\Documents\anime_all\in_between_beta\data\data_set_high_mae\input'  r"C:\Users\esmerinfr\Documents\anime_all\seraph_alpha_net\test_data\input_images"

    img_height, img_width = 256,384

    input_key_and_line_art_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = input_url,
    label_mode = None,
    color_mode='rgb',
    shuffle= False,
    image_size=(img_height, img_width),
    batch_size=1,
    #seed=42
    )
    # normilize
    input_key_and_line_art_ds = input_key_and_line_art_ds.map(normalize_img)
    count = 1
    epoch = 1

    url_write_image = r""
    if not os.path.exists(url_write_image):
        os.makedirs(url_write_image)
    print("printing images:")
    for x in input_key_and_line_art_ds:
        frames = seraph_net.predict(x)
        arr=np.asarray(frames[0])
        arr *= 255
        cv2.imwrite(url_write_image + str(count) +".png",arr)
        print("working in: "+ str(count),end ="\r")
        count +=1
