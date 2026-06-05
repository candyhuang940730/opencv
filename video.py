import cv2

cap = cv2.VideoCapture(1)

# 使用迴圈取得下一幀圖片
while True:
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (0, 0), fx=1.2, fy=1.2)
        cv2.imshow('video', frame)
    else:
        break
    # 影片速度調整
    # cv2.waitKey(1)

    if cv2.waitKey(10) == ord('q'):
        break
        # 按Q可結束影片
