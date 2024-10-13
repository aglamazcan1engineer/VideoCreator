import aiohttp
from .base_client import BaseAPIClient

class FMAClient(BaseAPIClient):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://freemusicarchive.org/api"

    async def search_music(self, query: str, limit: int = 10):
        url = f"{self.base_url}/get/tracks.json"
        params = {
            "api_key": self.api_key,
            "query": query,
            "limit": limit
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [
                        {
                            'title': track['track_title'],
                            'artist': track['artist_name'],
                            'download_url': track['track_file_url'],
                            'genre': track['track_genre']
                        }
                        for track in data.get('dataset', [])
                    ]
                else:
                    print(f"Hata: FMA API'den {response.status} durum kodu alındı.")
                    return []

    async def search_images(self, query: str, per_page: int = 5):
        # Bu method BaseAPIClient'tan geliyor ama burada kullanılmıyor
        return []

    async def search_videos(self, query: str, per_page: int = 5):
        # Bu method BaseAPIClient'tan geliyor ama burada kullanılmıyor
        return []