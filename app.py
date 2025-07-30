from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Spotify Downloader API is running!'

@app.route('/api/spotify', methods=['GET'])
def download_spotify():
    track_url = request.args.get('url')
    if not track_url:
        return jsonify({'error': 'Please provide a Spotify URL (e.g. /api/spotify?url=...)'}), 400

    try:
        scraper_url = f"https://spotidownloader.com/en?url={track_url}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(scraper_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        download_link = soup.find('a', {'class': 'button is-success is-fullwidth'})['href']
        
        return jsonify({'download_url': download_link})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch download link', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
