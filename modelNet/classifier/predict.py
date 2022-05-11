def judge(classfication,img):
    class_name,pro = classfication.detect_image(img)
    return class_name,pro
