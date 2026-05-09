from .base import embedingCompare
import requests

class lmStudioCompare(embedingCompare):
    def __init__(self,url: str) -> None:
        self.url = url
        super().__init__()
    def getEmbedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Empty text")
        responce = requests.post(
            self.url,
            json={"input": text},
            timeout=30
        )
        data = responce.json()
        return data["data"][0]["embedding"]