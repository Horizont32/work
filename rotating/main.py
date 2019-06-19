import cv2
import numpy as np
import os
import math
import constants
import func
import matplotlib.pyplot as plt

files = os.listdir(constants.data_path)
print(files)
os.chdir(os.path.join(os.getcwd(), 'chosen_for_analysys'))
func.ensure_dir(constants.ext_path, constants.data_path)
kek = 1
num = 1
blocksize = 13*constants.default_scale_factor/constants.scale_factor  # blocksize/C is 21/15, 9/7 is good
varC = round(8*constants.default_scale_factor/constants.scale_factor)  # prev varC = 8
for file in files:
    print(os.getcwd())
    print(os.access(file, os.F_OK))
    image = cv2.imread(file, 0)
    # cv2.imshow('kek1', image)
    shape = image.shape
    image2 = cv2.resize(image, (int(shape[1]/constants.scale_factor), int(shape[0]/constants.scale_factor)))
    image2 = cv2.resize(image, dsize=None, fx = 2, fy =2, interpolation=cv2.INTER_LANCZOS4)  ## Increasing a resolution
    # image2 = image2[(shape[0]-1024):shape[0], 0:shape[1]]
    # cv2.imshow('cropped', image2)
    # cv2.waitKey(0)
    img = cv2.medianBlur(image2, 7)  #9 was good
    cv2.imshow('image', img)
    cv2.waitKey(0)
    # img = cv2.GaussianBlur(image2, (5, 5), sigmaX=0.5, borderType=cv2.BORDER_DEFAULT)
    # cv2.imshow('kek1', img)
    cimg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, math.ceil(blocksize), varC)  # Default
    # contours, hierarchy = cv2.findContours(img, 1, 1)
    # cnt = contours
    # big_contour = []
    # max = 0
    # print(cnt)
    # for i in cnt:
    #     area = cv2.contourArea(i)  # --- find the contour having biggest area ---
    #     print(area)
    #     if area > max:
    #         max = area
    #         big_contour.append(i)
    # print(len(big_contour))
    # print(cv2.contourArea(big_contour[len(big_contour)-3]))

    # final = cv2.drawContours(cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR), big_contour, -1, (0, 0, 255), 3)
    # cv2.imshow('final', final)
    # cv2.waitKey(0)
    """https://www.tutorialspoint.com/opencv/opencv_adaptive_threshold.htm - look here for vars meanings
    https://docs.opencv.org/3.4/d7/d1b/group__imgproc__misc.html#ga72b913f352e4a1b1b397736707afcde3 - here for python
    """
    # TODO: Itarative search of variable C meaning, till it will find 3 points on the radiuses from 0.95 to 1.05 from defalt with radS from minrad_in_PX to maxrad_in_PX
    # Canny edge detection.
    cimg = cv2.Canny(img, 100, 120)
    print(str(cimg.shape) + " shape")
    cv2.imshow('cimg', cimg)
    cv2.waitKey(0)
    if kek == 1:
        cent_arr = func.find_main_center(cimg, round(constants.minCentRad), round(constants.maxCentRad))
        print(str(cent_arr) + ' main cent')
        cut_img = func.cut_image(image2, cent_arr, 2*50) # image2 replaced image
        perf_cent = func.find_real_center_on_cut_img(cut_img[0], round(constants.minCentRad), round(constants.maxCentRad), blocksize, varC)
        NAT_cent = func.iterated_center(cut_img[1], [perf_cent[0], perf_cent[1]])
        print(perf_cent, NAT_cent)
        cent_big_circle = func.find_big_circle_center(cimg, round(
            2*175/2*constants.default_scale_factor/constants.scale_factor),
                                                      round(
                                                          2*180/2*constants.default_scale_factor/constants.scale_factor))
        print('big cent ' + str(cent_big_circle))
        real_center = func.define_real_center(cent_arr, cent_big_circle)
        print(str(real_center) + ' Real cent')
        print(blocksize, cent_arr, cent_big_circle)
        scale_pix_in_mm = func.scale(150/2, cent_arr)  # Here cent_arr was cent_big_circle and 188/2 was 445/2
        print(str(scale_pix_in_mm) + ' scale')
        min_mark_rad_px = func.marker_rad_in_px(constants.markDIAmm, scale_pix_in_mm)[0]
        max_mark_rad_px = func.marker_rad_in_px(constants.markDIAmm, scale_pix_in_mm)[1]
        print(str(min_mark_rad_px) + ' MinMarkRad', str(max_mark_rad_px) + ' MaxMarkRad')
        blocksize = max_mark_rad_px * 1
        # print(max_mark_rad_px, blocksize)
        mindist_px = int(constants.dist_marks_mm * scale_pix_in_mm)
        # mark_arr = func.find_mark_cent(cimg, round(constants.minMarkRad), round(constants.maxMarkRad))
        mark_arr = func.find_mark_cent(cimg, min_mark_rad_px, max_mark_rad_px, mindist_px)
        main_rads = func.mark_cent_rad_calc(mark_arr, real_center)
        print('Radiusy raspologenia tochek ' + str(main_rads))
        main_mark_angles = func.mark_angle_calc(mark_arr, real_center)
        func.draw_circle_and_center(cimg, cent_big_circle, mark_arr)
        func.draw_circle_and_center(cimg, cent_arr, mark_arr)
        cv2.imwrite(constants.ext_path + '/%010d' % int(kek-1) + constants.file_ext, image2)
        kek += 1
        cv2.imshow('WITH MARKS!', cimg)
        cv2.waitKey(0)
    else:
        child_main_cent = func.find_main_center(cimg, constants.minCentRad, constants.maxCentRad)  # Находим главный центр(шпиндель) на текущем изображении
        child_big_cent = func.find_big_circle_center(cimg, round(
            2*350/2*constants.default_scale_factor/constants.scale_factor),
                                                      round(
                                                          2*370/2*constants.default_scale_factor/constants.scale_factor))  # Finding center of a big circle
        real_child_center = func.define_real_center(child_main_cent, child_big_cent)
        # print('Real_child_cent_coords are ' + str(real_child_center))
        child_mark_cent = func.find_mark_cent(cimg, min_mark_rad_px, max_mark_rad_px, mindist_px)  # Находим
        # центры маркеров
        child_mark_rads = func.mark_cent_rad_calc(child_mark_cent, child_main_cent)  # Находим радиусы, на которых лежат центры маркеров
        cnt = func.check_rads_number(main_rads, child_mark_rads)
        print(file, cnt, child_main_cent)
        while not cnt == constants.number_of_points and cnt < 1:
            varC = func.check_varC(child_mark_rads, varC, constants.number_of_points)
            cimg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                         cv2.THRESH_BINARY, math.ceil(blocksize), varC)
            print(varC)
            func.draw_circle_and_center(cimg, constants.scale_factor * child_main_cent,
                                        constants.scale_factor * child_mark_cent)
            # cv2.imshow('kek', cimg)
            # cv2.waitKey(0)
            child_mark_cent = func.find_mark_cent(cimg, min_mark_rad_px, max_mark_rad_px, mindist_px)
            child_mark_rads = func.mark_cent_rad_calc(child_mark_cent, child_main_cent)
            cnt = func.check_rads_number(main_rads, child_mark_rads)
            print(cnt, child_mark_rads)
        else:
            pass
        child_mark_angles = func.mark_angle_calc(child_mark_cent, child_main_cent)  # Вычисляем углы, на которых находятся маркеры
        point_rad = func.check_rad(main_rads, child_mark_rads)  # Находим радиусы, на которых лежат центры маркеров
        print('centers of markers ' + '\n' + str(child_mark_cent), '\nПозиции(радиусы) положения точек ' + str(child_mark_rads), '\nУглы расположения точек ' + str(child_mark_angles), '\nРадиус точки, по которой поворачиваем ' + str(point_rad))
        point_angle = func.check_angle(point_rad, child_mark_rads, child_mark_angles)
        print('УГОЛ ТОЧКИ ' + str(point_angle), '\nРЕАЛЬНЫЕ УГЛЫ НА НАЧАЛЬНОМ ИЗОБРАЖЕНИИ ' + str(main_mark_angles))
        found_marker_angle_on_origin = func.same_point_angle_on_origin_image(point_rad, main_rads, main_mark_angles)
        rot_angle = func.check_rotation_angle(found_marker_angle_on_origin, point_angle)
        print(str(rot_angle) + ' ANGLE')

        """Часть кода, в которой поворачиваем и перемещаем проверяем точность поворота и перемещения"""
        # rot_img_check = func.rotate(cimg, child_main_cent, rot_angle, image2.shape)
        # shift_img_check = func.shift_center(rot_img_check, real_center, child_main_cent, image2.shape)
        # mark_cent_check = func.find_mark_cent(shift_img_check, min_mark_rad_px,
        #                                       max_mark_rad_px, mindist_px)   # Проверка положения центров новых точек
        # на довернутом изображении относительно ПЕРВОГО изображения, сравнивать надо с ним. Тут мы только находим
        # эти новые центры
        # checked_center = func.find_main_center(shift_img_check, round(constants.minCentRad),
        #                                        round(constants.maxCentRad))
        # print(func.find_main_center(shift_img_check, round(constants.minCentRad), round(constants.maxCentRad)))
        # func.draw_circle_and_center(shift_img_check, constants.scale_factor * checked_center,
        #                             constants.scale_factor * child_mark_cent)
        # cv2.imshow('shifted', shift_img_check)
        # cv2.waitKey(0)
        # print(mark_cent_check)
        # accuracy = func.check_accuracy(mark_arr, mark_cent_check)
        """Writing here a codepiece contains shifting and rotating of orig img using the scaling factor as u multiplying coefficient"""
        rot_img = func.rotate(image2, constants.scale_factor*NAT_cent, rot_angle, image2.shape)
        # shift_img = func.shift_center(rot_img, constants.scale_factor*real_center,
        #                               constants.scale_factor*child_main_cent, image2.shape)
        # func.draw_circle_and_center(shift_img, constants.scale_factor*child_main_cent, constants.scale_factor*child_mark_cent)  # рисуем центы и сами маркеры
        # func.draw_circle_and_center(shift_img, constants.scale_factor*cent_big_circle, constants.scale_factor*mark_arr)
        # print(func.find_main_center(shift_img, 50, 60), func.find_mark_cent(shift_img, 20, 26))
        # cv2.imshow('shifted', shift_img)
        # cv2.waitKey(0)
        print(str(num) + '.jpg')
        cv2.imwrite(constants.ext_path + '/%010d' % num + constants.file_ext, rot_img)
        num += 1
