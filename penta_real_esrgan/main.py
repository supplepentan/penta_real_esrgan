import os
import shutil
from io import BytesIO
import pathlib

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import ffmpeg
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from inference_realesrgan_penta import super_resolution

PATH_UPLOAD_FOLDER = "./input"
PATH_OUTPUT_FOLDER = "./output"
# Image
INPUT_IMAGE_FILENAME = "input.jpg"
OUTPUT_IMAGE_FILENAME = "output.jpg"
PATH_INPUT_IMAGE = os.path.join(PATH_UPLOAD_FOLDER, INPUT_IMAGE_FILENAME)
PATH_OUTPUT_IMAGE = os.path.join(PATH_OUTPUT_FOLDER, OUTPUT_IMAGE_FILENAME)
# Video
INPUT_VIDEO_FILENAME = "input.mp4"
OUTPUT_VIDEO_FILENAME = "output.mp4"
PATH_INPUT_VIDEO = os.path.join(PATH_UPLOAD_FOLDER, INPUT_VIDEO_FILENAME)
PATH_OUTPUT_VIDEO = os.path.join(PATH_OUTPUT_FOLDER, OUTPUT_VIDEO_FILENAME)


app = FastAPI(title="さぷりぺんたんのReal ESRGAN", description="超解像するよ", version="1.0")

import mimetypes

mimetypes.init()
mimetypes.add_type("application/javascript", ".js")

#: Configure CORS
origins = ["http://localhost:8080", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="./templates/static"), name="static")
templates = Jinja2Templates(directory="./templates/")


def initialize_dir():
    if os.path.exists(PATH_UPLOAD_FOLDER):
        shutil.rmtree(PATH_UPLOAD_FOLDER)
    os.makedirs(PATH_UPLOAD_FOLDER)
    if os.path.exists(PATH_OUTPUT_FOLDER):
        shutil.rmtree(PATH_OUTPUT_FOLDER)
    os.makedirs(PATH_OUTPUT_FOLDER)


@app.get("/")
def index(request: Request):
    initialize_dir()
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def index(file: UploadFile = File(...)):
    initialize_dir()
    contents = await file.read()
    input_image = Image.open(BytesIO(contents)).convert("RGB")
    input_image.save(PATH_INPUT_IMAGE)
    super_resolution()
    output_image = Image.open(
        os.path.join(PATH_OUTPUT_FOLDER, f"esrgan_{INPUT_IMAGE_FILENAME}")
    )
    output_image.save(PATH_OUTPUT_IMAGE)
    response = FileResponse(path=PATH_OUTPUT_IMAGE, filename=OUTPUT_IMAGE_FILENAME)
    return response


@app.post("/upload_video")
async def index(file: UploadFile = File(...)):
    initialize_dir()
    video_data = await file.read()
    upload_path = pathlib.Path(PATH_INPUT_VIDEO)
    with upload_path.open(mode="wb") as f:
        f.write(video_data)
    stream_video = ffmpeg.input(PATH_INPUT_VIDEO)
    stream_video = ffmpeg.output(
        stream_video, os.path.join(PATH_UPLOAD_FOLDER, "%05d.jpg"), r=23.98, f="image2"
    )  # r=23.98
    ffmpeg.run(stream_video)
    stream_audio = ffmpeg.input(PATH_INPUT_VIDEO)
    stream_audio = ffmpeg.output(
        stream_audio, os.path.join(PATH_OUTPUT_FOLDER, "output.wav")
    )
    ffmpeg.run(stream_audio)
    os.remove(PATH_INPUT_VIDEO)
    super_resolution()
    stream_concat = ffmpeg.input(os.path.join(PATH_OUTPUT_FOLDER, "esrgan_%05d.jpg"))
    stream_concat = ffmpeg.output(
        stream_concat, os.path.join(PATH_OUTPUT_FOLDER, "concat.mp4")
    )
    ffmpeg.run(stream_concat)
    output_video = ffmpeg.input(os.path.join(PATH_OUTPUT_FOLDER, "output.wav"))
    output_audio = ffmpeg.input(os.path.join(PATH_OUTPUT_FOLDER, "concat.mp4"))
    stream_output = ffmpeg.output(output_video, output_audio, PATH_OUTPUT_VIDEO)
    ffmpeg.run(stream_output)
    response = FileResponse(
        path=PATH_OUTPUT_VIDEO,
        filename=OUTPUT_VIDEO_FILENAME,
    )
    return response


if __name__ == "__main__":
    uvicorn.main(app=app)
