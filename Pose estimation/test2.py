
import cv2
import numpy as np

background = cv2.imread('images/bg.jpg')

R_arm = cv2.imread('images/R_arm.jpg')
L_arm = cv2.imread('images/L_arm.jpg')
D_arm = cv2.imread('images/D_arm.jpg')

imcollection = {'R_arm': R_arm, 'L_arm': L_arm, 'D_arm': D_arm}

while True:

    background[200:200+346, 200: 200+240] = imcollection['R_arm']
    cv2.waitKey(100)
    cv2.imshow('posenet', background)
    background[200:200+346, 200: 200+240] = imcollection['L_arm']
    cv2.waitKey(100)
    cv2.imshow('posenet', background)
    background[200:200+346, 200: 200+240] = imcollection['D_arm']
    cv2.waitKey(100)
    cv2.imshow('posenet', background)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
