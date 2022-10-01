from flask import Flask, render_template, url_for, request, redirect, send_file, flash
from pytube import YouTube
from io import BytesIO

def download_video(url, quality):
    global title
    buffer = BytesIO()
    yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)

    try:
        title = yt.title
        # video = yt.streams.filter(subtype="mp4", resolution=quality).first()
        video = yt.streams.get_by_resolution(quality)
        video.download(filename='Video.mp4')
        print(video)
        # video.stream_to_buffer(buffer)
        return "Done"
    except Exception as e:
        return e


# yt.streams.filter(abr="160kbps", progressive=False).first().download(filename="audio.mp3")

url = 'https://www.youtube.com/watch?v=DVqFyinDgE4'
quality = '1080p'

print(download_video(url, quality))
