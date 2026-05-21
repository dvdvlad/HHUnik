from abc import ABC, abstractmethod
import math
from typing import List

class embedingCompare(ABC):
    @abstractmethod
    def getEmbedding(self, text: str, is_query: bool = False) -> list[float]:
        pass

    def get_human_percentage(self, all_scores: List[float]) -> List[int]:
        scores = [float(s) for s in all_scores if s is not None]
        
        if not scores:
            print("!!! КРИТИКА: scores пустой список в get_human_percentage !!!")
            return []
            
        min_score = min(scores)
        max_score = max(scores)
        
        print(f"DEBUG: scores={scores}, min={min_score}, max={max_score}") # Увидите в логах докера
        
        # Если разница между лучшим и худшим кандидатом микроскопическая или кандидат один
        if abs(max_score - min_score) < 1e-6:
            return [100] * len(scores)
            
        percentages = []
        for score in scores:
            # Формула нормализации
            normalized = (score - min_score) / (max_score - min_score)
            percentages.append(int(normalized * 100))
            
        return percentages    
    def cosineCompare(self, a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))

        if norm_a == 0 or norm_b == 0:
            return 0
        raw_score = dot / (norm_a * norm_b)
        return raw_score