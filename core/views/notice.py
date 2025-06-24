from django.shortcuts import render, get_object_or_404
from core import models
from django.core.paginator import Paginator


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
