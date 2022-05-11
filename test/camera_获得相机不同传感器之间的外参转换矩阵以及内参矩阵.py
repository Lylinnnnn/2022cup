#coding=gbk

import pyrealsense2 as rs


# 获得相机不同传感器之间的外参转换矩阵以及内参矩阵
def getMat():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)
    cfg = pipeline.start(config)
    device = cfg.get_device()
    name = device.get_info(rs.camera_info.name)
    print(name)
    profile = cfg.get_stream(rs.stream.depth)
    profile1 = cfg.get_stream(rs.stream.color)
    intr = profile.as_video_stream_profile().get_intrinsics()
    intr1 = profile1.as_video_stream_profile().get_intrinsics()
    extrinsics = profile1.get_extrinsics_to(profile)
    print(extrinsics)
    print("深度传感器内参：", intr)
    print("RGB相机内参:", intr1)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
profile = pipeline.start(config)
frames = pipeline.wait_for_frames()
depth = frames.get_depth_frame()
color = frames.get_color_frame()
# 获取内参
depth_profile = depth.get_profile()
print(depth_profile)
# <pyrealsense2.video_stream_profile: Depth(0) 640x480 @ 30fps Z16>
print(type(depth_profile))
# <class 'pyrealsense2.pyrealsense2.stream_profile'>
print(depth_profile.fps())
# 30
print(depth_profile.stream_index())
# 0
print(depth_profile.stream_name())
# Depth
print(depth_profile.stream_type())
# stream.depth
print('', depth_profile.unique_id)
# <bound method PyCapsule.unique_id of <pyrealsense2.video_stream_profile: Depth(0) 640x480 @ 30fps Z16>>

color_profile = color.get_profile()
print(color_profile)
# <pyrealsense2.video_stream_profile: Color(0) 960x540 @ 30fps BGR8>
print(type(color_profile))
# <class 'pyrealsense2.pyrealsense2.stream_profile'>
print(depth_profile.fps())
# 30
print(depth_profile.stream_index())
# 0

cvsprofile = rs.video_stream_profile(color_profile)
dvsprofile = rs.video_stream_profile(depth_profile)

color_intrin = cvsprofile.get_intrinsics()
print(color_intrin)
# 960x540  p[493.975 265.065]  f[673.775 673.824]  Brown Conrady [0.151657 -0.50863 -0.000700379 -0.000860805 0.471284]
depth_intrin = dvsprofile.get_intrinsics()
print(depth_intrin)
# [ 640x480  p[306.57 254.527]  f[461.453 461.469]  None [0 0 0 0 0] ]
extrin = depth_profile.get_extrinsics_to(color_profile)
print(extrin)
# rotation: [0.999965, 0.00762357, 0.00331248, -0.00754261, 0.999688, -0.0238027, -0.0034929, 0.0237769, 0.999711]
# translation: [0.000304107, 0.0142351, -0.00695471]
