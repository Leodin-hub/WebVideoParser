from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
# from moduls.model_yolo import Model
from moduls.streamer import Streamer
import asyncio
import uvicorn



# model = Model()
# camera = cv2.VideoCapture('http://211.132.61.124/mjpg/video.mjpg')

app = FastAPI()
templates = Jinja2Templates(directory='templates')
streamer = Streamer()


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('page.html', {'request': request})


async def gen_frames():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + streamer.get_img() + b'\r\n')
        await asyncio.sleep(0.03)


@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.post('/postdata')
def post_data(request: Request, stream=Form()):
    streamer.producer.send('url_video', bytes(stream, 'utf-8'))
    # producer.send('url_video', bytes(stream, 'utf-8'))
    return templates.TemplateResponse('page.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)