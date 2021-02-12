from model import *
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pydot
import cv2
import matplotlib.pyplot as plt


def normalize_img(image):
  return tf.cast(image , tf.float32)/255.0


if __name__ == "__main__":

    #make model
    seraph_net = make_model_residual_4()
    seraph_net.summary()
    weights_path = r"\saved-model-22.hdf5"
    seraph_net.load_weights(weights_path)
    #compaling the model
    optimizer=keras.optimizers.Adam(learning_rate=0.000001) # original = 0.00001
    loss_fn = tf.keras.losses.MeanAbsoluteError()  #tf.keras.losses.MeanSquaredError()

    seraph_net.compile(
    optimizer = optimizer,#"sgd",
    loss = loss_fn,
    )

    filepath = r""
    checkpoint = keras.callbacks.ModelCheckpoint(filepath, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto',save_freq='epoch')

    # loading data set

    input_url  = r''
    output_url = r''

    input_val_url = r''
    output_val_url= r''

    img_height, img_width = 256,384

    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
      try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=3200)])
      except RuntimeError as e:
        print(e)

    input_key_and_line_art_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = input_url,
    label_mode = None,
    color_mode='rgb',
    #shuffle=False,
    image_size=(img_height, img_width),
    batch_size=7,
    seed=42
    )

    grey_expected_image_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = output_url,
    label_mode = None,
    color_mode='grayscale',
    #shuffle=False,
    image_size=(img_height, img_width),
    batch_size=7,
    seed=42
    )
    #loading validation data set
    input_val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = input_val_url,
    label_mode = None,
    color_mode='rgb',
    shuffle=False,
    image_size=(img_height, img_width),
    batch_size=12
    )
    grey_val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = output_val_url,
    label_mode = None,
    color_mode='grayscale',
    shuffle=False,
    image_size=(img_height, img_width),
    batch_size=12
    #seed=42
    )

    # normilize
    input_key_and_line_art_ds = input_key_and_line_art_ds.map(normalize_img)
    grey_expected_image_ds = grey_expected_image_ds.map(normalize_img )

    input_val_ds = input_val_ds.map(normalize_img)
    grey_val_ds = grey_val_ds.map(normalize_img)

    # concateno los ds (input , target)
    ds = tf.data.Dataset.zip((input_key_and_line_art_ds,grey_expected_image_ds))
    ds_val = tf.data.Dataset.zip((input_val_ds,grey_val_ds))
    

    #fit model

    seraph_net.fit(x=ds,epochs = 30,verbose=1,validation_data = ds_val,callbacks=checkpoint,initial_epoch=22)
    #seraph_net.save(r"") #last save just for precaution ;)
