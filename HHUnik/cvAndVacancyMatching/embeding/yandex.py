from .base import embedingCompare
import httpx
import os

class YandexCompare(embedingCompare):
    def __init__(self) -> None:
        self.folder_id = os.environ.get('YANDEX_FOLDER_ID')
        self.api_key = os.environ.get('YANDEX_API_KEY')
        self.client = httpx.Client(timeout=30.0)
        super().__init__()

    def getEmbedding(self, text: str, is_query: bool = False) -> list[float]:
        model_type = "text-search-query" if is_query else "text-search-doc"
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/textEmbedding"

        headers = {
            # Для API-ключей заголовок выглядит как Api-Key, а не Bearer!
            "Authorization": f"Api-Key {self.api_key}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json",
        }
        data = {
            "modelUri": f"emb://{self.folder_id}/{model_type}/latest",
            "text": text,
        }

        response = self.client.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise RuntimeError(f"Ошибка Yandex API: {response.text}")
        return [float(x) for x in response.json()["embedding"]]

    def close(self) -> None:
        self.client.close()
