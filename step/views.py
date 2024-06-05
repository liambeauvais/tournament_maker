from django.shortcuts import render
from django.views.generic import TemplateView

from step.models import Step


# Create your views here.

class StepView(TemplateView):
    model = Step
    template_name = "step/step_view.html"
    context_object_name = "step"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    #def post(self, request, *args, **kwargs):

