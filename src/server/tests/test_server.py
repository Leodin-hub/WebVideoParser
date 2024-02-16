from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import cv2
import numpy as np
import uvicorn

img = np.zeros((640, 1080, 3), np.uint8) * 188
cv2.putText(img, 'Your video could be here', (130, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_encode = cv2.imencode('.jpg', img)[1]
img_byte = img_encode.tobytes()
app = FastAPI()


async def gen_frames():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_byte + b'\r\n')
        await asyncio.sleep(0.5)


@app.get('/')
def get_img():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8081)
