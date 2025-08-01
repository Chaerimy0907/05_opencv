import cv2
import matplotlib.pylab as plt
import pyzbar.pyzbar as pyzbar
import webbrowser

# 이미지 불러오기
#img = cv2.imread('../img/frame.png')

# 이미지 그레이 스케일로 변환
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cap = cv2.VideoCapture(0)
last_data = None

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue

    # 이미지 불러오기
    #img = cv2.imread('../img/frame.png')

    # 이미지 그레이 스케일로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    decoded = pyzbar.decode(gray)

    for d in decoded:
        x, y, w, h = d.rect

        barcode_data = d.data.decode('utf-8')
        barcode_type = d.type

        text = '%s (%s)' % (barcode_data, barcode_type)

         #cv2.rectangle(img, (d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), 
        #             (0,255,0), 20)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2.putText(img, text, (d.rect[0], d.rect[1] - 50), 
        #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        if barcode_data.startswith("http") and barcode_data != last_data:
            print(f"웹사이트로 이동 : {barcode_data}")
            webbrowser.open(barcode_data)
            last_data = barcode_data

    cv2.imshow('camera', img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyWindow()

# 결과 출력
#plt.imshow(img)
#plt.imshow(gray, cmap='gray')
#plt.show()

# 디코딩
#decoded = pyzbar.decode(gray)
#print(decoded)

#for d in decoded:
#    print(d.data.decode('utf-8'))
#    barcode_data = d.data.decode('utf-8')
#    print(d.type)
#    barcode_type = d.type

#    text = '%s (%s)' % (barcode_data, barcode_type)

#    cv2.rectangle(img, (d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), 
#                  (0,255,0), 20)
#    cv2.putText(img, text, (d.rect[0], d.rect[1] - 50), 
#                cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 2, cv2.LINE_AA)

#plt.imshow(img)
#plt.show()

#cv2.waitKey(0)
#cv2.destroyAllWindows()