import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pydot

def make_model_residual_4():
    # 3 convolutional layers 3 chanels 2 grey images and 1 line art image
    #normalitation_layer = tf.keras.layers.LayerNormalization(axis=1)
    grey_input_images =  keras.Input(shape=(256, 384, 3))
    conv_1 = tf.keras.layers.Conv2D(filters = 60,kernel_size = (3,3),activation='relu',padding='same')(grey_input_images)
    pool_1 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_1)
    conv_2 = tf.keras.layers.Conv2D(filters = 120,kernel_size = (3,3),activation='relu',padding='same')(pool_1)
    pool_2 = tf.keras.layers.MaxPooling2D(pool_size=(2, 2))(conv_2)
    conv_3 = tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),activation='relu',padding='same')(pool_2)


    #then 3 block layers
    internal_block_1 =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),padding='same')(conv_3)
    internal_block_1_activation =  tf.keras.layers.ReLU()(internal_block_1)
    internal_block_1_n =  tf.keras.layers.LayerNormalization()(internal_block_1_activation)

    internal_block_2 =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),padding='same')(internal_block_1_n)
    internal_block_2_activation =  tf.keras.layers.ReLU()(internal_block_2)
    internal_block_2_n =  tf.keras.layers.LayerNormalization()(internal_block_2_activation)

    residual_1      = tf.keras.layers.add([internal_block_1_n,internal_block_2_n])

    internal_block_3 =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),padding='same')(residual_1)
    internal_block_3_activation =  tf.keras.layers.ReLU()(internal_block_3)
    internal_block_3_n =  tf.keras.layers.LayerNormalization()(internal_block_3_activation)



    internal_block_4 =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),padding='same')(internal_block_3_n)
    internal_block_4_activation = tf.keras.layers.ReLU()(internal_block_4)
    internal_block_4_n =  tf.keras.layers.LayerNormalization()(internal_block_4_activation)

    residual_3      = tf.keras.layers.add([internal_block_3_n,internal_block_4_n])

    internal_block_5 =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),padding='same')(residual_3)
    internal_block_5_activation =  tf.keras.layers.ReLU()(internal_block_5)
    internal_block_5_n =  tf.keras.layers.LayerNormalization()(internal_block_5_activation)



    internal_block_final =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),padding='same')(internal_block_5_n)
    internal_block_final_activation = tf.keras.layers.ReLU()(internal_block_final)
    internal_block_final_n =  tf.keras.layers.LayerNormalization()(internal_block_final_activation)

    residual_5      = tf.keras.layers.add([internal_block_5_n,internal_block_final_n])


    #then 3 de-convolutioanl layers

    decond_3 =  tf.keras.layers.Conv2D(filters = 240,kernel_size = (3,3),activation='relu',padding='same')(residual_5)
    skip_1    = tf.keras.layers.add([decond_3,conv_3])
    up_pool_2 = tf.keras.layers.UpSampling2D((2, 2))(decond_3)
    decond_2 =  tf.keras.layers.Conv2D(filters = 120,kernel_size = (3,3),activation='relu',padding='same')(up_pool_2)
    up_pool_1 = tf.keras.layers.UpSampling2D((2, 2))(decond_2)
    decond_1 =  tf.keras.layers.Conv2D(filters = 60,kernel_size = (3,3),activation='relu',padding='same')(up_pool_1)


    output_img = tf.keras.layers.Conv2D(filters = 1, kernel_size=(3,3),activation = 'relu',padding = 'same')(decond_1)

    model = keras.Model(inputs = grey_input_images,outputs=output_img,name="fase_1")

    return model


if __name__ == "__main__":
    #tf.config.set_visible_devices([], 'GPU')
    model = make_model_residual_4()#make_model_residual_3()
    model.summary()
    keras.utils.plot_model(model ,show_shapes=True)
