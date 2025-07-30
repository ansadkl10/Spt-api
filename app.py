from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Spotify Downloader API is live!'

@app.route('/download')
def download():
    return '🔽 This will handle Spotify download logic.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
