#coding=gbk
import cv2
import numpy as np
import pyrealsense2 as rs
import os

# ����
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
i = 0
profile = pipe.start(cfg)

while True:
    # ��ȡͼƬ֡
    frameset = pipe.wait_for_frames()
    color_frame = frameset.get_color_frame()
    color_img = np.asanyarray(color_frame.get_data())

    # ����ͨ����˳��ΪRGB
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', color_img)
    k = cv2.waitKey(1)
    # Esc�˳���
    if k == 27:
        cv2.destroyAllWindows()
        break
    # ����ո񱣴�ͼƬ
    elif k == ord(' '):
        i = i + 1
        cv2.imwrite(os.path.join("D:\\Realsense\\pic_capture", str(i) + '.jpg'), color_img)
        print("Frames{} Captured".format(i))


pipe.stop()