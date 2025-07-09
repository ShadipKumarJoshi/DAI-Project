from . import models
from django.db.models import Q


def navbar_items(request):
    items = models.NavbarItem.objects.filter(is_active=True, parent=None, is_button=False).order_by('order')
    return {'navbar_items': items}

def navbar_buttons(request):
    user = request.user
    if user.is_authenticated:
        buttons = models.NavbarItem.objects.filter(
            is_active=True,
            is_button=True,
        ).filter(
            Q(visible_to='all') | Q(visible_to='authenticated')
        ).order_by('order')
    else:
        buttons = models.NavbarItem.objects.filter(
            is_active=True,
            is_button=True,
        ).filter(
            Q(visible_to='all') | Q(visible_to='anonymous')
        ).order_by('order')
    return {'navbar_buttons': buttons}


def footer_data(request):
    quick_links = models.FooterQuickLink.objects.filter(is_active=True)
    contact_infos = models.FooterContactInfo.objects.filter(is_active=True)
    social_medias = models.FooterSocialMedia.objects.filter(is_active=True)
    return {
        'footer_quick_links': quick_links,
        'footer_contact_infos': contact_infos,
        'footer_social_medias': social_medias,
    }