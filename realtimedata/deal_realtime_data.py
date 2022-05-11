from PIL import Image,ImageChops
from modelNet.efficientdet import predict
from modelNet.efficientdet.efficientdet import Efficientdet

def deal(desk_detect,img):
    w,h = img.size
    new_image = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ans_list = predict.main(desk_detect,img)
    top, left, bottom, right = ans_list[0][0],ans_list[0][1],ans_list[0][2],ans_list[0][3]
    width = right-left
    height = bottom-top
    newleft = int(max(left-width*0.05,0))
    newright = int(min(right+0.05*width,w))
    newtop = int(max(top-0.3*height,0))
    region = img.crop([newleft,newtop,newright,bottom])
    new_image.paste(region, (newleft,newtop))
    flip = img.transpose(Image.FLIP_LEFT_RIGHT)
    # width, height = img.size
    # offimg = ImageChops.offset(img,5,5)
    # offimg.paste((0,0,0),(0,0,5,height))
    # offimg.paste((0,0,0),(0,0,width,5))
    return img,new_image,region,flip,[newleft,newtop,newright,bottom]



def deal_move(top, left, bottom, right,img):
    w,h = img.size
    new_image = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    width = right-left
    height = bottom-top
    newleft = int(max(left-width*0.05,0))
    newright = int(min(right+0.05*width,w))
    newtop = int(max(top-0.3*height,0))
    region = img.crop([newleft,newtop,newright,bottom])
    new_image.paste(region, (newleft,newtop))
    flip = img.transpose(Image.FLIP_LEFT_RIGHT)
    # width, height = img.size
    # offimg = ImageChops.offset(img,5,5)
    # offimg.paste((0,0,0),(0,0,5,height))
    # offimg.paste((0,0,0),(0,0,width,5))
    return img,new_image,region,flip,[newleft,newtop,newright,bottom]