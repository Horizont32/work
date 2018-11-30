import cv2
import numpy as np

class OriginImage:

    def __init__(self, path, imsize, minRad_for_markers, maxRad_for_markers, minRad_center, maxRad_center):
        self.path = path
        self.imsize = imsize
        self.minR_mark = minRad_for_markers
        self.maxR_mark = maxRad_for_markers
        self.minR_cent = minRad_center
        self.maxR_cent = maxRad_center

    def find_params(self):
        img = cv2.imread('d1.jpg', 0)
        img = cv2.resize(img, (3 * self.imsize, 4 * self.imsize))
        cv2.imshow('detected circles', img)
        cv2.waitKey(0)
        img = cv2.medianBlur(img, 7)

        cimg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 21, 15)

        circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 100,
                                   param1=20, param2=10, minRadius=self.minR_mark, maxRadius=self.maxR_mark)  # Находим маленькие метки

        circles2 = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 100,
                                    param1=20, param2=10, minRadius=self.minR_cent,
                                    maxRadius=self.maxR_cent)  # Находим окружность с центром (главным центром, вокруг которого все потом крутить)
