from abc import ABC, abstractmethod

class BaseAPIClient(ABC):
    @abstractmethod
    async def search_images(self, query: str, per_page: int = 5):
        pass

    @abstractmethod
    async def search_videos(self, query: str, per_page: int = 5):
        pass