# File: server.py - VERSI KOYEB FINAL, ONLINE 24 JAM, FULL YOUTUBE
import os
import yt_dlp
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_audio_url(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "extract_flat": False,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("url"), info.get("duration", 0), info.get("title", ""), info.get("thumbnail", "")

@app.route("/")
def home():
    return jsonify({"status": "VIBRALYS ONLINE!", "message": "Server hidup, siap ngasih lagu FULL"})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/search")
def search():
    q = request.args.get("q", "")
    limit = int(request.args.get("limit", 15))
    if not q:
        return jsonify([])
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(f"ytsearch{limit}:{q} audio", download=False)
            entries = res.get("entries", [])
            songs = []
            for e in entries:
                vid = e.get("id", "")
                title = e.get("title", "Unknown")
                if " - " in title:
                    artist = title.split(" - ")[0]
                else:
                    artist = e.get("uploader", "Unknown")
                cover = ""
                if e.get("thumbnails"):
                    cover = e.get("thumbnails")[-1].get("url", "")
                if not cover:
                    cover = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                songs.append({
                    "id": vid,
                    "title": title,
                    "artist": artist,
                    "cover": cover,
                    "video_id": vid,
                    "source": "youtube-full",
                    "duration": "0:00",
                })
            return jsonify(songs)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([])

@app.route("/audio/<video_id>")
def audio(video_id):
    try:
        audio_url, dur, title, thumb = get_audio_url(video_id)
        return jsonify({"audio_url": audio_url, "duration": dur, "title": title, "thumbnail": thumb, "source": "youtube-full"})
    except Exception as e:
        print(f"Audio error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Server VIBRALYS jalan di port {port}")
    app.run(host="0.0.0.0", port=port)