import cv2
import matplotlib.pylab as plt
import pyzbar.pyzbar as pyzbar

# 이미지 불러오기
img = cv2.imread('../img/frame.png')

# 이미지 그레이 스케일로 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 결과 출력
#plt.imshow(img)
plt.imshow(gray, cmap='gray')
plt.show()

# 디코딩
decoded = pyzbar.decode(gray)
print(decoded)

cv2.waitKey(0)
cv2.destroyAllWindows()