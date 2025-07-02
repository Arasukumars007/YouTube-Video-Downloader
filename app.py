from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # <-- ADD THIS LINE
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)
CORS(app)  # <-- ADD THIS LINE

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
