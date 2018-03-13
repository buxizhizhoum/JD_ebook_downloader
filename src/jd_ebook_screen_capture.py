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
from find_button import FindButton


button_img_dir = "../image/button.PNG"
screen_img_dir = "../image/test_01.jpeg"


def button_center():
    button_cp = FindButton(button_img_dir, screen_img_dir).button_center()
    return button_cp


def image_diff(img_1, img_2):
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
    difference = cv.subtract(image_1, image_2)
    res = np.any(difference)

    if res is True:
        # two image is same
        return True
    else:
        # two image is not same
        return False


def confirm_loop():
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
    # todo: buffer page to judge whether it is same with last screen
    pag.alert(text="Please switch window to where the screen will be shot.",
              title="Alert",
              button='OK')
    confirm_loop()
    for page in range(page_num):
        time.sleep(0.3)

        file_name = "../screen/%s.jpeg" % page
        screen_img = pag.screenshot()
        screen_img.save(file_name)

        # pag.click(click_x, click_y, button="left")
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
        # pag.click(click_x, click_y, button="left")
        pag.press("right")


if __name__ == "__main__":
    # FindButton(button_img_dir, screen_img_dir).show_button_loc()
    click_x, click_y = button_center()
    # click_x, click_y = 781, 56

    page_num = 317
    capture_screen_and_save(page_num)




