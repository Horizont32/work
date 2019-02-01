import os
import cv2

files = os.listdir(os.getcwd())

for file in files:
    print(os.getcwd())
    print(os.access(file, os.F_OK))
    image = cv2.imread(file, 0)
    # cv2.imshow('kek1', image)
    shape = image.shape
    print(shape)