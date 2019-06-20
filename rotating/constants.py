import os

path = os.getcwd()
data_path = os.path.join(path, 'chosen_for_analysys')
ext_path = os.path.join(path, '4048_test_full')
file_ext = '.jpg'
default_scale_factor = 1
scale_factor = 1  # Default scale_factor is 3, that`s why we devide it in 3
markDIAmm = 8
dist_marks_mm = 2*20
number_of_points = 1
minMarkRad = int(2*6*default_scale_factor/scale_factor)  # minRad for 900*1200, edit using scale
maxMarkRad = int(2*17*default_scale_factor/scale_factor)
minCentRad = int(2*176/2*default_scale_factor/scale_factor)
maxCentRad = int(2*180/2*default_scale_factor/scale_factor)

# Cent params: 680/2 712/2
if __name__ == '__main__':
    print('kek')