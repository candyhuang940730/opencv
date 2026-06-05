import cv2

# 1. 初始化攝影機與分類器
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break

    # 2. 影像前處理
    frame = cv2.resize(frame, (540, 320))  # 縮小尺寸，提升效能
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 將鏡頭影像轉換成灰階 (這時候 gray 才真正成為影像矩陣)

    # 3. 偵測人臉 (必須在 gray 變數產生後才呼叫)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # 4. 繪製框線
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('oxxostudio', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()