from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return '🔽 This will handle Spotify download logic.'

@app.route('/download', methods=['GET'])
def download():
    spotify_url = request.args.get('url')
    if not spotify_url:
        return jsonify({'error': 'Spotify URL not provided'}), 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
        session = requests.Session()
        session.headers.update(headers)

        # Step 1: Load site
        home = session.get("https://spotidownloader.com/en")
        soup = BeautifulSoup(home.text, "html.parser")

        # Step 2: Submit URL
        res = session.post(
            "https://spotidownloader.com/inc/track.php",
            data={"url": spotify_url},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        # Step 3: Parse response
        soup = BeautifulSoup(res.text, 'html.parser')
        download_link = soup.find("a", class_="download-button")

        if not download_link or not download_link.get("href"):
            return jsonify({"error": "Download link not found"}), 404

        return jsonify({"download": download_link["href"]})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
