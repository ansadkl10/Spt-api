from flask import Flask, request, jsonify, send_from_directory
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import yt_dlp
import os

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="276e935108e34e839fa1f2a4abba8e82",
    client_secret="76d809eaf4444c2190b55ef7814dd243"
))

@app.route('/api/download', methods=['GET'])
def download_song():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Spotify URL missing'}), 400

    try:
        track = sp.track(url)
        name = track['name']
        artist = track['artists'][0]['name']
        query = f"{name} {artist}"

        result = VideosSearch(query, limit=1).result()
        yt_link = result['result'][0]['link']

        os.makedirs("downloads", exist_ok=True)

        options = {
            'format': 'bestaudio/best',
            'outtmpl': f'downloads/{name}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([yt_link])

        return jsonify({'status': 'success', 'file': f"/download/{name}.mp3"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def serve_file(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
