from . import models
from django.db.models import Q

def navbar_items(request):
    user = request.user
    
    if user.is_authenticated:
        visibility_filter = Q(visible_to='all') | Q(visible_to='authenticated')
        role_filter = Q(required_role__isnull=True) | Q(required_role=user.role)
    else:
        visibility_filter = Q(visible_to='all') | Q(visible_to='anonymous')
        role_filter = Q(required_role__isnull=True)

    left_items = models.NavbarItem.objects.filter(
        is_active=True,
        parent=None,
        position='left'
    ).filter(visibility_filter& role_filter).order_by('order')

    right_items = models.NavbarItem.objects.filter(
        is_active=True,
        parent=None,
        position='right'
    ).filter(visibility_filter& role_filter).order_by('order')

    return {
        'navbar_items_left': left_items,
        'navbar_items_right': right_items,
    }

def navbar_buttons(request):
    user = request.user

    if user.is_authenticated:
        visibility_filter = Q(visible_to='all') | Q(visible_to='authenticated')
        role_filter = Q(required_role__isnull=True) | Q(required_role=user.role)
    else:
        visibility_filter = Q(visible_to='all') | Q(visible_to='anonymous')
        role_filter = Q(required_role__isnull=True)

    buttons = models.NavbarItem.objects.filter(
        is_active=True,
        is_button=True,
    ).filter(visibility_filter & role_filter).order_by('order')

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