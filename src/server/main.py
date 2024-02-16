from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from moduls.model_yolo import Model
from moduls.reading import Reading
from kafka import KafkaProducer, KafkaConsumer
import asyncio
import uvicorn


app = FastAPI()
model = Model()
reader = Reading()
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
consumer = KafkaConsumer('stream', group_id='group1', bootstrap_servers=['localhost:9092'],
                         auto_offset_reset='earliest')
# camera = cv2.VideoCapture('http://211.132.61.124/mjpg/video.mjpg')
templates = Jinja2Templates(directory='templates')


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('page.html', {'request': request})


async def gen_frames():
    while True:
        msg = consumer.poll()
        if msg:
            value = ''
            for m in msg:
                value = msg[m][0].value.decode('utf-8')
            print(value)
            img = reader.connect_redis.get(value)
            print(img)
        else:
            img = reader.img_wait
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
        await asyncio.sleep(0.03)


@app.get('/video_feed')
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.post('/postdata')
def post_data(request: Request, stream=Form()):
    producer.send('url_video', bytes(stream, 'utf-8'))
    return templates.TemplateResponse('page.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8080)
