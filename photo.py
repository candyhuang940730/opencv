import cv2

img = cv2.imread('dog.jpg')

img1 = cv2.resize(img, (400, 800)) # 調整大小(px)
img2 = cv2.resize(img, (0, 0), fx = 0.5, fy = 0.5)  # 調整大小(倍數)

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.waitKey(0)