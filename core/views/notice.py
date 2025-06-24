from django.shortcuts import render, get_object_or_404
from core import models
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q

def notice(request):
    notice_list = models.Notice.objects.order_by('-published_date')
    paginator = Paginator(notice_list, 6)  # Show N notices per page
    page_number = request.GET.get('page')
    notices = paginator.get_page(page_number)
    return render(request, 'core/notice/notice.html', {'notices': notices})


def notice_detail(request, pk):
    notice = get_object_or_404(models.Notice, pk=pk)
    attachments = notice.attachments.all()
    return render(request, 'core/notice/notice_detail.html', {
        'notice': notice,
        'attachments': attachments,
    })

def popup_notices(request):
    today = timezone.now().date()
    popup_notices_qs = models.Notice.objects.filter(
        pop_up=True,
        popup_start_date__lte=today
    ).filter(
        Q(popup_end_date__gte=today) | Q(popup_end_date__isnull=True)
    ).order_by('-published_date')

    return render(request, 'core/notice/popup_notices.html', {
        'popup_notices': popup_notices_qs
    })
