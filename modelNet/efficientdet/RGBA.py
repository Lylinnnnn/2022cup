from PIL import Image
import numpy as np
import os


def deal3channel24channel(imgpath=r"F:\deeplabv3-plus-pytorch-main\img\20000.png",deppath=r"F:\deeplabv3-plus-pytorch-main\img\20000.npy",savepath=r"F:\deeplabv3-plus-pytorch-main\img\test.png"):
    img = Image.open(imgpath).convert('RGBA')
    imgmat = np.array(img)
    dep = np.load(deppath)
    dep = np.uint8((dep-np.min(dep))/(np.max(dep)-np.min(dep))*255)
    imgmat[:,:,3] = dep
    img = Image.fromarray(imgmat)

    img.save(savepath)

# deal3channel24channel()


def get_files():
    i = 0
    for filepath,dirnames,filenames in os.walk(r'F:\Final\dataset\classfierdeskData\color'):
        for filename in filenames:
            index = filename.split('.')[0]
            print(filepath+'\\'+filename)
            print(r"F:\Final\dataset\classfierdeskData\depth"+'\\'+index+'.npy')
            print(r"F:\efficientdet-pytorch-master\VOCdevkit\VOC2007\JPEGImages"+'\\'+index+'.png')
            deal3channel24channel(imgpath=filepath+'\\'+filename,deppath=r"F:\Final\dataset\classfierdeskData\depth"+'\\'+index+'.npy',savepath=r"F:\efficientdet-pytorch-master\VOCdevkit\VOC2007\JPEGImages"+'\\'+index+'.png')
get_files()