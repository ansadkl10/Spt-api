import express from 'express';
import { getSpotifyDownloadLink } from './scraper.js';

const app = express();
const PORT = process.env.PORT || 10000;

app.get('/', (req, res) => {
  res.send('🔽 This will handle Spotify download logic.');
});

app.get('/download', async (req, res) => {
  const { url } = req.query;

  if (!url || !url.includes('spotify.com/track/')) {
    return res.status(400).json({ error: 'Invalid Spotify track URL' });
  }

  try {
    const link = await getSpotifyDownloadLink(url);
    if (!link) {
      return res.status(404).json({ error: 'Download link not found' });
    }
    res.json({ url: link });
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.listen(PORT, () => {
  console.log(`Spotify API running on port ${PORT}`);
});
