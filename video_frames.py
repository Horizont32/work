import cv2
import os

# import cv2
# print(cv2.__version__)
# vidcap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
# success,image = vidcap.read()
# count = 0
# success = True
# # os.makedirs('/data')
# while success:
#   cv2.imwrite("./data/%010d.jpg" % count, image)     # save frame as JPEG file
#   success,image = vidcap.read()
#   print( 'Read a new frame: ', success)
#   count += 1

video = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
num = 0
ret = True
while ret:
    ret, frame = video.read()
    if not num % 60:
        print(num)
        # cv2.imwrite("./data/%010d.jpg" % num, frame)
    # print('Recording frame No ', num)
    num += 1
