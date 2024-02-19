import matplotlib.pyplot as plt
import numpy as np
import cv2

img = np.zeros((640, 1080, 3), np.uint8)
cv2.putText(img, 'text', (475, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()
img_encode = cv2.imencode('.jpg', img)[1]
print(f'img: {img.size}, encode: {img_encode.size}')
img_bytes = img_encode.tobytes()
ing = np.frombuffer(img_bytes, dtype=np.uint8)
a = cv2.imdecode(ing, cv2.IMREAD_COLOR)
plt.imshow(a)
plt.show()
