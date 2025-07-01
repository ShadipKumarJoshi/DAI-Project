from django.contrib import admin
from django.apps import apps
import core.admin  # import your admin module to register ModelAdmins

def get_list_display_for_model(model):
    """
    Given a model class, return the list_display tuple from its registered ModelAdmin.
    If not registered or list_display not set, default to ['__str__'].
    """
    try:
        model_admin = admin.site._registry.get(model)
        if model_admin and hasattr(model_admin, 'list_display'):
            # list_display can be a tuple/list or '__str__' fallback
            ld = model_admin.list_display
            # If list_display is just ('__str__',), replace with some default
            if ld == ('__str__',) or not ld:
                return ('__str__',)
            return ld
    except Exception:
        pass
    return ('__str__',)
