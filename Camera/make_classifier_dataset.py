import xml.etree.ElementTree as ET
import os
from PIL import Image


def xml_coord():
    i=0

    for filepath,dirnames,filenames in os.walk(r'F:\yolox-pytorch-main\VOCdevkit\VOC2007\Annotations'):
        for filename in filenames:
            try:
                etree = ET.parse(filepath+'/'+filename)
                img = Image.open(r'F:\yolox-pytorch-main\VOCdevkit\VOC2007\JPEGImages'+'\\'+filename.split('.')[0]+'.png').convert("RGBA")
                print(filename)
                for obj in etree.iter('object'):
                    name = obj.find('name').text
                    print(name)
                    pos = []
                    pos.append(int(obj.find('bndbox').find('xmin').text))
                    pos.append(int(obj.find('bndbox').find('ymin').text))
                    pos.append(int(obj.find('bndbox').find('xmax').text))
                    pos.append(int(obj.find('bndbox').find('ymax').text))
                    print(pos)
                    if os.path.isdir(r'F:\Final\dataset\classifierData'+'\\'+name):
                        region = img.crop(pos)
                        region.save(r'F:\Final\dataset\classifierData'+'\\'+name +'\\'+ filename.split('.')[0]+'_'+str(i)+'.png')
                    else:
                        os.makedirs(r'F:\Final\dataset\classifierData'+'\\'+name)
                        region = img.crop(pos)
                        region.save(r'F:\Final\dataset\classifierData' + '\\' + name +'\\'+ filename.split('.')[0]+'_'+str(i) + '.png')
                    i+=1
            except:
                pass
            finally:
                pass

xml_coord()