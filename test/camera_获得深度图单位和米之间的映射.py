import pyrealsense2 as rs

# Create a pipeline
pipeline = rs.pipeline()
# Start streaming
profile = pipeline.start()

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)
