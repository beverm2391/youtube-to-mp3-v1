from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, VideoPrivate, RegexMatchError
from moviepy.editor import *
import os
import re
import random

app = FastAPI()

# ! HELPERS ========================================

def sanitize_filename(filename: str):
    return re.sub(r'[\\/*?:"<>|]', "", filename)


def check_url(url):
    try:
        yt = YouTube(url)
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="Video is unavailable")
    except VideoPrivate:
        raise HTTPException(status_code=403, detail="Video is private")
    except RegexMatchError:
        raise HTTPException(status_code=400, detail="Invalid URL")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ! ROUTES =========================================

@app.get("/")
async def read_root():
    return {"message": "Welcome to the YouTube to MP3 API. Use the /convert endpoint to get started."}

@app.get("/convert/")
async def convert(background_tasks: BackgroundTasks, url: str = Query(..., alias="url")):
    check_url(url)

    tempdir = "temp"
    if not os.path.exists(tempdir):
        os.mkdir(tempdir)

    try:
        # Download the video
        print("Downloading...")
        yt = YouTube(url)

        # Generate unique filenames to prevent clashes
        temp_filename = os.path.join(tempdir, "temp_video.mp4")
        if sanitize_filename(yt.title).strip() != "":
            mp3_filename = os.path.join(tempdir, f"{sanitize_filename(yt.title)}_{random.randint(0, 9999)}.mp3")
        else:
            mp3_filename = os.path.join(tempdir, f"unnamed_{random.randint(0, 9999)}.mp3")

        video = yt.streams.first()
        video.download(filename=temp_filename)

        # Convert to MP3
        print("Converting to MP3...")
        video_clip = VideoFileClip(temp_filename)
        video_clip.audio.write_audiofile(mp3_filename)

        # Clean Up
        print("Cleaning up...")
        os.remove(temp_filename)
        background_tasks.add_task(os.remove, mp3_filename) # have to use a background task to delete the file, otherwise it will be deleted before the response is sent

        return FileResponse(mp3_filename, headers={"Content-Disposition": f"attachment; filename={mp3_filename.split('/')[-1]}"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))