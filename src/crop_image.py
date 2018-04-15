#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
crop image.

there are black side at the lateral of the photo, needs to crop.
"""
import os
import traceback

import cv2
import numpy as np

from ROI_calculate import calculate_roi_2


SMALL_CONTOUR_AREA = 10


def crop_image(filename_full):
    """
    crop the black side of an image.
    :param filename_full: the path of the image to crop
    :return:
    """
    image = cv2.imread(filename_full)
    if image is None:
        return

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
    contours = [c for c in contours if cv2.contourArea(c) > SMALL_CONTOUR_AREA]
    # find the contour with largest area
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt = contours[max_index]

    x, y, w, h = calculate_roi_2(cnt)
    print(x, y, w, h)

    # crop until area is to an set value, proper?
    # remove the contour whose area is same with image, get the next contour?
    # judge if the area of contour is not less than a value, crop?
    img_to_keep = image[y:y + h, x:x + w, :]  # why y first?

    # todo: does it is possible to save files in the original path?
    filename_full_crop = new_filename(filename_full)
    cv2.imwrite(filename_full_crop, img_to_keep)


def new_filename(filename_full):
    """
    creat new filename.
    :param filename_full:
    :return:
    """
    filename_path, filename = os.path.split(filename_full)
    filename_crop_pre, extension = os.path.splitext(filename)
    filename_crop = filename_crop_pre + "_crop" + extension
    filename_full_crop = os.path.join(filename_path, filename_crop)
    return filename_full_crop


def crop_images(filenames_list):
    """
    crop images whose path is in a list.
    :param filenames_list: the list of images path
    :return:
    """
    for filename in filenames_list:
        print(filename)

        try:
            crop_image(filename)
            # delete original file after crop.
            os.remove(filename)
        except Exception as e:
            print e
            print traceback.format_exc()


if __name__ == "__main__":
    # filename_full = "../screen/0.jpeg"
    filename_full = "C:/Software/screen_capture/books/ThinkPython/215.jpeg"
    crop_image(filename_full)
