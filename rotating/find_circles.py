import cv2
import numpy as np

imsize = 300
img = cv2.imread('d1.jpg', 0)
img = cv2.resize(img, (3*imsize, 4*imsize))
cv2.imshow('detected circles', img)
cv2.waitKey(0)
img = cv2.medianBlur(img, 7)
# blur = cv2.GaussianBlur(img,(5,5),0)
# ret3,cimg = cv2.threshold(blur,0,255,cv2.THRESH_OTSU)
# cimg = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
# cc, cimg = cv2.threshold(blur, 255,cv2.THRESH_BINARY, 11, 2)
cimg = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 21, 15)
circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 100,
                            param1=20, param2=10, minRadius=10, maxRadius=27)

# kek, circles = cv2.findCirclesGrid(cimg, (3, 3), flags=cv2.CALIB_CB_ASYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING)
# cv2.findCirclesGrid()
# im2, circles, hierarchy = cv2.findContours(cimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(circles)

# vis = cimg.copy()
# cv2.drawContours(vis, circles, 0, (255, 50, 0), 1, cv2.LINE_AA,  0)
# cv2.imshow('contours', vis)
# cv2.waitKey(0)

circles2 = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 100,
                            param1=20, param2=10, minRadius=50, maxRadius=60) # Находим окружность с центром (главным центром)

# circles = np.uint16(np.around(circles))
#
print(len(circles[0]))
print(circles2[0])
print(len(circles2[0]))
xarr = []
yarr = []
for i in circles[0]:
    xarr.append(i[0])
    yarr.append(i[1])
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (50, 255, 80), 2)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 1)

xarr = np.array(xarr)
yarr = np.array(yarr)

for i in circles2[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (50, 255, 80), 2)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 1)

def rad_calc(): # Нахер не надо функция, только 1 раз использую, если относительно 1 картинки поворот, а можно относительно предыдущей, но последний подход менее точный, ошибка копится.
    xcent=circles2[0][0][0]
    ycent=circles2[0][0][1]
    rcent=circles2[0][0][2]
    # тут надо сделать массив для точек маркеров
    rads = []
    for i in range(len(xarr)):
        rad = ((xarr[i]-xcent)**2+(yarr[i]-ycent)**2)**0.5
        print(rad)
        rads.append(rad) #Записываем массив радиусов, на которых лежат центры точек на родительской картинке
    return rads

def find_dots_nth_image():
    pass

def find_rad_exist_point():
    pass

def check_rad():
    for rad in rad_calc():
        if 0.98*rad < find_rad_exist_point() < 1.15*rad:
            return True

rad_calc()
cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()