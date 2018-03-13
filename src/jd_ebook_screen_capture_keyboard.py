#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
make a copy of jd ebook by capture screen.
"""
import os
import time

import cv2 as cv
import numpy as np
import pyautogui as pag


def image_diff(img_1, img_2):
    """
    this is to judge whether the 2 screen is already same, if same, it means
    it is already the end of the file, the program should stop.

    this is not completed yet.

    :param img_1:
    :param img_2:
    :return:
    """
    image_1 = cv.imread(img_1)
    image_2 = cv.imread(img_2)

    difference = cv.subtract(image_1, image_2)
    res = np.any(difference)

    if res is True:
        # two image is same
        return True
    else:
        # two image is not same
        return False


def image_diff_2(image_1, image_2):
    """
    to judge whether 2 screen shot is same or not, not completed yet.
    :param image_1:
    :param image_2:
    :return:
    """
    difference = cv.subtract(image_1, image_2)
    res = np.any(difference)

    if res is True:
        # two image is same
        return True
    else:
        # two image is not same
        return False


def confirm_loop():
    """
    provide a alert window to remind user to change window to capture screen.
    provide a button for user to confirm that the window has been changed to
    the window which is to capture.
    :return:
    """
    confirm = pag.confirm(text="Have you switched to the screen which "
                               "you are to capture?",
                          title="confirm",
                          buttons=["Yes", "No"])
    while True:
        if confirm == "Yes":
            return True
        else:
            time.sleep(3)
            confirm = pag.confirm(text="Have you switched to the screen which "
                                       "you are to capture?",
                                  title="confirm",
                                  buttons=["Yes", "No"])


def capture_screen_and_save(page_num):
    """
    capture the screen and save it.
    :param page_num:
    :return:
    """
    pag.alert(text="Please switch window to where the screen will be shot.",
              title="Alert",
              button='OK')
    confirm_loop()
    for page in range(page_num):
        time.sleep(0.3)

        file_name = "../screen/%s.jpeg" % page
        screen_img = pag.screenshot()
        screen_img.save(file_name)

        pag.press("right")


def capture_screen_compare_and_save(page_num):
    # todo: buffer page to judge whether it is same with last screen
    # locateCenterOnScreen
    # locate
    for page in range(page_num):
        file_current = "../screen/%s.jpeg" % page
        if page == 0:
            print("Please switch window to where the screen will be shot.")
            time.sleep(3)
            diff = False
        else:
            time.sleep(1)
            file_before = "../screen/%s.jpeg" % (page - 1)
            diff = image_diff(file_current, file_before)

        screen_img = pag.screenshot()
        screen_img.save("../screen/%s.jpeg" % page)

        # judge if it is already the end of the file by compare screen shot
        # with screen shot before
        if diff is True:
            os.remove(file_current)
            print("It is already the end of the file.")
            break
        pag.press("right")


if __name__ == "__main__":
    page_num = 317
    capture_screen_and_save(page_num)




