from PIL import Image,ImageDraw
# from yolo import YOLO
from modelNet.classifier.predict import judge
from output import output_message
import os
import datetime
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def static_detect(yolo,classification,img):
    image,ans_lst = yolo.detect_image(img)
    # image.show()
    static_lst = []
    for thing in ans_lst:
        top, left, bottom, right = int(thing[1]),int(thing[2]),int(thing[3]),int(thing[4])
        pos = [left,top,right,bottom]
        region = img.crop(pos)
        class_name,pro = judge(classification,region)

        if class_name == thing[0].decode().split(' ')[0]:
            static_lst.append(thing)
        elif class_name != thing[0].decode().split(' ')[0] and pro>0.9:
            temp_str = class_name+' '+str(pro)
            static_lst.append([temp_str.encode(),top, left, bottom, right])
    ans = [x[0].decode().split(' ')[0].encode() for x in static_lst]
    dic = output_message.change_list2dict(ans)
    ans_str = output_message.dict2str(dic)
    return dic,ans_str
def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
def move_detect(yolo,img):

    image,ans_lst1 = yolo.detect_image(img)
    ans = [x[0].decode().split(' ')[0].encode() for x in ans_lst1]
    dic = output_message.change_list2dict(ans)
    ans_str = output_message.dict2str(dic)
    image.save(r"F:\Final\result"+"\\"+tid_maker()+".png")
    return dic,ans_str


# from PIL import Image,ImageDraw
# from yolo import YOLO
#
# yolo = YOLO()
# img = Image.open(r'G:\1.png').convert("RGBA")
#
# result,result_str = move_detect(yolo,img)
# print(result)
# print(result_str)