from modelNet.efficientdet import predict
from modelNet.efficientdet.efficientdet import Efficientdet
from PIL import Image
import xml.etree.ElementTree as ET
import cv2 as cv
import os


def xml_coord(path_xml, path_img, x1, y1, x2, y2, newdir_img, newdir_xml):
    etree = ET.parse(path_xml)
    etree.find('size').find('width').text = str(x2-x1)
    etree.find('size').find('height').text = str(y2-y1)
    for obj in etree.iter('object'):
        obj.find('bndbox').find('xmin').text = str(
            int(obj.find('bndbox')[0].text)-x1)
        obj.find('bndbox').find('ymin').text = str(
            int(obj.find('bndbox')[1].text)-y1)
        obj.find('bndbox').find('xmax').text = str(
            int(obj.find('bndbox')[2].text)-x1)
        obj.find('bndbox').find('ymax').text = str(
            int(obj.find('bndbox')[3].text)-y1)
    etree.write(newdir_xml)

def get_black_pic():
    efficientdet = Efficientdet()
    i = 0
    for filepath,dirnames,filenames in os.walk(r'F:\Final\dataset\undealedData2\color'):
        for filename in filenames:
            depth_path = r'F:\Final\dataset\undealedData2\depth'+'/'+filename.split('.')[0]+'.npy'
            color_path = r'F:\Final\dataset\undealedData2\png4'+'/'+filename
            img = Image.open(color_path).convert("RGBA")
            w,h = img.size
            new_image = Image.new('RGBA', (w, h), (0, 0, 0, 0))
            ans_list = predict.main(efficientdet,color_path,depth_path)
            top, left, bottom, right = ans_list[0][0],ans_list[0][1],ans_list[0][2],ans_list[0][3]
            width = right-left
            height = bottom-top
            newleft = int(max(left-width*0.05,0))
            newright = int(min(right+0.05*width,w))
            newtop = int(max(top-0.3*height,0))
            region = img.crop([newleft,newtop,newright,bottom])
            new_image.paste(region, (newleft,newtop))
            new_image.save('../dataset/makeblackData/color/'+'black_'+filename)
    for filepath,dirnames,filenames in os.walk(r'F:\Final\dataset\makeblackData\xmls'):
        for filename in filenames:
            print(filename)
            os.rename(filepath+'/'+filename,filepath+'/'+'black_'+filename)


def get_crop_pic():
    efficientdet = Efficientdet()
    i = 0
    for filepath,dirnames,filenames in os.walk(r'F:\Final\dataset\undealedData2\color'):
        for filename in filenames:
            depth_path = r'F:\Final\dataset\undealedData2\depth'+'/'+filename.split('.')[0]+'.npy'
            xml_path = r'F:\Final\dataset\undealedData2\xmls'+'/'+filename.split('.')[0]+'.xml'
            color_path = r'F:\Final\dataset\undealedData2\png4'+'/'+filename
            new_color_path = '../dataset/makecropData/color/'+filename
            new_xml_path = r'F:\Final\dataset\makecropData\xmls'+'/'+'crop_'+filename.split('.')[0]+'.xml'
            img = Image.open(color_path).convert("RGBA")
            w,h = img.size
            ans_list = predict.main(efficientdet,color_path,depth_path)
            top, left, bottom, right = ans_list[0][0],ans_list[0][1],ans_list[0][2],ans_list[0][3]
            width = right-left
            height = bottom-top
            newleft = int(max(left-width*0.05,0))
            newright = int(min(right+0.05*width,w))
            newtop = int(max(top-0.3*height,0))
            region = img.crop([newleft,newtop,newright,bottom])
            region.save('../dataset/makecropData/color/'+'crop_'+filename)
            xml_coord(xml_path, new_color_path, newleft,newtop,newright,bottom, '../dataset/makecropData/color/'+filename, new_xml_path)
# get_crop_pic()
get_black_pic()