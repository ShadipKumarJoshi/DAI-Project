from django.shortcuts import render, get_object_or_404
from core import models
from django.core.paginator import Paginator

def cms_list_view(request):
    pages_qs = models.CMSPage.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(pages_qs, 9)  # 9 items per page
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)

    return render(request, 'core/cms/cms_list.html', {
        'pages': pages,
    })

def cms_page_view(request, slug):
    page = get_object_or_404(models.CMSPage, slug=slug, published=True)
    latest_pages = models.CMSPage.objects.filter(published=True).exclude(pk=page.pk).order_by('-created_at')[:6]

    return render(request, 'core/cms/cms_page.html', {
        'page': page,
        'latest_pages': latest_pages,
    })