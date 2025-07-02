from flask import Flask, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(_name_)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "YouTube Downloader Backend is running."})

@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        ydl_opts = {
            'format': 'best',
            'outtmpl': filepath,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if _name_ == "_main_":
    app.run(debug=True)
