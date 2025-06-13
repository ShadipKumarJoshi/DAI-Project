from django.shortcuts import render
from . import models
from django.utils import timezone
from django.db.models import Q



def home(request):
    sliders = models.Slider.objects.filter(is_slide_active=True).order_by(
        'order')  # Fetch only active sliders
    sme_section = models.SMEDevelopmentStepSection.objects.filter(
        is_active=True).first()
    sme_steps = sme_section.steps.filter(
        is_active=True).order_by('order') if sme_section else []
    service_cards = models.ServiceCard.objects.filter(
        is_active=True).prefetch_related('tags')
    guideline_cards = models.SMEGuidelineCard.objects.filter(
        is_active=True).order_by('order')
    now = timezone.now()
    # Filter news within publication window
    news_list = models.NewsEvent.objects.filter(
        is_active=True,
        publication_start__lte=now
    ).filter(
        Q(publication_end__gte=now) | Q(publication_end__isnull=True)
    ).order_by('-is_featured', '-created_at')  # Featured first, then latest

    # Show only top 2 in the left
    featured_news = list(news_list[:2])

    # Show rest (excluding the 2 already shown) on the right
    other_news = news_list.exclude(id__in=[n.id for n in featured_news])

    
    return render(request, 'core/home.html', {
        'sliders': sliders,
        'sme_section': sme_section,
        'sme_steps': sme_steps,
        'service_cards': service_cards,
        'guideline_cards': guideline_cards,
        'featured_news': featured_news,
        'other_news': other_news,
    })
