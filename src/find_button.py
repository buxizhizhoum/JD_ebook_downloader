#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
find the location of a button in the screen.
"""
import cv2 as cv
import numpy as np


threshold = 0.9


class FindButton(object):
    def __init__(self, button_dir, screen_dir):
        self.button_dir = button_dir
        self.screen_dir = screen_dir
        self.rec_color = (0, 255, 255)
        self.rec_width = 1

    @classmethod
    def read_img(cls, img_dir):
        img_rgb = cv.imread(img_dir)
        return img_rgb

    def pre_process(self, img_dir):
        # button = cv.imread(self.button_dir, 0)
        # screen_rgb = cv.imread(self.screen_dir)
        # screen_grey = cv.cvtColor(screen_rgb, cv.COLOR_BGR2GRAY)
        img_rgb = self.read_img(img_dir)
        img_grey = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        return img_grey

    def button_size(self):
        button_img = self.pre_process(self.button_dir)
        width, height = button_img.shape[:2][::-1]
        return width, height

    def button_loc(self):
        screen = self.pre_process(self.screen_dir)
        button = self.pre_process(self.button_dir)
        width, height = self.button_size()

        res = cv.matchTemplate(screen, button, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        locations = []
        for pt in zip(*loc[::-1]):
            left_top = pt
            right_bottom = (pt[0] + width, pt[1] + height)

            locations.append((left_top, right_bottom))

        if locations:
            return locations[-1]
        else:
            return None

    def button_loc_all(self):
        screen = self.pre_process(self.screen_dir)
        button = self.pre_process(self.button_dir)
        width, height = self.button_size()

        res = cv.matchTemplate(screen, button, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        locations = []
        for pt in zip(*loc[::-1]):
            left_top = pt
            right_bottom = (pt[0] + width, pt[1] + height)

            locations.append((left_top, right_bottom))

        if locations:
            return locations
        else:
            return None

    def button_center(self):
        button_location = self.button_loc()
        if button_location is None:
            return None

        left_top, right_bottom = self.button_loc()

        left_x, left_y = left_top
        right_x, right_y = right_bottom

        center_x = int((left_x + right_x) / 2.0)
        center_y = int((left_y + right_y) / 2.0)
        return center_x, center_y

    def show_button_loc(self):
        screen_rgb = self.read_img(self.screen_dir)
        button_location = self.button_loc()
        if button_location is None:
            print("Button is not founded!")
            return

        # 有可能发现多个值，但是只取最后一个
        left_top, right_bottom = button_location
        cv.rectangle(screen_rgb, left_top, right_bottom, self.rec_color,
                     self.rec_width)
        cv.imshow("res", screen_rgb)
        cv.waitKey(0)


if __name__ == "__main__":
    button_img_dir = "../image/button.PNG"
    screen_img_dir = "../image/test_01.jpeg"

    find_butn = FindButton(button_img_dir, screen_img_dir)
    find_butn.show_button_loc()
    print find_butn.button_loc()
