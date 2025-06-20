# core/utils.py 
from . import models, forms

DASHBOARD_MODEL_MAP = {
    'cms': {
        'model': models.CMSPage,
        'form': forms.CMSPageForm,
        'title': 'CMS Pages',
    },
    'navbaritem': {
        'model': models.NavbarItem,
        'form': forms.NavbarItemForm,
        'title': 'Navbar Items',
    },
    # Add more as needed
}
