# 01. QR 코드 인식 및 자동 웹사이트 이동 프로젝트

## 개요
- 웹캠으로 QR 코드 인식
- QR 코드 안에 URL이 포함되어 있으면 **자동으로 웹사이트 실행**
- 같은 QR 코드일 때는 한 번만 실행, **QR 코드가 바뀌면 새로 실행**

---

## 사용 기술
- Python
- OpenCV (cv2)
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
<img width="1920" height="891" alt="실행결과1" src="https://github.com/user-attachments/assets/8ec81106-1785-4c85-bfd1-4dd453bad7ad" />

- 실습용으로 받은 QR 코드 인식 후 웹사이트 열림

 
<img width="1920" height="1038" alt="실행결과2" src="https://github.com/user-attachments/assets/9586206b-88ab-4c45-aebb-71ca70c7c5a0" />

- 네이버 주소 QR코드를 생성한 후 QR 코드 인식 후 네이버 사이트가 열림


---


# 02. ArUco 마커 실습

## 개요
- 웹캠으로 다각도 체커보드 사진 촬영 -> 카메라 캘리브레이션 -> ArUco 마커 인식 및 거리/각도 측정
- OpenCV의 ArUco 모듈을 활용하여 **마커의 3D 위치와 회전 각도를 측정**
- 특정 조건(거리 30cm 이하)에서 **"STOP" / "GO" 텍스트 표시 기능** 추가

---

## 사용 기술
- Python
- OpenCV (cv2, cv2.aruco)
- Numpy
- Pickle (캘리브레이션 데이터 저장)

---

## 단계별 설명

### 1. 웹캠으로 체커보드 이미지 캡쳐 (photo.py)
- 웹캠 화면 출력
- 'a' 키 -> 현재 프레임을 '../img/' 폴더에 저장
- 'q' 키 -> 종료
- **체커보드 이미지를 여러 각도에서 촬영하기 위해 사용**
- 여러 각도에서 체커보드 이미지 10장 이상 저장

<img width="648" height="489" alt="실행결과3" src="https://github.com/user-attachments/assets/c52eeca7-fc7f-4671-bd1f-ef3ed7fcccbd" />

- 체커보드 이미지 촬영 후 지정한 경로에 저장

### 2. 카메라 캘리브레이션 (calibration.py)
- 촬영한 체커보드 이미지들을 불러와서 **카메라 내부 파라미터(Camera Matrix)** 와 **왜곡 계수(Distortion Coefficients)** 계산
- 다양한 체커보드 크기 및 전처리 방식(CLAHE, Blur, Adaptive Threshold)으로 검출 성공률 향상
- 성공 시 'camera_calibration.pkl' 파일로 저장
- 'camera_calibration.pkl' 파일은 ArUco 마커 인식 시 필수 : 촬영 시 체커보드가 프레임 전체에 잘 보이고 다양한 각도에서 찍는 것이 정확도를 높임

<img width="1273" height="501" alt="실행결과6" src="https://github.com/user-attachments/assets/06e84351-c849-4334-94dc-ce0fbab78e5c" />

- 캘리브레이션 성공 후 생성된 `camera_calibration.pkl'을 저장한 보정전/후

### 3. ArUco 마커 인식 (ScanArucomarker2.py)
- 'camera_calibration.pkl' 불러오기 -> 왜곡 보정
- 웹캠 영상에서 ArUco 마커 검출
- 마커의 **ID, 3D 위치(tvec), 회전(rvec)** 계산
- 마커 중심에 좌표축 표시, 정보 텍스트 출력

<img width="627" height="501" alt="실행결과7" src="https://github.com/user-attachments/assets/544f3ed2-b979-41c3-aefd-c3a148e63f3f" />

- 실행 결과

### 4. ArUco 마커 인식 + STOP/GO 텍스트
- 3번과 동일하게 마커 인식 및 3D 포즈 추정
- **카메라와 마커 간 거리가 30cm 이하일 경우 -> 빨간색 "STOP!" 텍스트**
- **30cm 초과일 경우 -> 초록색 "GO!" 텍스트**

<img width="1009" height="402" alt="10" src="https://github.com/user-attachments/assets/021833fe-35ee-49ba-958a-375a2ab53892" />

- GO! / STOP!
