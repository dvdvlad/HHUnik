from .base import AembedingCompare
import httpx


class YandexCompare(AembedingCompare):
    def __init__(self, folder_id: str, iam_token: str) -> None:
        self.folder_id = folder_id
        self.iam_token = iam_token
        self.client = httpx.AsyncClient(timeout=30.0)
        super().__init__()
    async def getEmbedding(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Empty text")
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/textEmbedding"
        headers = {
            "Authorization": f"Bearer {self.iam_token}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json",
        }
        data = {
            "modelUri": f"emb://{self.folder_id}/text-search-doc/latest",
            "text": text,
        }
        response = await self.client.post(
            url, headers=headers, json=data
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Ошибка API ({response.status_code}): {response.text}"
            )
        result_data = response.json()
        return [float(x) for x in result_data["embedding"]]
    async def close(self) -> None:
        await self.client.aclose()
