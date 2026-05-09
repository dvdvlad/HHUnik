from cvAndVacancyMatching.embeding.dto import cvData, vacancyData
from .models import CV,Vacancy

def cvToDto(cv:CV)->cvData:
    return cvData(
        title=cv.title, # type: ignore
        content=cv.content # type: ignore
    )


def vacancyToDto(vc:Vacancy)->cvData:
    return cvData(
        title=vc.title, # type: ignore
        content=vc.content # type: ignore
    )