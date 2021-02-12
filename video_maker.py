import os
import cv2
import numpy as np
def read_folder_img_array(url,size):
    array = []
    for filename in os.listdir(url):
        #print(url + filename)
        img = cv2.imread(url + filename)
        img = cv2.resize(img,size)
        array.append(img)
    return array
def from_grey_to_3_chanel_grey(arr):
    for i in range(len(arr)):
        arr[i] = cv2.merge([arr[i],arr[i],arr[i]])
    return arr

url_1=r""
url_2=r""
url_3=r""
url_4=r""

RGB_arr =[]
input_arr =[]
line_art_arr =[]
output_arr = []
size = (384,256)

RGB_arr     = read_folder_img_array(url_1,size)
#input_arr    = read_folder_img_array(url_2,size)
#line_art_arr = read_folder_img_array(url_3,size)
#output_arr   = read_folder_img_array(url_4,size)

#print(grey_arr.shape , input_arr.shape , line_art_arr.shape , output_arr.shape)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('test_final.mp4',fourcc, 6, (384,256))
for i in range(len(grey_arr)):
    aux_img = cv2.hconcat([RGB_arr[i])
    out.write(aux_img)
out.release()
