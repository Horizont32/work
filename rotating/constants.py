import os

path = os.getcwd()
data_path = os.path.join(path, 'vid1')
ext_path = os.path.join(path, 'edited2')
file_ext = '.jpg'
default_scale_factor = 1
scale_factor = 1  # Default scale_factor is 3, that`s why we devide it in 3
markDIAmm = 23
dist_marks_mm = 125
number_of_points = 1
minMarkRad = int(35*default_scale_factor/scale_factor)  # minRad for 900*1200, edit using scale
maxMarkRad = int(40*default_scale_factor/scale_factor)
minCentRad = int(280/2*default_scale_factor/scale_factor)
maxCentRad = int(300/2*default_scale_factor/scale_factor)

# Cent params: 680/2 712/2
if __name__ == '__main__':
    print('kek')