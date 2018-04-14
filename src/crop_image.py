#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
crop image. during developing
为了一页能在一个屏幕显示，截图两侧有黑边，需要裁剪
"""
# todo: 将所有的截图进行分类后，再进行裁剪，
# 这样或许可以解决部分截图大小不一样的问题。
import os
import cv2
import numpy as np
from ROI_calculate import calculate_roi_2


SMALL_CONTOUR_AREA = 10

filename_full = "../screen/0.jpeg"
# filename_full = "../screen/0_crop.jpeg"
image = cv2.imread(filename_full)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# in order to find contours of a image properly, convert it to threshold

# how to confirm the threshold?
# ret, thresh = cv2.threshold(image_gray, 177, 255, 0)

# adaptive threshold instead of hard code.
thresh = cv2.adaptiveThreshold(
    src=image_gray, maxValue=255,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY,
    blockSize=11, C=2)
# find contours
img, contours, hierarchy = cv2.findContours(
    thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# those lines are used to test whether the contours are properly found.
# img_cnt = cv2.drawContours(image, contours, -3, (0, 255, 0), 1)
# cv2.imshow("contours_1", img_cnt)
# cv2.waitKey(0)
# cv2.imwrite("../screen/contours_1.jpeg", image)

# remove contours whose areas are too small
contours = [c for c in contours if cv2.contourArea(c) > 10]
# find the contour with largest area
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt = contours[max_index]
area_max = areas[max_index]

x, y, w, h = calculate_roi_2(cnt)

# crop until area is to an set value, proper?
# remove the contour whose area is same with image, get the next contour?
# judge if the area of contour is not less than a value, crop?
img_to_keep = image[y:y+h, x:x+w, :]  # why y first?

filename_path, filename = os.path.split(filename_full)
filename_crop_pre, extension = os.path.splitext(filename)
filename_crop = filename_crop_pre + "_crop" + extension
filename_full_crop = os.path.join(filename_path, filename_crop)
cv2.imwrite(filename_full_crop, img_to_keep)

