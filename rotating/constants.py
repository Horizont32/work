import os

path = os.getcwd()
data_path = os.path.join(path, 'img2')
imsize = 300
ext_path = os.path.join(path, 'edited')
file_ext = '.jpg'
default_scale_factor = 3
scale_factor = 1  # Default scale_factor is 3, that`s why we devide it in 3
markDIAmm = 16
dist_marks_mm = 125
number_of_points = 3
minMarkRad = int(20*default_scale_factor/scale_factor)  # minRad for 900*1200, edit using scale
maxMarkRad = int(30*default_scale_factor/scale_factor)
minCentRad = int(50*default_scale_factor/scale_factor)
maxCentRad = int(80*default_scale_factor/scale_factor)


if __name__ == '__main__':
    print('kek')