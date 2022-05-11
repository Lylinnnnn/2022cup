
import time

import cv2
import numpy as np
from PIL import Image
def deal3channel24channel(imgpath=r"F:\deeplabv3-plus-pytorch-main\img\20000.png",deppath=r"F:\deeplabv3-plus-pytorch-main\img\20000.npy",savepath=r"F:\deeplabv3-plus-pytorch-main\img\test.png"):
    img = Image.open(imgpath).convert('RGBA')
    imgmat = np.array(img)
    dep = np.load(deppath)
    dep = np.uint8((dep-np.min(dep))/(np.max(dep)-np.min(dep))*255)
    imgmat[:,:,3] = dep
    img = Image.fromarray(imgmat)

    return img

def main(efficientdet,img):
    try:
        image = img
    except:
        print('Open Error! Try again!')
    else:
        r_image,ans_list = efficientdet.detect_image(image)
        return ans_list