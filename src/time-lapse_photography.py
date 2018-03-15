#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
time lapse photography
"""
import time


import numpy as np
import cv2


INTERVAL = 1
FPS = 20  # flips per seconds
RESOLUTION = (640, 480)


def time_lapse_video(fps=20.0, resolution=(640, 480), interval=None):
    """
    record a video
    :param fps: how many flip per seconds
    :param resolution:
    :param interval:
    :return:
    """
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, resolution)

    try:

        while cap.isOpened():
            ret, frame = cap.read()
            if ret is True:
                frame = cv2.flip(frame, 0)

                # rotate 180 degree
                frame = rotate_image(frame, degree=180)
                # write the flipped frame
                out.write(frame)

                # cv2.imshow('frame', frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                time.sleep(interval or INTERVAL)
            else:
                break

    finally:
        # Release everything if job is finished or not exit properly
        cap.release()
        out.release()
        cv2.destroyAllWindows()


def rotate_image(image, degree=0.0, scale=1.0):
    """
    rotate a image
    :param image: image that is to rotate
    :param degree: how many degrees to rotate
    :param scale: zoom with scale
    :return:
    """
    height, width = image.shape[:2]
    center = (width / 2, height / 2)

    # rotate
    trans_mat = cv2.getRotationMatrix2D(
        center=center, angle=degree, scale=scale)
    rotated = cv2.warpAffine(src=image, M=trans_mat, dsize=(width, height))
    return rotated


if __name__ == "__main__":
    time_lapse_video()
