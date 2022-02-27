from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
from io import BytesIO
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        link = request.form.get("url_video")
        
        try:
            video = YouTube(link)
            video.check_availability()
        except:
            return redirect(url_for("homepage"))
       
        buffer = BytesIO()
        video.streams.get_audio_only().stream_to_buffer(buffer)
        buffer.seek(0)
        musica = video.streams.get_audio_only()
        musica.download()

        return send_file(buffer, as_attachment=True, download_name=f"{video.title}.mp3")
    return render_template("homepage.html")

if __name__ == "__main__":
    app.run(debug=True)