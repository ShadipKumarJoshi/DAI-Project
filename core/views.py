from django.shortcuts import render
from . import models


def home(request):
    sliders = models.Slider.objects.filter(is_slide_active=True).order_by(
        'order')  # Fetch only active sliders
    sme_section = models.SMEDevelopmentStepSection.objects.filter(
        is_active=True).first()
    sme_steps = sme_section.steps.filter(
        is_active=True).order_by('order') if sme_section else []
    return render(request, 'core/home.html', {
        'sliders': sliders,
        'sme_section': sme_section,
        'sme_steps': sme_steps
    })
