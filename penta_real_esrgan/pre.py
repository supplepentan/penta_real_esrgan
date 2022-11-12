import ffmpeg
import os

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

stream_output = ffmpeg.input(os.path.join(PATH_OUTPUT_FOLDER, "output_%05d.jpg"))
stream_output = ffmpeg.output(
    stream_output, os.path.join(PATH_OUTPUT_FOLDER, "output.mp4")
)
ffmpeg.run(stream_output)
