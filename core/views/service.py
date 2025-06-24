from django.shortcuts import render, get_object_or_404
from core import models
def service_detail(request, pk):
    service = get_object_or_404(models.ServiceCard, pk=pk)
    return render(request, 'core/service/service_detail.html', {'service': service})
