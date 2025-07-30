from flask import Flask, request, jsonify, send_from_directory
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
import os

app = Flask(__name__)

# Replace these with your Spotify developer credentials
SPOTIFY_CLIENT_ID = '276e935108e34e839fa1f2a4abba8e82'
SPOTIFY_CLIENT_SECRET = '76d809eaf4444c2190b55ef7814dd243'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@app.route('/api/download', methods=['GET'])
def download_song():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Spotify URL missing'}), 400

    try:
        track = sp.track(url)
        song = track['name']
        artist = track['artists'][0]['name']
        query = f"{song} {artist}"
        search_url = f"ytsearch1:{query}"

        os.makedirs("downloads", exist_ok=True)

        options = {
            'format': 'bestaudio/best',
            'outtmpl': f'downloads/{song}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([search_url])

        return jsonify({'status': 'success', 'file': f"/download/{song}.mp3"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def serve_file(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
