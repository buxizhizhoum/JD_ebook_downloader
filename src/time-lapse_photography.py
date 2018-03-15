#!/usr/bin/python
# -*- coding: utf-8 -*-
import time


import numpy as np
import cv2


INTERVAL = 60
FPS = 20
RESOLUTION = (640, 480)


def time_lapse_video(fps=20.0, resolution=(640, 480), interval=None):
    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, resolution)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret is True:
            frame = cv2.flip(frame, 0)

            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # time.sleep(interval or INTERVAL)
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    time_lapse_video()
