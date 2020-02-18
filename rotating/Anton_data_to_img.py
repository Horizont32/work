import cv2
import os
import itertools


path = 'C:/Users/Artem/YandexDisk/Programming/work/imgs_to_write_data/'
os.chdir(path)
imgs = os.listdir()
print(os.listdir())
print(os.getcwd())

frame_n_arr = [0, 42, 91, 142, 191, 241, 288, 337, 387, 437, 488, 532, 579, 629, 677, 727, 775, 825, 872, 922, 970,
               1017, 1067]


def forces_array(Fmin, Fmax, frames_array):
    forces_arr = []
    for real in range(1, len(frames_array)):
        for i in range(frames_array[real]-frames_array[real-1]):
            if (real % 2) or (real == 1):
                current_force = Fmin + i * (Fmax - Fmin) / (frames_array[real]-frames_array[real-1])
                forces_arr.append(current_force)
            elif not(real % 2):
                current_force = Fmax - i * (Fmax - Fmin) / (frames_array[real]-frames_array[real-1])
                forces_arr.append(current_force)
    return forces_arr


def fill_full_forces_array(input_array, Cycles_N):
    output_array = []
    for i in range(Cycles_N):
        for elem in input_array:
            output_array.append(elem)
    return output_array


def data_to_img(imgs, forces_arr):
    for (img, force) in itertools.zip_longest(imgs, forces_arr):
        pic = cv2.imread(img, 0)
        new_pic = cv2.putText(pic, 'Force = {}'.format(force), (500, 200), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 0), 5)
        cv2.imshow('New', new_pic)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


forces_arr = forces_array(200, 1000, frame_n_arr)
print(forces_arr)
print(len(forces_arr))
# full_arr = fill_full_forces_array(forces_arr, 2)
# print(full_arr)
data_to_img(imgs, forces_arr)