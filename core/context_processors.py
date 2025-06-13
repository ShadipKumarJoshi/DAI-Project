from . import models


def navbar_items(request):
    items = models.NavbarItem.objects.filter(is_active=True).order_by('order')
    return {'navbar_items': items}
