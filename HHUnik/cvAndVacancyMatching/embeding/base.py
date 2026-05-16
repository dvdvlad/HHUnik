from abc import ABC, abstractmethod
import math

class embedingCompare(ABC):
    @abstractmethod
    def getEmbedding(self,text: str) -> list[float]:
        pass
    def cosineCompare(self,a:list[float], b:list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0

        return (dot / (norm_a * norm_b))*100