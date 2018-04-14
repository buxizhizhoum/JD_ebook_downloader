#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
calculate the ROI of an image with the contour
return the x, y, w, h where x, y is the coordinate of top left,
w is the width, h is the height.

the shape of the figure is something like below, the rectangle at the bottom
is the scroll bar when print screen, what we want is the rec inside.

                left_top   --------------  right_top           -----
                           |            |                        |
                           |            |                        |
                           |            |                        |
                           |            |                        |  h
                           |            |  right_bottom          |
                  ---------              ----------              |
                  |     left_bottom               |              |
                  ---------------------------------            -----

                           |------w-----|

                  |----------w_modified-----------|


ideally the point left_top and right_top should be at the same horizon line,
so to left_bottom and right bottom, however, in practise they may have a
slight misalignment, and this is why DELTA_HEIGHT_ERROR is used, it is the
tolerance.

same situation may happen to the point that should be at the same vertical line
and DELTA_WIDTH_ERROR is used to tolerate this misalignment
"""
MINIMUM_WIDTH = 100
DELTA_HEIGHT_ERROR = 10
DELTA_WIDTH_ERROR = 10


def calculate_roi(contour, bounding_rec_width, bounding_rec_height):
    if len(contour) < 4:
        # contour should contain at least 4 point.
        raise ValueError("bad contour")

    sorted_array = sorted(contour, key=lambda x: x[0][1])

    p_left_top = sorted_array[0][0]
    p_right_top = sorted_array[1][0]

    # select the 2 points at top by calculate the minimum width
    i = 1
    flag = False  # flag of whether the point has been found
    # for index in range(i, len(contour)):
    while i < len(contour):
        # extract the 2 points at the top, abs(x1 - x0) should larger than
        # MINIMUM_WIDTH.
        tmp_width = abs(p_right_top[0] - p_left_top[0])
        if tmp_width < MINIMUM_WIDTH:
            p_right_top = sorted_array[i + 1][0]
        else:
            flag = True
            break

        i += 1

    if flag is False:
        return None

    current_width = abs(p_right_top[0] - p_left_top[0])
    assert MINIMUM_WIDTH <= current_width <= bounding_rec_width

    # delta height of the 2 point at top should not too large,
    # they should be on the same horizon line
    assert abs(p_right_top[1] - p_left_top[1]) <= DELTA_HEIGHT_ERROR

    # select the 2 points at the bottom by calculate whether the y is close to
    # the 2 points found above
    i += 1
    p_left_bottom = sorted_array[i][0]
    # for index in range(i, len(contour)):
    while i < len(contour):
        delta_h_left = abs(p_left_bottom[1] - p_left_top[1])
        if bounding_rec_height * 0.9 <= delta_h_left <= bounding_rec_height:
            # the point meet the requirement.
            # x coordinate should be on the same vertical line
            delta_x_left = abs(p_left_bottom[0] - p_left_top[0])
            if delta_x_left < DELTA_WIDTH_ERROR:
                break
        else:
            p_left_bottom = sorted_array[i + 1][0]
        i += 1

    i += 1
    p_right_bottom = sorted_array[i][0]
    while i < len(contour):
        delta_h_right = abs(p_right_bottom[1] - p_right_top[1])
        if bounding_rec_height * 0.9 <= delta_h_right <= bounding_rec_height:

            # calculate the delta y of the 2 points at bottom
            delta_y_bottom = abs(p_right_bottom[1] - p_left_bottom[1])
            # the 2 points at the bottom should have close y coordinate,
            # on idea situation they should be on the same horizon line
            assert delta_y_bottom < DELTA_HEIGHT_ERROR
            # x coordinate should be on the same vertical line
            delta_x_right = abs(p_right_bottom[0] - p_right_top[0])
            if delta_x_right < DELTA_WIDTH_ERROR:
                break

            break
        else:
            p_right_bottom = sorted_array[i + 1][0]

        i += 1

    x, y = p_left_top[0], p_left_top[1]
    w1 = abs(p_right_top[0] - p_left_top[0])
    w2 = abs(p_right_bottom[0] - p_left_bottom[0])
    # ideally they should be equal to each other
    assert abs(w1 - w2) < DELTA_WIDTH_ERROR

    h1 = abs(p_left_bottom[1] - p_left_top[1])
    h2 = abs(p_right_bottom[1] - p_right_top[1])
    # ideally they should be equal to each other
    assert abs(h1 - h2) < DELTA_HEIGHT_ERROR

    w = w1
    h = h1

    return x, y, w, h


if __name__ == "__main__":
    import numpy as np
    test_cnt = np.array([[[ 426,   1]],
                         [[ 426, 1052]],
                         [[ 425, 1053]],
                         [[  11, 1053]],
                         [[  11, 1058]],
                         [[  10, 1059]],
                         [[   0, 1059]],
                         [[   1, 1060]],
                         [[   1, 1079]],
                         [[   2, 1078]],
                         [[1699, 1078]],
                         [[1699, 1053]],
                         [[1275, 1053]],
                         [[1274, 1052]],
                         [[1274,    1]]])
    res = calculate_roi(test_cnt, 1079, 1078)
    print res
