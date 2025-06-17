from django.shortcuts import render, get_object_or_404
from . import models
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.utils.text import Truncator

def home(request):
    hero_carousels = models.HeroCarousel.objects.filter(is_slide_active=True).order_by(
        'order')  # Fetch only active hero_carousels
    sme_section = models.SMEDevelopmentStepSection.objects.filter(
        is_active=True).first()
    sme_steps = sme_section.steps.filter(
        is_active=True).order_by('order') if sme_section else []
    service_cards = models.ServiceCard.objects.filter(
        is_active=True).prefetch_related('tags')    # Efficiently fetches many-to-many or reverse foreign key related objects in a single batch query, reducing database hits.
    guideline_cards = models.SMEGuidelineCard.objects.filter(
        is_active=True).order_by('order')
    now = timezone.now()
    # Filter news within publication window
    news_list = models.NewsEvent.objects.filter(
        is_active=True,
        publication_start__lte=now  # lte = Less Than or Equal To
    ).filter(
        # gte = Greater Than or Equal To
        Q(publication_end__gte=now) | Q(publication_end__isnull=True)
    ).order_by('-is_featured', '-created_at')  # Featured first, then latest

    # Show only top 2 in the left
    featured_news = list(news_list[:2])

    # Show rest (excluding the 2 already shown) on the right
    other_news = news_list.exclude(id__in=[n.id for n in featured_news])[
        :4]  # limit preview to 4 news on right
    
     # ✅ Get all pop-up notices
    popup_notices_qs = models.Notice.objects.filter(pop_up=True).order_by('-published_date')
    
    # ✅ Simplify and serialize notices for frontend
    pop_up_notices = []
    for notice in popup_notices_qs:
        pop_up_notices.append({
            'id': notice.id,
            'title': notice.title,
            'content': Truncator(strip_tags(notice.content)).chars(300),
            'image': notice.image.url if notice.image else None,
        })
        
    return render(request, 'core/home.html', {
        'hero_carousels': hero_carousels,
        'sme_section': sme_section,
        'sme_steps': sme_steps,
        'service_cards': service_cards,
        'guideline_cards': guideline_cards,
        'featured_news': featured_news,
        'other_news': other_news,
        'pop_up_notices': pop_up_notices,
    })


def notice(request):
    notice_list = models.Notice.objects.order_by('-published_date')
    paginator = Paginator(notice_list, 6)  # Show N notices per page
    page_number = request.GET.get('page')
    notices = paginator.get_page(page_number)
    return render(request, 'core/notice.html', {'notices': notices})

def notice_detail(request, pk):
    notice = get_object_or_404(models.Notice, pk=pk)
    attachments = notice.attachments.all()
    return render(request, 'core/notice_detail.html', {
        'notice': notice,
        'attachments': attachments,
    })

def dummy(request):
    return render(request, 'core/dummy.html',)