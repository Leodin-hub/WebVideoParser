from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from moduls.streamer import Streamer
from kafka import KafkaProducer
import uvicorn



# 'http://211.132.61.124/mjpg/video.mjpg'

app = FastAPI()
templates = Jinja2Templates(directory='templates')
streamer = Streamer()
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('page.html', {'request': request})


# async def gen_frames():
#     while True:
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + streamer.get_img() + b'\r\n')
#         await asyncio.sleep(0.03)


@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(streamer.get_img(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.post('/postdata')
def post_data(request: Request, stream: str = Form()):
    if stream is None:
        stream = ''
    producer.send('url_video', value=bytes(stream, 'utf-8'), timestamp_ms=1000)
    return templates.TemplateResponse('page.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)