import cv2 as cv
import numpy as np
import pyautogui as pag


button_img_dir = "../image/button.PNG"
screen_img_dir = "../image/test_01.jpeg"


button = cv.imread(button_img_dir, 0)
screen_rgb = cv.imread(screen_img_dir)
screen_grey = cv.cvtColor(screen_rgb, cv.COLOR_BGR2GRAY)
print button.shape
print screen_rgb.shape

width, height = button.shape[:2][::-1]

# cv.imshow("button", button)
# cv.imshow("screen", screen_rgb)
# cv.imshow("screen_grey", screen_grey)
# cv.waitKey(0)

res = cv.matchTemplate(screen_grey, button, cv.TM_CCOEFF_NORMED)
print "res_shape:", res.shape
print res

threshold = 0.7
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    left_top = pt
    right_bottom = (pt[0] + width, pt[1] + height)
    cv.rectangle(screen_rgb, pt, right_bottom, (0, 255, 255), 1)
# cv.imshow("res", screen_rgb)
# cv.waitKey(0)


left_x, left_y = left_top
right_x, right_y = right_bottom
click_x = int((left_x + right_x) / 2.0)
click_y = int((left_y + right_y) / 2.0)
print click_x, click_y
cv.rectangle(screen_rgb, (click_x, click_y), (click_x + 1, click_y + 1), (0, 255, 255), 1)
cv.imshow("res", screen_rgb)
cv.waitKey(0)

pag.click(x=click_x, y=click_y, button="left")

