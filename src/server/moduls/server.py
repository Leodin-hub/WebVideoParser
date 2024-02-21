import sys
sys.path.append('../server')
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from moduls.streamer import Streamer
from library.helpers.kafka_function import get_producer  # , delete_topic, init_topic


def run_server():
    app = FastAPI()
    router = InferringRouter()

    @cbv(router)
    class MainServer:
        def __init__(self):
            self.templates = Jinja2Templates(directory='templates')
            self.streamer = Streamer()
            self.producer = get_producer()

        @router.get('/')
        def home(self, request: Request):
            return self.templates.TemplateResponse('page.html', {'request': request})

        @router.get('/video_feed')
        async def video_feed(self):
            return StreamingResponse(self.streamer.get_img(), media_type='multipart/x-mixed-replace; boundary=frame')

        @router.post('/postdata')
        def post_data(self, request: Request, stream: str = Form()):
            if stream is None:
                stream = ''
            self.producer.send('url_video', value=bytes(stream, 'utf-8'), timestamp_ms=1000)
            return self.templates.TemplateResponse('page.html', {'request': request})

    app.include_router(router)
    return app
