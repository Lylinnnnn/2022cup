#coding=gbk
import cv2
import numpy as np
videocap = cv2.VideoCapture('../img/test2.mp4')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# fps = videocap.get(cv2.CAP_PROP_FPS)
size = (int(videocap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videocap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# videowrite = cv2.VideoWriter('../img/dealedtest2.avi',fourcc,fps,size)
import cv2
firstframe=None
framesdst = np.zeros((1,size[1],size[0]))
print(framesdst.shape)
i=0
while(videocap.isOpened()):
    ret,frame=videocap.read()
    if ret:
        i += 1
        pp=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)      #将RGB转换为GSV
        if firstframe is None:                     #前面已经设置为空
            firstframe=pp
            continue
        frameDelta=cv2.absdiff(firstframe,pp)      #帧差法，将firstframe和gray的差值输出到frameDelta中
        if i%10 == 0:
            framesdst = np.insert(framesdst,0,frameDelta,axis = 0)
    else:
        break
videocap.release()
print(framesdst.shape)

stdmat = np.std(framesdst,axis=0)
mean = np.mean(stdmat)
_, attention = cv2.threshold(np.uint8(stdmat),mean,255,cv2.THRESH_BINARY)
print(attention)
cv2.imshow('1',attention)
cv2.waitKey()