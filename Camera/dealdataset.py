import os
import shutil

def get_files():
    i = 0
    for filepath,dirnames,filenames in os.walk('../data/color'):
        for filename in filenames:
            print('../data/depth/'+filepath.split('\\')[1]+'/'+filename.split('.')[0]+'.npy')

            shutil.copyfile('../data/depth/'+filepath.split('\\')[1]+'/'+filename.split('.')[0]+'.npy','../dataset/undealedData2/depth/'+'4_'+str(i)+'.npy')
            i+=1

# get_files()

def split_pics():
    i = 1
    for filepath, dirnames, filenames in os.walk('../dataset/undealedData2/color'):
        for filename in filenames:
            print(filepath+'/'+filename)

split_pics()

from torchvision import models
fcn = models.segmentation.fcn_resnet101(pretrained=True).eval()