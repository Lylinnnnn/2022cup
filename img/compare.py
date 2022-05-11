

from PIL import Image
import numpy as np
pc_img = Image.open(r'F:\Final\img\4_7_2_2_3.png')
nano_img = Image.open(r'F:\Final\img\nano_0.png')

pc_img = np.array(pc_img)

nano_img = np.array(nano_img)
nano_img = nano_img[:,:,::-1]
Image.fromarray(nano_img).show()
# pc_r = pc_img[:,:,0]+50
# pc_g = pc_img[:,:,1]
# pc_b = pc_img[:,:,2]
# pc_d = pc_img[:,:,3]
#
# nano_r = nano_img[:,:,0]
# nano_g = nano_img[:,:,1]
# nano_b = nano_img[:,:,2]
# nano_d = nano_img[:,:,3]
#
#
# print(pc_img.shape,nano_img.shape)
#
# print(np.max(pc_r),np.mean(pc_r),np.median(pc_r),np.sum(pc_r),np.std(pc_r))
# print(np.max(nano_r),np.mean(nano_r),np.median(nano_r),np.sum(nano_r),np.std(nano_r))
#
# print(np.max(pc_g),np.mean(pc_g),np.median(pc_g),np.sum(pc_g),np.std(pc_g))
# print(np.max(nano_g),np.mean(nano_g),np.median(nano_g),np.sum(nano_g),np.std(nano_g))
#
# print(np.max(pc_b),np.mean(pc_b),np.median(pc_b),np.sum(pc_b),np.std(pc_b))
# print(np.max(nano_b),np.mean(nano_b),np.median(nano_b),np.sum(nano_b),np.std(nano_b))
#
# print(np.max(pc_d),np.mean(pc_d),np.median(pc_d),np.sum(pc_d),np.std(pc_d))
# print(np.max(nano_d),np.mean(nano_d),np.median(nano_d),np.sum(nano_d),np.std(nano_d))
#
# pc_r = pc_r[:, :, None]
# pc_g = pc_g[:, :, None]
# pc_b = pc_b[:, :, None]
# pc_d = pc_d[:, :, None]
# # temp_image = np.array(color_image)[:, :, ::-1]
# print(pc_r.shape)
# pc_img = np.concatenate([pc_r,pc_g,pc_b,pc_d], 2)
# Image.fromarray(pc_img).save(r'F:\Final\img\pc_dealed.png')