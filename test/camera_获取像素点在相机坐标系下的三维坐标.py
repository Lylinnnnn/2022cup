#coding=gbk

import pyrealsense2 as rs
import numpy as np
import cv2
import json


def get_aligned_images():
    frames = pipeline.wait_for_frames()  # �ȴ���ȡͼ��֡
    aligned_frames = align.process(frames)  # ��ȡ����֡
    aligned_depth_frame = aligned_frames.get_depth_frame()  # ��ȡ����֡�е�depth֡
    color_frame = aligned_frames.get_color_frame()  # ��ȡ����֡�е�color֡

    ############### ��������Ļ�ȡ #######################
    intr = color_frame.profile.as_video_stream_profile().intrinsics  # ��ȡ����ڲ�
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics  # ��ȡ��Ȳ�������������ϵת�������ϵ���õ���
    camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
                         'ppx': intr.ppx, 'ppy': intr.ppy,
                         'height': intr.height, 'width': intr.width,
                         'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()
                         }
    # �����ڲε�����
    with open('./intrinsics.json', 'w') as fp:
        json.dump(camera_parameters, fp)
    #######################################################

    depth_image = np.asanyarray(aligned_depth_frame.get_data())  # ���ͼ��Ĭ��16λ��
    depth_image_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)  # ���ͼ��8λ��
    depth_image_3d = np.dstack((depth_image_8bit, depth_image_8bit, depth_image_8bit))  # 3ͨ�����ͼ
    color_image = np.asanyarray(color_frame.get_data())  # RGBͼ

    # ��������ڲΡ���Ȳ�������ɫͼ�����ͼ����֡�е�depth֡
    return intr, depth_intrin, color_image, depth_image_3d, aligned_depth_frame


pipeline = rs.pipeline()  # ��������pipeline
config = rs.config()  # ��������config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # ����depth��
config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)  # ����color��
profile = pipeline.start(config)  # ���̿�ʼ
align_to = rs.stream.color  # ��color������
align = rs.align(align_to)
while True:
    intr, depth_intrin, rgb, depth, aligned_depth_frame = get_aligned_images()  # ��ȡ�����ͼ��������ڲ�
    # ������Ҫ�õ���ʵ��ά��Ϣ�����ص㣨x, y)�������������ĵ�Ϊ��
    x = 320
    y = 240
    dis = aligned_depth_frame.get_distance(x, y)  # ��x, y)�����ʵ���ֵ
    print("distance:",dis)
    camera_coordinate = rs.rs2_deproject_pixel_to_point(intr, [x, y], dis)
    # ��x, y)�����������ϵ�µ���ʵֵ��Ϊһ����ά������
    # ����camera_coordinate[2]��Ϊdis��camera_coordinate[0]��camera_coordinate[1]Ϊ�������ϵ�µ�xy��ʵ���롣
    print(camera_coordinate)

    cv2.imshow('RGB image', rgb)  # ��ʾ��ɫͼ��

    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        pipeline.stop()
        break
cv2.destroyAllWindows()
