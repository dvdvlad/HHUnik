
from django.views.generic.base import TemplateView

class Main(TemplateView):
    template_name="base.html"
class hrAccountPage(TemplateView):
    template_name="main/hrPage.html"