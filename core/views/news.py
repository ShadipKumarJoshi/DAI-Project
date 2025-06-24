from django.shortcuts import render, get_object_or_404
from core import models
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator


def news(request):
    now = timezone.now()
    news_list_qs = models.NewsEvent.objects.filter(
        is_active=True,
        publication_start__lte=now
    ).filter(
        Q(publication_end__gte=now) | Q(publication_end__isnull=True)
    ).order_by('-is_featured', '-created_at')

    paginator = Paginator(news_list_qs, 9)  # 9 per page
    page_number = request.GET.get('page')
    news_list = paginator.get_page(page_number)

    return render(request, 'core/news/news.html', {'news_list': news_list})


def news_detail(request, pk):
    news = get_object_or_404(models.NewsEvent, pk=pk, is_active=True)
    return render(request, 'core/news/news_detail.html', {'news': news})
