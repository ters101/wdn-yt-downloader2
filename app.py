# app.py
import os
from flask import Flask, render_template, send_file, request
from pytube import YouTube
from werkzeug.utils import secure_filename  # Import the secure_filename function   

print(os.getcwd())

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download')
def download():
    try:
        url = request.args.get('url')
        format = request.args.get('format')
        resolution = request.args.get('resolution')

        if format == 'mp3':
            video = YouTube(url)
            stream = video.streams.filter(only_audio=True).first()
            file_extension = 'mp3'

        elif format == 'mp4':
            video = YouTube(url)
            if resolution:
                stream = video.streams.filter(res=resolution, file_extension='mp4').first()
            else:
                stream = video.streams.get_highest_resolution()
            file_extension = 'mp4'

        else:
            return "Invalid format"

        # Download video
        download_path = stream.download()

        # Get the title of the video and sanitize it for the filename
        video_title = secure_filename(video.title)

        # Set the file name with the video title and correct extension
        file_name = f'{video_title}.{file_extension}'

        # Send file to browser with the correct file name
        return send_file(download_path, as_attachment=True, download_name=file_name)

    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=False)

