from flask import Flask, request, send_file, Response
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <title>YouTube Downloader</title>
</head>
<body>
    <h2>YouTube Video Downloader</h2>
    <input type='text' id='url' placeholder='Paste YouTube URL' />
    <button onclick='download()'>Download</button>

    <script>
    async function download() {
        const url = document.getElementById("url").value;
        if (!url) {
            alert("Please enter a URL!");
            return;
        }

        const response = await fetch("/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            const error = await response.text();
            alert("Error: " + error);
            return;
        }

        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = "video.mp4";
        a.click();
    }
    </script>
</body>
</html>
"""

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.get_json()
        print("📦 Received JSON:", data)

        if not data or 'url' not in data:
            return Response("Invalid or missing URL", status=400)

        url = data['url']
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = "video.mp4"
        stream.download(filename=filename)
        return send_file(filename, as_attachment=True)

    except Exception as e:
        return Response(str(e), status=400)

if __name__ == '__main__':
    app.run(debug=True)
