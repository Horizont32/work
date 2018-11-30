import cv2
import numpy as np
import os
import math
import constants

kek = 1


def ensure_dir(ext_path, data_path):
    dir_data = os.path.dirname(ext_path)
    dir_dest = os.path.dirname(data_path)
    if not os.path.exists(dir_data):
        os.makedirs(dir_data)
    if not os.path.exists(dir_dest):
        os.makedirs(dir_dest)


def scale(rad_in_mm, rad_in_px):
    return rad_in_px[2]/rad_in_mm  # Получаем масштаб в пикселях/мм


def marker_rad_in_px(mark_dia_in_mm, scale):
    rad_pix = mark_dia_in_mm * scale/2
    minrad_pix = round(int(rad_pix*0.95))
    maxrad_pix = round(int(rad_pix*1.4))
    return minrad_pix, maxrad_pix, rad_pix


def dist_between_marks_mm_to_pix(dist_in_mm, scale):
    dist_pix = dist_in_mm * scale
    return 0.95*dist_pix


def find_main_center(edited_image, minRad, maxRad):
    circ = cv2.HoughCircles(edited_image, cv2.HOUGH_GRADIENT, 1, 100,
                            param1=20, param2=10, minRadius=minRad, maxRadius=maxRad)[0][0] # Находим окружность с центром (главным центром)
    return circ


def find_big_circle_center(edited_image, minRad, maxRad):
    circ = cv2.HoughCircles(edited_image, cv2.HOUGH_GRADIENT, 1, 100,
                            param1=20, param2=2, minRadius=minRad, maxRadius=maxRad)[0][0] # Находим окружность с центром (главным центром)
    return circ


def find_mark_cent(edited_image, minRad, maxRad, min_dist_px):
    circ = cv2.HoughCircles(edited_image, cv2.HOUGH_GRADIENT, 1, minDist=min_dist_px,
                            param1=30, param2=15, minRadius=minRad, maxRadius=maxRad)[0]  # Находим окружность с центром маркера
    return circ


def mark_cent_rad_calc(mark_array, cent_array): # Нахер не надо функция, только 1 раз использую, если относительно 1 картинки поворот, а можно относительно предыдущей, но последний подход менее точный, ошибка копится.
    # rad = ((xarr-xcent)**2+(yarr-ycent)**2)**0.5
    # print(rad)
    # rads.append(rad) #Записываем массив радиусов, на которых лежат центры точек на родительской картинке
    rad = []
    for marker in mark_array:  # маркер тут уже - массив из 3 строк - х, у, и радиус
        rad.append(((marker[0] - cent_array[0])**2 + (marker[1] - cent_array[1])**2)**0.5)
    return rad


def mark_angle_calc(mark_array, cent_array):
    angles = []
    for marker_coord in mark_array:
        if marker_coord[0] >= cent_array[0] and marker_coord[1] <= cent_array[1]:  # 1st quarter
            angle = math.atan((cent_array[1] - marker_coord[1])/(marker_coord[0] - cent_array[0]))
        elif marker_coord[0] <= cent_array[0] and marker_coord[1] <= cent_array[1]:  # 2nd quart
            angle = math.atan((cent_array[0] - marker_coord[0])/(cent_array[1] - marker_coord[1])) + math.pi/2
        elif marker_coord[0] <= cent_array[0] and marker_coord[1] >= cent_array[1]:  # 3rd quart
            angle = math.atan((marker_coord[1] - cent_array[1]) / (cent_array[0] - marker_coord[0])) + math.pi
        elif marker_coord[0] >= cent_array[0] and marker_coord[1] >= cent_array[1]:  # 4th quarter
            angle = math.atan((marker_coord[0] - cent_array[0]) / (marker_coord[1] - cent_array[1])) + math.pi*3/2
        angles.append(math.degrees(angle))
    return angles


def check_rad(array_of_points_rads_in_origin, array_rad_exist_point):
    for origin_rad in array_of_points_rads_in_origin:
        for exist_rad in array_rad_exist_point:
            if 0.95*origin_rad < exist_rad < 1.05*origin_rad:
                return exist_rad


def check_varC(array_rad_exist_point, varC, number_of_points):
    if len(array_rad_exist_point) < number_of_points:
        varC -= 1
    elif len(array_rad_exist_point) > number_of_points:
        varC += 1
    return varC


def check_rads_number(array_of_points_rads_in_origin, array_rad_exist_point):
    cnt = 0
    for origin_rad in array_of_points_rads_in_origin:
        for exist_rad in array_rad_exist_point:
            if 0.95 * origin_rad < exist_rad < 1.05 * origin_rad:
                cnt += 1
    return cnt


def same_point_angle_on_origin_image(point_rad, array_of_points_rads_in_origin, origin_angles_array):
    for origin_rad in array_of_points_rads_in_origin:
        if 0.95*origin_rad < point_rad < 1.05*origin_rad:
            angle_index = array_of_points_rads_in_origin.index(origin_rad)
            return origin_angles_array[angle_index]


def check_angle(point_rad, array_rad_exist_point, array_angles_exist_point):
    rad_index_in_array = array_rad_exist_point.index(point_rad)
    return array_angles_exist_point[rad_index_in_array]


def check_rotation_angle(angle_of_point_origin, angle_of_point_exist_image):
    # if angle_of_point_exist_image > angle_of_point_origin:
    #     rot_angle = -angle_of_point_exist_image + angle_of_point_origin
    # else:
    rot_angle = angle_of_point_origin - angle_of_point_exist_image
    return rot_angle


def rotate(src, cent_array, rot_angle, shape):
    M = cv2.getRotationMatrix2D((cent_array[0], cent_array[1]), rot_angle, 1)
    rot_img = cv2.warpAffine(src, M, (shape[1], shape[0]), flags=cv2.INTER_NEAREST)
    return rot_img


def shift_center(src, main_cent_origin, main_cent_current, shape):
    dx = main_cent_origin[0] - main_cent_current[0]
    dy = main_cent_origin[1] - main_cent_current[1]
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    shifted_img = cv2.warpAffine(src, M, (shape[1], shape[0]), flags=cv2.INTER_LANCZOS4)
    return shifted_img


def check_accuracy(mark_cent_origin, mark_cent_after_shifting):
    diff_x = mark_cent_origin[0] - mark_cent_after_shifting[0]
    diff_y = mark_cent_origin[1] - mark_cent_after_shifting[1]
    abs_diff = math.sqrt(diff_x**2 + diff_y**2)
    return diff_x, diff_y, abs_diff


def draw_circle_and_center(src, main_center, mark_arr):
    cv2.circle(src, (main_center[0], main_center[1]), main_center[2], (50, 255, 80), 2)  # draw the main circle
    # draw the center of the main circle
    cv2.circle(src, (main_center[0], main_center[1]), 2, (0, 0, 255), 1)
    for i in mark_arr:
        cv2.circle(src, (i[0], i[1]), i[2], (193, 0, 120), 2)  # draw the markers
        # draw the center of the markers
        cv2.circle(src, (i[0], i[1]), 2, (0, 0, 255), 1)