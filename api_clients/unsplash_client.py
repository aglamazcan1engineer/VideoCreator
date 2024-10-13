import aiohttp
from .base_client import BaseAPIClient

class UnsplashClient(BaseAPIClient):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.unsplash.com"

    async def search_images(self, query: str, per_page: int = 5):
        if not self.api_key:
            print("Uyarı: Unsplash API anahtarı bulunamadı.")
            return []

        url = f"{self.base_url}/search/photos"
        params = {
            "query": query,
            "per_page": per_page
        }
        headers = {"Authorization": f"Client-ID {self.api_key}"}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [item['urls']['regular'] for item in data.get('results', [])]
                    else:
                        print(f"Hata: Unsplash API'den {response.status} durum kodu alındı.")
                        return []
        except Exception as e:
            print(f"Hata: Unsplash API isteği sırasında bir sorun oluştu: {e}")
            return []

    async def search_videos(self, query: str, per_page: int = 5):
        # Unsplash does not provide video search, return empty list
        return []