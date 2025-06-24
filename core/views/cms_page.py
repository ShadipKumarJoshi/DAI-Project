from django.shortcuts import render, get_object_or_404
from core import models



def cms_page_view(request, slug):
    page = get_object_or_404(models.CMSPage, slug=slug, published=True)
    return render(request, 'core/cms/cms_page.html', {'page': page})
