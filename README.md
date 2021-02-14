# inbetween colorization

open source project for automatic inbetween colorization 
in the folder paper you can see the result of my investigation 

if you want to try it yourself, take in consideration that this net, works in black and white so, you have to generate each channel of RGB individualy.
as input it takes a especial format of image, where in the channel RED is a keyframe in black and white, the second key frame should be the second keyframe, and in the
green channel should be the line art or douga! 

![alt text](https://github.com/esmerin/inbetween_colorization/blob/main/paper/images/final%20images/figure2.png)

if you want to see what this can do look at https://drive.google.com/drive/folders/1PfLBpxPzkipXkPuRJZISHBfmKKFxQPc9?usp=sharing to look at it 

#generating data

first of all you need shots of animations, to do so, i use pyscenedetect, after the sequences in a folder use video_clips_folder_to_image_batch_raw() in data_preparation.py then you have images in shots of 8 in a folder, here you have 2 options manually delete bad inbetweens or use the filter copy_high_mae_to_folder_rgb() but this filter is not perfect so after the filter you should filter manualy anyway. 

now you have the shots, to generate the gengas i use sketchkeras, now with transfor_to_grey_folder_to_other() transform the folder into greyscale, with copy_grey_no_key() extract the ground truth we use this later. with the gengas generated and the shots in greyscale, use the function transform_2_key_frames_1_line_art_to_image_folder() this creates the data type this net use. and now you are ready to use the net! 
give you and example:

![alt text](https://github.com/esmerin/inbetween_colorization/blob/main/paper/images/final%20images/figure%201.png)

another example: 1)lineart 2)input from blue chanel greyscale 3)output bluechannel 4)after merge output greenchanel and output greenchanel 5) original frames we want to emulate 
![alt text](https://github.com/esmerin/inbetween_colorization/blob/main/paper/images/final%20images/figure%203.png)

to an easier tutorial i made a youtube tutorial: https://youtu.be/8-YIrqm3aCs

