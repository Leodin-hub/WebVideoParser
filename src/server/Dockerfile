FROM python:3.12
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
WORKDIR .

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /server/

COPY . .

CMD ["python", "main.py"]

