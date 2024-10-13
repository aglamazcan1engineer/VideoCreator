from .unsplash_client import UnsplashClient
from .pexels_client import PexelsClient
from .fma_client import FMAClient

class APIFactory:
    @staticmethod
    def get_client(api_name: str, api_key: str):
        if api_name.lower() == "unsplash":
            return UnsplashClient(api_key)
        elif api_name.lower() == "pexels":
            return PexelsClient(api_key)
        elif api_name.lower() == "fma":
            return FMAClient(api_key)
        else:
            raise ValueError(f"Unsupported API: {api_name}")