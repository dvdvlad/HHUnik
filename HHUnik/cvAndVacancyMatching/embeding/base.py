from abc import ABC, abstractmethod
import math

class embedingCompare(ABC):
    @abstractmethod
    def getEmbedding(self, text: str, is_query: bool = False) -> list[float]:
        pass

    def get_human_percentage(self, cosine_score: float) -> int:
        # Задаем эмпирические пороги для Яндекса
        min_score = 0.26  # Все, что ниже или равно 0.35, станет 0%
        max_score = 0.38  # Все, что выше или равно 0.65, станет 100%
        
        if cosine_score <= min_score:
            return 0
        if cosine_score >= max_score:
            return 100
            
        # Считаем пропорцию внутри нашего рабочего диапазона
        normalized = (cosine_score - min_score) / (max_score - min_score)
        
        # Возвращаем округленный процент
        return int(normalized * 100)

    def cosineCompare(self, a: list[float], b: list[float]) -> int:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0

        # Теперь self передан корректно, и результатом будет красивое число от 0 до 100
        raw_score = dot / (norm_a * norm_b)
        return self.get_human_percentage(raw_score)