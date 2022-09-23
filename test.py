from flask import Flask, render_template, url_for, request, redirect, send_file, flash
from pytube import YouTube
from io import BytesIO


url = 'https://www.youtube.com/watch?v=DVqFyinDgE4'

buffer = BytesIO()
yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)

title = yt.title
# audio = yt.streams.get_audio_only()
# audiofiles = yt.streams.filter(only_audio=True)
# audio = yt.streams.get_by_itag(139)
audio = yt.streams.get_audio_only()
audio.download(output_path='/static/downloads', filename=title.replace('/', '_')+'.mp3')
# audio.stream_to_buffer(buffer)
# buffer.seek(0)
# send_file(buffer, as_attachment=True, download_name=title + '.mp3', mimetype='audio/mp4')

# a_qualities = [i.abr for i in audiofiles]
# audio.stream_to_buffer(buffer)
print(audio)
# print(a_qualities)
print(title)
# print(audiofiles)

# buffer.seek(0)
# send_file(buffer, as_attachment=True, download_name=title + '.mp4', mimetype='video/mp4')

#
# if __name__ == "__main__":
#     app.run()