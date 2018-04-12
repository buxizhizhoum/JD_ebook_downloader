#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
crop image. during developing
"""

import cv2
import numpy as np


image = cv2.imread("../screen/0.jpeg")
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# cv2.imshow("image_gray", image_hsv)
# cv2.waitKey(0)

# ret, thresh = cv2.threshold(image_gray, 90, 255, 0)
# img, contours, hierarchy = cv2.findContours(
#     thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# # img = cv2.drawContours(img, contours, -3, (0, 255, 255), 3)
# # cv2.imshow("contours", img)
# # cv2.waitKey(0)
# areas = [cv2.contourArea(c) for c in contours]
# max_index = np.argmax(areas)
# cnt = contours[max_index]
#
# x, y, w, h = cv2.boundingRect(cnt)
# img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 20)
# cv2.imshow("contours", img)
# cv2.waitKey()
# cv2.destroyAllWindows()

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
hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
COLOR_MIN = np.array([20, 20, 20], np.uint8)
COLOR_MAX = np.array([255, 255, 255], np.uint8)
frame_threshed = cv2.inRange(hsv_img, COLOR_MIN, COLOR_MAX)
imgray = frame_threshed
ret,thresh = cv2.threshold(frame_threshed,127,255,0)
img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

# Find the index of the largest contour
areas = [cv2.contourArea(c) for c in contours]
max_index = np.argmax(areas)
cnt = contours[max_index]

x, y, w, h = cv2.boundingRect(cnt)
cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.imshow("Show", image)
cv2.waitKey()
cv2.destroyAllWindows()


