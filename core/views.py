from django.shortcuts import render
from . import models 

def home(request):
    sliders = models.Slider.objects.filter(is_slide_visible=True).order_by('order') # Fetch only visible sliders
    return render(request, 'core/home.html', {'sliders': sliders})