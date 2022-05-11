import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
for s in device.sensors:
    print(s.get_info(rs.camera_info.name))

cfg = pipeline.start(config)
device1 = cfg.get_device()
for s in device1.sensors:
    print(s.get_info(rs.camera_info.name))
