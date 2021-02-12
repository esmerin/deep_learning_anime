import math
import numpy as np
import cv2
import os
def calculate_psnr(img1, img2):
    # img1 and img2 have range [0, 255]
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))

def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()


def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')

def all_names_folder(url_folder):
    name = []
    for filename in os.listdir(url_folder):
        name.append(filename)
    return name
if __name__ == "__main__":

    url_raw_images =    r""
    url_output_images = r""

    images_name = all_names_folder(url_output_images)

    frame0 = 0
    frame1 = 0
    frame2 = 0
    frame3 = 0
    frame4 = 0
    frame5 = 0

    length      = int(len(images_name)/6)
    print(length)
    for shot in range(0,length):
        shot_name = images_name[shot*6:(shot*6 + 6)]
        frame0 += calculate_psnr(cv2.imread(url_raw_images+shot_name[0]),cv2.imread(url_output_images+shot_name[0]))
        frame1 += calculate_psnr(cv2.imread(url_raw_images+shot_name[1]),cv2.imread(url_output_images+shot_name[1]))
        frame2 += calculate_psnr(cv2.imread(url_raw_images+shot_name[2]),cv2.imread(url_output_images+shot_name[2]))
        frame3 += calculate_psnr(cv2.imread(url_raw_images+shot_name[3]),cv2.imread(url_output_images+shot_name[3]))
        frame4 += calculate_psnr(cv2.imread(url_raw_images+shot_name[4]),cv2.imread(url_output_images+shot_name[4]))
        frame5 += calculate_psnr(cv2.imread(url_raw_images+shot_name[5]),cv2.imread(url_output_images+shot_name[5]))

    print("frame0: ",frame0/length,"frame1: ",frame1/length,"frame2: ",frame2/length,"frame3: ",frame3/length,"frame4: ",frame4/length,"frame5: ",frame5/length)
    #average = calculate_ssim(img1, img2)
    #frame0:  0.8661183310227432 frame1:  0.8570826792566888 frame2:  0.8548272762062972 frame3:  0.8550862249438754 frame4:  0.8571832669982918 frame5:  0.8688004720521119
    #print(average)
