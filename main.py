import cv2

img = cv2.imread('dog.jpg')

cv2.imshow('img', img)
cv2.waitKey(0)