#!/usr/bin/python
# -*- coding: UTF-8 -*-

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import pcl

filename = './1542614507.194016000'
p = pcl.load(filename + '.pcd')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = []
y = []
z = []
for i in range(p.size):
    x.append(p[i][0])
    y.append(p[i][1])
    z.append(p[i][2])

ax.scatter(x, y, z, c='k', marker='.', s=0.1)

plt.show()
