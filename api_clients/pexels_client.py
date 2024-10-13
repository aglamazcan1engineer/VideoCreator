import aiohttp
from .base_client import BaseAPIClient

class PexelsClient(BaseAPIClient):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"

    async def search_images(self, query: str, per_page: int = 5):
        if not self.api_key:
            print("Uyarı: Pexels API anahtarı bulunamadı.")
            return []

        url = f"{self.base_url}/search"
        params = {
            "query": query,
            "per_page": per_page
        }
        headers = {"Authorization": self.api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [item['src']['large'] for item in data.get('photos', [])]
                    else:
                        print(f"Hata: Pexels API'den {response.status} durum kodu alındı.")
                        return []
        except Exception as e:
            print(f"Hata: Pexels API isteği sırasında bir sorun oluştu: {e}")
            return []

    async def search_videos(self, query: str, per_page: int = 5):
        if not self.api_key:
            print("Uyarı: Pexels API anahtarı bulunamadı.")
            return []

        url = f"{self.base_url}/videos/search"
        params = {
            "query": query,
            "per_page": per_page
        }
        headers = {"Authorization": self.api_key}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [item['video_files'][0]['link'] for item in data.get('videos', [])]
                    else:
                        print(f"Hata: Pexels API'den {response.status} durum kodu alındı.")
                        return []
        except Exception as e:
            print(f"Hata: Pexels API video isteği sırasında bir sorun oluştu: {e}")
            return []