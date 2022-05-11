# -*- coding:utf-8 -*-

import pyrealsense2 as rs
from PIL import Image
import numpy as np
import cv2
import os
import time

def turnon_camera():
    try:
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

        profile = pipeline.start(config)  # Start streaming
        sensor_dep = profile.get_device().first_depth_sensor()
        sensor_rgb = profile.get_device().first_color_sensor()
        
        sensor_dep.set_option(rs.option.laser_power, 16)
        sensor_dep.set_option(rs.option.accuracy, 3)
        sensor_dep.set_option(rs.option.motion_range, 60)
        sensor_dep.set_option(rs.option.filter_option, 3)
        sensor_dep.set_option(rs.option.confidence_threshold, 6)
        
        sensor_rgb.set_option(rs.option.enable_auto_exposure, 1.0)
        sensor_rgb.set_option(rs.option.gain, 64)
        sensor_rgb.set_option(rs.option.backlight_compensation, 0)
        sensor_rgb.set_option(rs.option.brightness, 0)
        sensor_rgb.set_option(rs.option.contrast, 50)
        sensor_rgb.set_option(rs.option.gamma, 300)
        sensor_rgb.set_option(rs.option.hue, 0)
        sensor_rgb.set_option(rs.option.saturation, 50)
        sensor_rgb.set_option(rs.option.sharpness, 0)
        sensor_rgb.set_option(rs.option.enable_auto_white_balance, 1.0)
        
        print("Current Parameters")
        return pipeline
    except RuntimeError:
        print("未检测到摄像头!")
    finally:
        print("摄像机打开!")

def get_data(pipeline):
    align_to = rs.stream.color
    align = rs.align(align_to)

    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)

    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    depth_data = np.asanyarray(aligned_depth_frame.get_data(), dtype="float16")
    color_image = np.asanyarray(color_frame.get_data())
    depth_data = np.uint8((depth_data - np.min(depth_data)) / (np.max(depth_data) - np.min(depth_data)) * 255)
    depth_data = depth_data[:, :, None]
    temp_image = np.array(color_image)[:, :, ::-1]
    png_image = np.concatenate([temp_image, depth_data], 2)
    img = Image.fromarray(png_image)
    return img


def get_camera_image(pipeline,flag):
    try:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        if flag:
            return color_image
        else:
            return depth_colormap
    except RuntimeError:
        print("固件问题!")
    finally:
        i=1

def get_data_more(pipeline,color_path,depth_path,saved_count):
    align_to = rs.stream.color
    align = rs.align(align_to)
    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)

    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    depth_data = np.asanyarray(aligned_depth_frame.get_data(), dtype="float16")
    # depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imwrite(os.path.join((color_path), "{}.png".format(saved_count)), color_image)
    # 深度信息由采集到的float16直接保存为npy格式


    #------------------------------------------------------
    #加上那个每隔几毫秒保存
    while saved_count<=4:
        cv2.imwrite(os.path.join((color_path), "{}.png".format(saved_count)), color_image)
        time.sleep(0.5)
        saved_count += 1
def get_data_sig(pipeline,color_path,depth_path,saved_count):
    align_to = rs.stream.color
    align = rs.align(align_to)
    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)

    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    depth_data = np.asanyarray(aligned_depth_frame.get_data(), dtype="float16")
    # depth_image = np.asanyarray(aligned_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imwrite(os.path.join((color_path), "{}.png".format(saved_count)), color_image)
    # 深度信息由采集到的float16直接保存为npy格式


    #------------------------------------------------------
    #加上那个每隔几毫秒保存
    np.save(os.path.join((depth_path), "{}".format(saved_count)), depth_data)

def turnoff_camera(pipeline):
    pipeline.stop()
    print("摄像机关闭!")
pip  = turnon_camera()
get_data(pip).save(r'F:\Final\1.png')
