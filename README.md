# 01. QR 코드 인식 및 자동 웹사이트 이동 프로젝트

## 개요
- 웹캠으로 QR 코드 인식
- QR 코드 안에 URL이 포함되어 있으면 **자동으로 웹사이트 실행**
- 같은 QR 코드일 때는 한 번만 실행, **QR 코드가 바뀌면 새로 실행**

---

## 사용 기술
- OpenCV
- pyzbar (QR 인식 라이브러리)
- webbrowser (웹사이트 열기)

---

## 코드 분석

### 1. 라이브러리 불러오기
- 설치 후 코드 실행 시 imortError가 뜨는 경우
  [여기](https://www.microsoft.com/en-US/download/details.aspx?id=40784) 에서 vcredist_x64.exe(python 64-bit인 경우)를 설치하면 된다
```bash
pip install pyzbar
```

```python
import cv2                        # 웹캠 사용 및 화면 출력
import pyzbar.pyzbar as pyzbar    # QR 코드 인식
import webbrowser                 # URL 자동 실행
```

### 2. 변수 초기화
```python
cap = cv2.VideoCapture(0)  # 기본 웹캠 사용
last_data = None           # 마지막으로 인식한 QR 데이터 저장
```

### 3. 웹캠으로 프레임 읽기
- 카메라가 열려 있는 동안 반복
- 한 프레임씩 읽어오고, 읽기 실패 시 다음 반복으로 넘어감
```python
while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue
```

### 4. QR 코드 인식
- 이미지를 그레이스케일로 변환 (인식 성능 향상)
- pyzbar.decode() : QR코드를 인식해 데이터 반환
```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
decoded = pyzbar.decode(gray)
```

### 5. 인식된 QR 코드 처리
- QR 코드의 위치 정보(rect)와 데이터(data) 추출
- barcode_data : QR 코드 안의 문자열
- barcode_type : QR 코드인지 바코드인지 타입 정보
```python
for d in decoded:
    x, y, w, h = d.rect
    barcode_data = d.data.decode('utf-8')
    barcode_type = d.type
```

### 6. 화면에 사각형과 텍스트 표시
- QR 코드 영역을 초록색 사각형으로 표시
- QR 코드의 데이터와 타입을 화면에 출력
```python
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
cv2.putText(img, text, (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (0, 255, 0), 2, cv2.LINE_AA)
```

### 7. URL이면 자동으로 열기
- QR 코드 데이터가 http로 시작하는 URL일 경우에만 실행
- 마지막으로 인식한 데이터와 다를 때만 웹사이트를 열어 중복 실행 방지
```python
if barcode_data.startswith("http") and barcode_data != last_data:
    print(f"웹사이트로 이동 : {barcode_data}")
    webbrowser.open(barcode_data)
    last_data = barcode_data
```

### 8. 카메라 종료
- q를 누르면 프로그램 종료
- 웹캠 연결 해제 및 창 닫기
```python
if cv2.waitKey(1) == ord('q'):
    break

cap.release()
cv2.destroyWindow()
```

---

## 실행 화면 예시
<img width="1920" height="1080" alt="실행결과1" src="https://github.com/user-attachments/assets/15748e62-b0d1-4817-8fa7-f057972b5b3d" />
- 실습용으로 받은 QR 코드 인식 후 웹사이트가 열린 화면

 
<img width="1920" height="1080" alt="실행결과2" src="https://github.com/user-attachments/assets/4f408d79-a862-42db-bfcc-3f0f864e1f58" />
- 네이버 주소 QR코드를 생성한 후 QR 코드 인식 후 웹사이트가 열린 화면 
