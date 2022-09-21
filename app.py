from flask import Flask, render_template, url_for, request, redirect, send_file, flash
from urllib.parse import urlparse
from pytube import YouTube
from io import BytesIO


app = Flask(__name__)
app.secret_key = "gfdjhglhlkjhg567809hghgc980787hhvj"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/info', methods=['POST', 'GET'])
def info():
    global data
    if request.method == "POST":
        url = request.form['url']
        o = urlparse(url)
        # ParseResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
        #             params='', query='', fragment='')

        if not o.geturl():
            flash("Please enter the valid url !")
            return redirect(url_for('home'))

        try:
            yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)
            title = yt.title
            thumbnail = yt.thumbnail_url
            mp4files = yt.streams.filter(file_extension='mp4')
            qualities = [i.resolution for i in mp4files]
            data = dict(title=title, thumbnail=thumbnail, qualities=qualities, url=url)
        except:
            flash("Something went wrong! Please try again")
            redirect(url_for('home'))

        return render_template('result.html', info=data)

    else:
        return redirect(url_for('home'))


@app.route('/download', methods=['POST', 'GET'])
def download():
    global title
    if request.method == "POST":
        quality = request.form['quality']
        url = request.form['url']

        buffer = BytesIO()
        yt = YouTube(url, use_oauth=False, allow_oauth_cache=True)

        try:
            title = yt.title
            video = yt.streams.get_by_resolution(quality)
            video.stream_to_buffer(buffer)
        except:
            flash("Something went wrong! Please try again")
            return redirect(url_for('home'))

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=title + '.mp4', mimetype='video/mp4')
    else:
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()
