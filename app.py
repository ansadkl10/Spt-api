from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Spotify Downloader API is working!"

@app.route('/download', methods=['GET'])
def download():
    spotify_url = request.args.get('url')
    if not spotify_url:
        return jsonify({'error': 'Spotify URL is missing'}), 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        data = {'url': spotify_url}

        # Spotidownloader scrap
        res = requests.post('https://spotidownloader.com/download', headers=headers, data=data)
        soup = BeautifulSoup(res.text, 'html.parser')
        link = soup.find('a', {'class': 'download-button'})

        if not link:
            return jsonify({'error': 'Download link not found'}), 404

        return jsonify({
            'status': 'success',
            'spotify_url': spotify_url,
            'download_url': link['href']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
