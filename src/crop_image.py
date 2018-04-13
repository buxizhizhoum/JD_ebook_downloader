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

# cv2.imshow("thresh", thresh)
# cv2.waitKey(0)
# cv2.imwrite("../screen/thresh.jpeg", thresh)

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

img_cnt = cv2.drawContours(image, cnt, -3, (0, 255, 0), 3)
cv2.imshow("contours_2", img_cnt)
cv2.waitKey(0)
cv2.imwrite("../screen/contours_2.jpeg", image)

# tmp = cv2.minMaxLoc(cnt)
moment = cv2.moments(cnt)
cx = int(moment["m10"]/moment["m00"])
cy = int(moment["m01"]/moment["m00"])

"""
the shape of the figure is something like below, the rectangle at the bottom
is the scroll bar when print screen, what we want is the rec inside.

                left_top   --------------  right_top           -----
                           |            |                        |
                           |            |                        |
                           |            |                        |
                           |            |                        |  h
                           |            |                        |
                  ---------|            |----------              |
                  |        |            |         |              |
                  ---------------------------------            -----
                  
                           |------w-----|
                  
                  |----------w_modified-----------|
"""

# hull = cv2.convexHull(cnt, returnPoints=True)
hull = cv2.convexHull(cnt, returnPoints=False)
point_cnt = [cnt[index[0]] for index in hull]

img_convex = cv2.drawContours(image, point_cnt, -3, (0, 0, 255), 5)
point_cnt.sort(key=lambda x: x[0][1])
# todo: how to process the situation that more than 3 points are on
# todo: the top line?
p_left_top, p_right_top = point_cnt[0], point_cnt[1]
x_left_top, y_left_top = p_left_top[0][0], p_right_top[0][1]
x_right_top, y_right_top = p_right_top[0][0], p_right_top[0][1]

# p_left_bottom, p_right_bottom = point_cnt[-1], point_cnt[-2]
# img_convex = cv2.drawContours(image, hull, -3, (0, 0, 255), 5)
# cv2.imshow("img_convex", img_convex)
# cv2.waitKey(0)
# cv2.imwrite("../screen/img_convex.jpeg", img_convex)

# remove the point where y is the max will remove the bottom line,
# the problem is that there are more than 2 point at the bottom line

x, y, w, h = cv2.boundingRect(cnt)  # what is useful is the h
print x, y, w, h

w_modified = x_right_top - x_left_top

# lines below is to check whether ORI is right or not when developing.
# img_rec = cv2.rectangle(image, (x_left_top, y_left_top),
#                         (x_left_top + w_modified, y_left_top + h),
#                         (255, 0, 0), 2)
# cv2.imshow("contours", img_rec)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# crop until area is to an set value, proper?
# remove the contour whose area is same with image, get the next contour?
# judge if the area of contour is not less than a value, crop?
# img_to_keep = image[y:y+h, x:x+w, :]  # why y first?
img_to_keep = image[y_left_top:y_left_top+h,
                    x_left_top:x_left_top+w_modified, :]  # why y first?
# img_to_keep = image_gray[0:1080, 0:1700]
# cv2.imshow("crop", img_to_keep)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

filename_path, filename = os.path.split(filename_full)
filename_crop_pre, extension = os.path.splitext(filename)
filename_crop = filename_crop_pre + "_crop" + extension
filename_full_crop = os.path.join(filename_path, filename_crop)
cv2.imwrite(filename_full_crop, img_to_keep)
# 每张图裁剪完之后再寻找轮廓裁剪一次，可行否?
# 图片有个黑边，先去掉黑边再寻找，是否会好点?

# 轮廓，


# edge = cv2.Canny(image_gray, 200, 10)
# print edge
# cv2.imshow("edge", edge)
# cv2.waitKey(0)

# grad_x = cv2.Sobel(image_gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
# grad_y = cv2.Sobel(image_gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

# gradient = cv2.subtract(grad_x, grad_y)
# gradient = cv2.convertScaleAbs(gradient)
#
# cv2.imshow("gradient", gradient)
# cv2.waitKey(0)
#
# # binary
# image_b_w = cv2.threshold(gradient, 90, 255, cv2.THRESH_BINARY)
#
# cv2.imshow("image_b_w", image_b_w)
# cv2.waitKey(0)
#
# cv2.findContours()



# im = cv2.imread('shot.bmp')
# hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# COLOR_MIN = np.array([20, 20, 20], np.uint8)
# COLOR_MAX = np.array([255, 255, 255], np.uint8)
# frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
# imgray = frame_threshed
# ret,thresh = cv2.threshold(frame_threshed,127,255,0)
# img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#
# # Find the index of the largest contour
# areas = [cv2.contourArea(c) for c in contours]
# max_index = np.argmax(areas)
# cnt = contours[max_index]
#
# x, y, w, h = cv2.boundingRect(cnt)
# cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
# cv2.imshow("Show", image)
# cv2.waitKey()
# cv2.destroyAllWindows()


