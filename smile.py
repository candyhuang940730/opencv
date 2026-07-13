import cv2
import numpy as np
from deepface import DeepFace

cap = cv2.VideoCapture(0)


def putText(source, x, y, text, scale=2.5, color=(255, 255, 255)):
    org = (x, y)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = scale
    thickness = 5
    lineType = cv2.LINE_AA
    cv2.putText(source, text, org, fontFace, fontScale, color, thickness, lineType)


a = 0  # 白色圖片透明度
n = 0  # 檔名編號
happy = 0  # 是否有 happy 的變數
sec = 4  # 倒數秒數初始值

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # 調整 waitKey 的時間，100 毫秒（0.1秒）跑一次迴圈，這樣比較好控制倒數計時與降溫
    key = cv2.waitKey(100)

    ret, img = cap.read()
    if not ret:
        print("Cannot receive frame")
        break

    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    w = int(img.shape[1] * 0.5)
    h = int(img.shape[0] * 0.5)
    img = cv2.resize(img, (w, h))
    white = 255 - np.zeros((h, w, 4), dtype='uint8')

    # 將 BGR 丟給 DeepFace（因為你前面把 img 轉成 BGRA 了，DeepFace 不支援 4 頻道影像）
    # 另外指定 detector_backend='opencv' 確保它使用剛才下載的 xml
    try:
        bgr_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 這裡多加一個 actions=['emotion'] 確保只跑情緒，加快速度
        predictions = DeepFace.analyze(bgr_img, actions=['emotion'], detector_backend='opencv', enforce_detection=False)

        if predictions and len(predictions) > 0:
            emotion_data = predictions[0]['emotion']
            # 💡 把這行印出來，看看你的電腦抓到的數值是多少
            print(f"真實微笑數值: {emotion_data['happy']:.2f}% | 中性數值: {emotion_data['neutral']:.2f}%")

            # 💡 放寬門檻：有時候微微笑只有 5%~10%，我們把門檻從 30 降到 10.0
            if emotion_data['happy'] > 10.0:
                happy += 1
            else:
                happy = 0
        else:
            happy = 0

    except Exception as e:
        happy = 0
        # 💡 這行非常重要！如果程式底層死掉了，它會把原因印在終端機上
        print("偵測發生錯誤，原因:", e)

    # 觸發拍照條件
    if happy == 1 or key == 32:  # 剛開始微笑或按下空白鍵
        if a == 0:  # 避免重複觸發
            a = 1
            sec = 3.0  # 設為 3 秒倒數

    if key == ord('q'):
        break

    output = img.copy()

    # 拍照與倒數特效邏輯
    if a > 0:
        if sec > 0:
            # 正在倒數
            photo = img.copy()
            putText(output, 10, 70, str(int(sec) + 1), scale=2.0, color=(0, 255, 255))
            sec -= 0.1  # 因為 waitKey(100) 是 0.1 秒，所以每次減 0.1
        else:
            # 倒數結束，觸發閃光燈效果（白畫面慢慢變透明）
            output = cv2.addWeighted(white, a, photo, 1 - a, 0)
            a -= 0.2  # 閃光燈消退速度

            if a <= 0:
                a = 0
                n += 1
                # 儲存時要記得轉回 BGR 或是去除去除透明度，不然一般看圖軟體可能打不開
                save_img = cv2.cvtColor(photo, cv2.COLOR_BGRA2BGR)
                cv2.imwrite(f'photo-{n}.jpg', save_img)
                print(f'儲存成功: photo-{n}.jpg')

    cv2.imshow('Smile Camera', output)

cap.release()
cv2.destroyAllWindows()