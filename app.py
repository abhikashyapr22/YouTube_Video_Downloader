from flask import Flask, render_template, url_for, request, redirect, send_file, flash, session
import json
from urllib.parse import urlparse
from pytube import YouTube, Stream
from io import BytesIO


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/downloads'
app.secret_key = "gfdjhglhlkjhg567809hghgc980787hhvj"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/info', methods=['POST', 'GET'])
def info():
    global data, audio_files
    if request.method == "POST":
        url = request.form['url']

        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
        o = urlparse(url)

        if not o.geturl():
            flash("Please enter the valid url !")
            return redirect(url_for('home'))

        try:
            audio_files = yt.streams.filter(only_audio=True)
            # a_qualities = [i.abr for i in audiofiles]
        except:
            flash("Audio files are not available")

        try:
            title = yt.title
            thumbnail = yt.thumbnail_url
            mp4files = yt.streams.filter(file_extension='mp4')
            v_qualities = [i.resolution for i in mp4files]
            data = dict(title=title, thumbnail=thumbnail, v_qualities=set(v_qualities), audio_files=audio_files, url=url)
            # data1 = json.dumps(data)
            # session['data1'] = data1
        except:
            flash("Something went wrong! Please try again")
            return redirect(url_for('home'))

        return render_template('result.html', info=data)

    else:
        # data1 = session['data1']
        # return render_template('result.html', info=json.load(data1))
        return redirect(url_for('home'))


@app.route('/download_video', methods=['POST', 'GET'])
def download_video():
    global title
    if request.method == "POST":
        quality = request.form['quality']
        url = request.form['url']

        buffer = BytesIO()
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)

        try:
            title = yt.title
            video = yt.streams.filter(subtype="mp4", resolution=quality).first()
            video.stream_to_buffer(buffer)
        except:
            flash("Something went wrong! Please try again, if error persist try with different quality")
            #return render_template('result.html', info=data)
            return redirect(url_for('home'))

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=title + '.mp4', mimetype='video/mp4')
    else:
        return redirect(url_for('home'))


@app.route('/download_audio', methods=['POST', 'GET'])
def download_audio():
    global title
    if request.method == "POST":
        url = request.form['url']
        itag = request.form['itag']

        buffer = BytesIO()
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)

        try:
            title = yt.title
            audio = yt.streams.get_by_itag(int(itag))
            audio.stream_to_buffer(buffer)
        except:
            flash("Something went wrong! Please try again")
            return redirect(url_for('home'))

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=title + '.mp3', mimetype='audio/mp3')
    else:
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
