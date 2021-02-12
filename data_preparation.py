import os
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def create_list_directory(list_of_directory):
    for folder_list in list_of_directory:
        if not os.path.exists(folder_list):
            os.makedirs(folder_list)

def video_clips_folder_to_image_batch_raw(url_folder_video,url_raw,number):
   #number is the initial value for name the frames

  for filename in os.listdir(url_folder_video):
      clip_name=filename
      name = clip_name.split(".")
      anime_capture = cv2.VideoCapture(url_folder_video + clip_name)
      print("procesing this clip: " , url_folder_video + clip_name)
      success,image = anime_capture.read()
      if success == False:
          print("video fail to load: ", clip_name)
          return
      image = cv2.resize(image, dsize = (384,256))
      count = 0

      while success:
        batch = []
        batch_name = []
        for i in range(0,8):

          success,image = anime_capture.read()
          success,image = anime_capture.read()
          if success == False:
            break
          batch.append(image)
          batch_name.append(url_raw + name[0] + "_" "{}.png".format(str(number).zfill(5)))
          number = number + 1
          count += 1
        #save
        if success:
          for i in range(0,8):
            image_aux = batch[i]
            image_aux = cv2.resize(image_aux,dsize = (384,256))
            print('saved a new frame:',batch_name[i],count, end = '\r')
            cv2.imwrite(batch_name[i], image_aux)
  return number


def transfor_to_grey_folder_to_other(path,out):
	print("using this folder: "+ path)
	for filename in os.listdir(path):
		image = cv2.imread(path + filename)
		print(f"working in:" + filename, end = '\r')
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		cv2.imwrite(out + filename,gray_image)

def transform_2_key_frames_1_line_art_to_image_folder(path_keyframes,path_line_art,path_save):
    # this function prepare de data load for the neuronal net
    # the labels should be the grey ones with the same name
    all_filename_grey=[]
    all_filename_line_art=[]

    for filename in os.listdir(path_keyframes):
        all_filename_grey.append(filename)

    for filename in os.listdir(path_line_art):
        all_filename_line_art.append(filename)

    if (len(all_filename_grey) != len(all_filename_line_art)):
        print("not equal filesize")
        return

    for i in range(0,int(len(all_filename_grey)/8)):

        grey_image_batch = all_filename_grey[i*8:(i*8+8)]
        line_art_batch   = all_filename_line_art[i*8:(i*8+8)]
        key_frame_name_1 = grey_image_batch[0]
        key_frame_name_2 = grey_image_batch[7]
        for i in range(0,8):
            #open key frame 1
            #flag 0 make it greyscale
            key1 = cv2.imread(path_keyframes + key_frame_name_1,0)

            #key1 = cv2.resize(key1,(384,256))
            #open key frame 2
            key2 = cv2.imread(path_keyframes + key_frame_name_2,0)
            #key2 = cv2.resize(key2,(384,256))
            #open line_art i
            line_art_i = cv2.imread(path_line_art + line_art_batch[i],0)
            line_art_i = cv2.resize(line_art_i,(384,256))
            # fusion in 3 chanels
            #print(key1.shape,key2.shape,line_art_i.shape)
            not_even_my_final_form = cv2.merge([key1,key2,line_art_i])
            #not_even_my_final_form = np.concatenate((),axis = 0)
            #print(not_even_my_final_form.shape )
            #save the image of 3 chanels
            cv2.imwrite(path_save + line_art_batch[i],not_even_my_final_form)
            print("working in: ",line_art_batch[i], end = '\r')
        #break
def transform_2_key_frames_1_line_art_to_image_folder_2(path_keyframes,path_line_art,path_save):
    # this function prepare de data load for the neuronal net
    # the labels should be the grey ones with the same name
    all_filename_grey=[]
    all_filename_line_art=[]

    for filename in os.listdir(path_keyframes):
        all_filename_grey.append(filename)

    for filename in os.listdir(path_line_art):
        all_filename_line_art.append(filename)

    if (len(all_filename_grey) != len(all_filename_line_art)):
        print("not equal filesize")
        return

    for i in range(0,int(len(all_filename_grey)/8)):

        grey_image_batch = all_filename_grey[i*8:(i*8+8)]
        line_art_batch   = all_filename_line_art[i*8:(i*8+8)]
        key_frame_name_1 = grey_image_batch[0]
        key_frame_name_2 = grey_image_batch[7]
        for j in range(1,7):
            #print(line_art_batch)
            #print(line_art_batch[j])
            #return
            #open key frame 1
            #flag 0 make it greyscale
            key1 = cv2.imread(path_keyframes + key_frame_name_1,0)
            #key1 = cv2.resize(key1,(384,256))
            #open key frame 2
            key2 = cv2.imread(path_keyframes + key_frame_name_2,0)
            #key2 = cv2.resize(key2,(384,256))
            #open line_art i
            line_art_i = cv2.imread(path_line_art + line_art_batch[j],0)
            line_art_i = cv2.resize(line_art_i,(384,256))
            #line_art_i = cv2.cvtColor(line_art_i, cv2.COLOR_BGR2GRAY)
            # fusion in 3 chanels
            #print(key1.shape,key2.shape,line_art_i.shape)
            not_even_my_final_form = cv2.merge([key1,key2,line_art_i])
            #not_even_my_final_form = np.concatenate((),axis = 0)
            #print(not_even_my_final_form.shape )
            #save the image of 3 chanels
            cv2.imwrite(path_save + line_art_batch[j],not_even_my_final_form)
            print("working in: ",path_save + line_art_batch[j], end = '\r')

def copy_grey_no_key(path_copy,path_paste):
    #what this does is copy only frames 1 to 7 not key frames
    n = 0
    for filename in os.listdir(path_copy):
        if (n%8 == 0 or n%8 == 7):
            n+=1
            continue
        else:
            #print('copy '+ path_copy + filename+' '+path_paste+filename,end ='\r')
            os.system('copy '+ path_copy + filename+' '+path_paste+filename)
            n+=1

def input_data_to_rnn_data(input_path,save_path):
    for filename in os.listdir(input_path):
        img = cv2.imread(input_path + filename)
        red = img[:, :, 0]
        green = img[:, :, 1]
        blue = img[:, :, 2]
        save_img = cv2.hconcat([red,green,blue])
        cv2.imwrite(save_path + filename +".png",save_img)
        print(save_path + filename,end = '\r')
    return 0

def copy_high_mae_to_folder(input_path,input_rgb_path,output_rgb_path,no_gey_path,output_no_gey_path,minimun_loss):
    #what this does is copy only high mae batches to another folder
    mae = tf.keras.losses.MeanAbsoluteError()
    img_height, img_width = 256,384
    grey_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = input_path,
    label_mode = None,
    color_mode='grayscale',
    shuffle=False,
    image_size=(img_height, img_width),
    batch_size=8
    )
    batch_list = []
    list_error = []
    batch = 0
    for x in grey_ds:
        key1 = x[0]
        key2 = x[7]
        for i in range(1,7):
            #key error 1
            error1 = mae(key1,x[i]).numpy()
            #key error 2
            error2 = mae(key2,x[i]).numpy()
            error = (error1 + error2)/2
            list_error.append(error)
        mean = 0
        for error_in_batch in list_error:
            mean += error_in_batch
        mean /= len(list_error)
        #print(len(list_error),"  ",mean)
        if mean > minimun_loss:
            batch_list.append(batch)

        list_error = []
        batch+= 1
    #here i have a list with all the batches
    filenumber = 0
    batch_name = []
    batch_name_aux = []

    for filename in os.listdir(input_rgb_path):
        if not(filenumber % 6 == 0):
            batch_name_aux.append(filename)
        else:
            batch_name.append(batch_name_aux)
            batch_name_aux = []
            batch_name_aux.append(filename)
        filenumber += 1
    batch_name.append(batch_name_aux)
    #print(batch_name)
    #now i copy the other foldername
    filenumber = 0
    for batch_index in batch_list:
        for image_name in batch_name[batch_index]:
            print('working in:  '+ input_rgb_path + image_name +' '+ output_rgb_path + image_name, end = '\r')
            os.system('copy '+ input_rgb_path + image_name +' '+ output_rgb_path + image_name)

    batch_name = []
    filenumber = 0
    batch_name_aux = []
    for filename in os.listdir(no_gey_path):
        if not(filenumber % 6 == 0):
            batch_name_aux.append(filename)
        else:
            batch_name.append(batch_name_aux)
            batch_name_aux = []
            batch_name_aux.append(filename)
        filenumber += 1
    batch_name.append(batch_name_aux)
    for batch_index in batch_list:
        for image_name in batch_name[batch_index]:
            print('working in:  '+ no_gey_path + image_name +' '+ output_no_gey_path + image_name, end = '\r')
            os.system('copy '+ no_gey_path + image_name +' '+ output_no_gey_path + image_name)
def copy_high_mae_to_folder_rgb(input_folder,output_folder,minimun_loss):

    mae = tf.keras.losses.MeanAbsoluteError()
    img_height, img_width = 256,384
    color_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = input_folder,
    label_mode = None,
    color_mode='rgb',
    shuffle=False,
    image_size=(img_height, img_width),
    batch_size=8
    )
    batch_list = []
    list_error = []
    batch = 0
    for x in color_ds:
        key1 = x[0]
        key2 = x[7]
        for i in range(1,7):
            #key error 1
            error1 = mae(key1,x[i]).numpy()
            #key error 2
            error2 = mae(key2,x[i]).numpy()
            error = (error1 + error2)/2
            list_error.append(error)
        mean = 0
        for error_in_batch in list_error:
            mean += error_in_batch
        mean /= len(list_error)
        #print(len(list_error),"  ",mean)
        if mean > minimun_loss:
            batch_list.append(batch)

        list_error = []
        batch += 1
        print("prosesing batch: ",batch,end = "\r")
    print(batch)
    #here i have a list with all the batches
    filenumber = 0
    batch_name = []
    batch_name_aux = []
    foldername_aux = ""
    for foldername in os.listdir(input_folder):
        foldername_aux = foldername
        for filename in os.listdir(input_folder + foldername):
            if not(filenumber % 8 == 0):
                batch_name_aux.append(filename)
            else:
                batch_name.append(batch_name_aux)
                batch_name_aux = []
                batch_name_aux.append(filename)
            filenumber += 1
        batch_name.append(batch_name_aux)
    #print(batch_name)
    #now i copy the other foldername
    batch_name.pop(0)
    filenumber = 0
    print(len(batch_name))
    for batch_index in batch_list:
        for image_name in batch_name[batch_index]:
            print('copy '+ input_folder +foldername_aux +"\\"+image_name+' '+ output_folder + image_name, end = '\r')
            os.system('copy "'+ input_folder +foldername_aux +"\\"+image_name+'"  "'+ output_folder + image_name+'"')

def copy_high_mae_to_folder_greyscale(input_folder,output_folder,minimun_loss):

    mae = tf.keras.losses.MeanAbsoluteError()
    img_height, img_width = 256,384
    color_ds = tf.keras.preprocessing.image_dataset_from_directory(
    directory = input_folder,
    label_mode = None,
    color_mode='grayscale',
    shuffle=False,
    image_size=(img_height, img_width),
    batch_size=8
    )
    batch_list = []
    list_error = []
    batch = 0
    for x in color_ds:
        key1 = x[0]
        key2 = x[7]
        for i in range(1,7):
            #key error 1
            error1 = mae(key1,x[i]).numpy()
            #key error 2
            error2 = mae(key2,x[i]).numpy()
            error = (error1 + error2)/2
            list_error.append(error)
        mean = 0
        for error_in_batch in list_error:
            mean += error_in_batch
        mean /= len(list_error)
        #print(len(list_error),"  ",mean)
        if mean > minimun_loss:
            batch_list.append(batch)

        list_error = []
        batch+= 1
    #here i have a list with all the batches
    filenumber = 0
    batch_name = []
    batch_name_aux = []
    foldername_aux = ""
    for foldername in os.listdir(input_folder):
        foldername_aux = foldername
        for filename in os.listdir(input_folder + foldername):
            if not(filenumber % 8 == 0):
                batch_name_aux.append(filename)
            else:
                batch_name.append(batch_name_aux)
                batch_name_aux = []
                batch_name_aux.append(filename)
            filenumber += 1
        batch_name.append(batch_name_aux)
    #print(batch_name)
    #now i copy the other foldername
    filenumber = 0
    for batch_index in batch_list:
        for image_name in batch_name[batch_index]:
            print('working in:  '+ image_name, end = '\r')
            os.system('copy '+ input_folder +foldername_aux +"\\"+image_name+' '+ output_folder + image_name)
def rename(path,save):
    print(path)
    #os.system("cd "+path+" & dir")
    for filename in os.listdir(path):
        print('copy "' +path + filename+'"  "'+ save + filename+'"')
        os.system('copy "' +path + filename+'"  "'+ save + filename+'"')
    return 0

def color_to_grey_no_key_and_input(path_keyframes,path_line_art,path_save):

    all_filename_grey=[]
    all_filename_line_art=[]

    for filename in os.listdir(path_keyframes):
        all_filename_grey.append(filename)

    for filename in os.listdir(path_line_art):
        all_filename_line_art.append(filename)

    if (len(all_filename_grey) != (len(all_filename_line_art)*8)/6):
        print("not equal filesize")
        print(len(all_filename_grey),(len(all_filename_line_art)*6)/8)
        return

    for i in range(0,int(len(all_filename_grey)/8)):

        grey_image_batch = all_filename_grey[i*8:(i*8+8)]
        line_art_batch   = all_filename_line_art[i*6:(i*6+6)]
        key_frame_name_1 = grey_image_batch[0]
        key_frame_name_2 = grey_image_batch[7]
        #the 0 make it grey
        key1 = cv2.imread(path_keyframes + key_frame_name_1,0)
        key2 = cv2.imread(path_keyframes + key_frame_name_2,0)


        for j in range(0,6):

            line_art_i = cv2.imread(path_line_art + line_art_batch[j],0)
            line_art_i = cv2.resize(line_art_i,(384,256))
            not_even_my_final_form = cv2.merge([key1,key2,line_art_i])
            #save the image of 3 chanels
            cv2.imwrite(path_save + line_art_batch[j],not_even_my_final_form)
            print("working in: ",path_save + line_art_batch[j], end = '\r')


def copy_color_to_no_key(path_color,path_save):
    #what this does is copy only frames 1 to 7 not key frames
    n = 0
    for filename in os.listdir(path_color):
        if (n%8 == 0 or n%8 == 7):
            n+=1
            continue
        else:
            key1 = cv2.imread(path_color + filename,0)
            cv2.imwrite(path_save + filename,key1)
            print(filename,end = '\r')
            n+=1
#transfor_to_grey_folder_to_other("C:\\Users\\esmerinfr\\Documents\\anime_all\\seraph_alpha_net\\owari_data\\color\\","C:\\Users\\esmerinfr\\Documents\\anime_all\\seraph_alpha_net\\owari_data\\greyscale\\")

def clips_to_all_images(url_folder_video,url_out_images):
    count = 0
    for filename in os.listdir(url_folder_video):
        clip_name = filename
        anime_capture = cv2.VideoCapture(url_folder_video + clip_name)
        print("procesing this clip: " , url_folder_video + clip_name)
        name = clip_name.split(".")
        success,image = anime_capture.read()
        if success == False:
            print("video fail to load: ", clip_name)
            return
        while success:
            image = cv2.resize(image, dsize = (384,256))
            cv2.imwrite(url_out_images+name[0]+"_{}.png".format(str(count).zfill(5)),image)
            success,image = anime_capture.read()
            count += 1

def extract_key_frames(url_key_frames,url_save):
    filename_list = []
    for filename in os.listdir(url_key_frames):
        filename_list.append(filename)
    count = 0
    for i in range(0,int(len(filename_list)/8)):
        color_image_batch = filename_list[i*8:(i*8+8)]
        key_frame_name_1 = color_image_batch[0]
        key_frame_name_2 = color_image_batch[7]

        os.system('copy "' +url_key_frames + key_frame_name_1+'"  "'+ url_save + key_frame_name_1+'"')
        os.system('copy "' +url_key_frames + key_frame_name_2+'"  "'+ url_save + key_frame_name_2+'"')

def extract__no_key_frames(url_key_frames,url_save):
    filename_list = []
    for filename in os.listdir(url_key_frames):
        filename_list.append(filename)
    count = 0
    for i in range(0,int(len(filename_list)/8)):
        color_image_batch = filename_list[i*8:(i*8+8)]
        for i2 in range(1,7):
            os.system('copy "' +url_key_frames + color_image_batch[i2]+'"  "'+ url_save +color_image_batch[i2]+'"')
            os.system('copy "' +url_key_frames + color_image_batch[i2]+'"  "'+ url_save +color_image_batch[i2]+'"')

    return

def grey_from_rgb(folder_url,out_url):
# create directories
    if not os.path.exists(out_url):
        os.makedirs(out_url)
    if not os.path.exists(out_url+"red\\r\\"):
        os.makedirs(out_url+"red\\r\\")
    if not os.path.exists(out_url+"green\\g\\"):
        os.makedirs(out_url+"green\\g\\")
    if not os.path.exists(out_url+"blue\\b\\"):
        os.makedirs(out_url+"blue\\b\\")
#seprarate images then write them
    for filename in os.listdir(folder_url):
        img = cv2.imread(folder_url + filename)
        red = img[:, :, 0]
        green = img[:, :, 1]
        blue = img[:, :, 2]
        cv2.imwrite(out_url+"red\\r\\"+filename,red)
        cv2.imwrite(out_url+"green\\g\\"+filename,green)
        cv2.imwrite(out_url+"blue\\b\\"+filename,blue)
        print("working in:",filename,end="\r")
    return 1
if __name__ == "__main__":
    #functions in this file
    """
    def video_clips_folder_to_image_batch_raw(url_folder_video,url_raw,number): return the end number
    def transfor_to_grey_folder_to_other(path,out):
    def transform_2_key_frames_1_line_art_to_image_folder(path_keyframes,path_line_art,path_save):
    def create_list_directory(list_of_directory)
    def transform_2_key_frames_1_line_art_to_image_folder_2(path_keyframes,path_line_art,path_save):
        copy_grey_no_key(path_copy,path_paste):
    def input_data_to_rnn_data(input_path,save_path):
    def copy_high_mae_to_folder(input_path,input_rgb_path,output_rgb_path,no_gey_path,output_no_gey_path,minimun_loss):
    def copy_high_mae_to_folder_rgb(input_folder,output_folder,minimun_loss):
    def copy_high_mae_to_folder_greyscale(input_folder,output_folder,minimun_loss):
        color_to_grey_no_key_and_input(path_keyframes,path_line_art,path_save)
        copy_color_to_no_key(path_color,path_save)
    def clips_to_all_images(url_folder_video,url_out_images)
    def extract_key_frames(url_key_frames,url_save):
    def extract__no_key_frames(url_key_frames,url_save):
    """


    path1=r'C:\Users\esmerinfr\Documents\anime_all\final_inbetween_proyect\paper\video_test\raw_images\\'
    path2=r'C:\Users\esmerinfr\Documents\anime_all\final_inbetween_proyect\paper\video_test\key_no_only\\'
    path3=r'C:\Users\esmerinfr\Documents\anime_all\final_inbetween_proyect\paper\video_test\lineart\\'
    path4=r'C:\Users\esmerinfr\Documents\anime_all\final_inbetween_proyect\paper\video_test\RGB\\'
    path5=r'C:\Users\esmerinfr\Documents\anime_all\final_inbetween_proyect\paper\video_test\output\\'
    path6=r'C:\Users\esmerinfr\Documents\anime_all\final_inbetween_proyect\paper\video_test\lineart\\'

    #color_to_grey_no_key_and_input(path2,path3,path1)
    #copy_color_to_no_key(path2,path4)
    #clips_to_all_images(path1,path2)
    extract__no_key_frames(path1,path2)



# scenedetect -i "sakuraso_b.mkv" detect-content split-video --output C:\Users\esmerinfr\Documents\anime_all\in_between_beta\data\video\video_clips\clip_data_set_2\sakuraso_b
#scenedetect -i "[Judas] Haikyuu!! S1 - 04.mkv" detect-content split-video --output C:\Users\esmerinfr\Documents\anime_all\in_between_beta\data\video\video_clips\clip_data_set_2\haikyu
