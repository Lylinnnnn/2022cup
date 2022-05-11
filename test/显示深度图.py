import numpy as np
import cv2

def showDepthPic(filePath=r"F:\Final\img\nano_0.npy"):
    img_depth = np.load(filePath)
    img_depth = np.uint16(img_depth)
    print(img_depth.shape)
    x,y,_ = img_depth.shape
    print(img_depth[540,960,0])
    print(img_depth[1000,960,0])
    img_depth = cv2.resize(img_depth, (int(y / 2), int(x / 2)))
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(img_depth, alpha=0.03), cv2.COLORMAP_JET)
    cv2.imshow("depth",depth_colormap)
    return depth_colormap

def showColorPic(filePath=r"F:\Final\img\nano_0.png"):
    img_rgb = cv2.imread(filePath)
    x,y,_ = img_rgb.shape
    print(x,y)
    img_rgb = cv2.resize(img_rgb, (int(y / 2), int(x / 2)))
    cv2.imshow("color",img_rgb)
    return img_rgb


depthMat = showDepthPic()
colorMat = showColorPic()
print(depthMat.shape)
print(colorMat.shape)

cv2.imshow("mixed",depthMat+colorMat)

cv2.waitKey()