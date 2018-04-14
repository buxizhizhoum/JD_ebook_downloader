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
    """
    find the ROI rec, this method works, but relay on the contour type.
    :param contour:
    :param bounding_rec_width: the width of bounding rec
    :param bounding_rec_height: the height of bounding rec
    :return:
    """
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


def calculate_roi_2(contour):
    """
    a better method to find the rec of the content.

    This method group point to 3 group, the points at top, the points at left
    and the points at right.

    the points at the top could be grouped by extract the point with min y,
    after that, the left_top point and the right_top point could be extracted.

    the group at left could be extracted by compare x coordinate with the point
    at left_top, same logic to the group at right.

    the left_top point is the point in the group top, and with the min x,
    the right_top point is the point in the group right and with the max x,
    the left_bottom point is the point in the group left and with the max y,
    the right_bottom point is the point in the group right and with the max y
    :param contour:
    :return:
    """
    if len(contour) < 4:
        # contour should contain at least 4 point.
        raise ValueError("bad contour")

    sorted_array = sorted(contour, key=lambda x: x[0][1])

    # the points are sorted by coordinate y,
    # the first point is belong to group_top
    p_top_0 = sorted_array[0][0]

    # todo: if there are too many points to process, point processed
    # should be removed from sorted_array, however, there are only
    # several points, do not remove the point not cause heavy
    # calculation in the following processes.

    # group of points at the top of the contour
    group_top = group_maker(sorted_array, base_point=p_top_0, according="y")

    # the top left point should be the point in the group_top
    # and with the smallest x coordinate
    group_top.sort(key=lambda x: (x[1], x[0]))  # sort by y and x, y priority.
    p_left_top = group_top[0]  # the point with min y and min x

    # find the point with max x coordinate, that is the point at right top
    x_max_top = p_left_top
    for point in group_top:
        if point[0] > x_max_top[0]:
            x_max_top = point

    p_right_top = x_max_top

    group_left = group_maker(sorted_array,
                             base_point=p_left_top, according="x")

    group_left.sort(key=lambda x: x[1])
    p_left_bottom = group_left[-1]

    group_right = group_maker(sorted_array,
                              base_point=p_right_top, according="x")

    group_right.sort(key=lambda x: x[1])
    p_right_bottom = group_right[-1]

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


def group_maker(points, base_point, according):
    if according in ("x", "X", 0):
        according = 0
    elif according in ("y", "Y", 1):
        according = 1
    else:
        raise ValueError("Wrong according value, x or y")
    # find points who belongs to group_top
    res = []
    for point in points:
        point = point[0]
        tmp_height = abs(point[according] - base_point[according])
        if tmp_height < DELTA_HEIGHT_ERROR:
            res.append(point)

    return res


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
    res = calculate_roi_2(test_cnt)
    print res
