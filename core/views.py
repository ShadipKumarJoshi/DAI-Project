from django.shortcuts import render
from . import models 

def home(request):
    sliders = models.Slider.objects.all()
    return render(request, 'core/home.html', {'sliders': sliders})