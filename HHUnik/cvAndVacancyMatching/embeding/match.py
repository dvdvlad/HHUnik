from .base import embedingCompare
class cvMatcher:
    def __init__(self,embeddingService: embedingCompare):
        self.embeding=embeddingService
    def match(self,vacancy,cvs):
        vEmb=self.embeding.getEmbedding(vacancy)
        results = []

        for cv in cvs:
            text = f"{cv.title}\n{cv.content}"