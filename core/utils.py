# core/utils.py

from . import models, forms
from .admin_utils import get_list_display_for_model  # import the helper


DASHBOARD_MODEL_MAP = {
    'navbaritem': {
        'model': models.NavbarItem,
        'form': forms.NavbarItemForm,
        'title': 'Navbar Items',
    },
    'cms': {
        'model': models.CMSPage,
        'form': forms.CMSPageForm,
        'title': 'CMS Pages',
    },
    'herocarousel': {
        'model': models.HeroCarousel,
        'form': forms.HeroCarouselForm,
        'title': 'Hero Carousel',
    },
    'sme_section': {
        'model': models.SMEDevelopmentStepSection,
        'form': forms.SMEDevelopmentStepSectionForm,
        'title': 'SME Dev Sections',
    },
    'sme_step': {
        'model': models.SMEDevelopmentStep,
        'form': forms.SMEDevelopmentStepForm,
        'title': 'SME Dev Steps',
    },
    'servicetag': {
        'model': models.ServiceTag,
        'form': forms.ServiceTagForm,
        'title': 'Service Tags',
    },
    'servicecard': {
        'model': models.ServiceCard,
        'form': forms.ServiceCardForm,
        'title': 'Service Cards',
    },
    'guidelinecard': {
        'model': models.SMEGuidelineCard,
        'form': forms.SMEGuidelineCardForm,
        'title': 'Guideline Cards',
    },
    'newsstatus': {
        'model': models.NewsEventStatus,
        'form': forms.NewsEventStatusForm,
        'title': 'News Status',
    },
    'newstype': {
        'model': models.NewsEventType,
        'form': forms.NewsEventTypeForm,
        'title': 'News Types',
    },
    'news': {
        'model': models.NewsEvent,
        'form': forms.NewsEventForm,
        'title': 'News & Events',
    },
    'quicklink': {
        'model': models.FooterQuickLink,
        'form': forms.FooterQuickLinkForm,
        'title': 'Footer Links',
    },
    'contactinfo': {
        'model': models.FooterContactInfo,
        'form': forms.FooterContactInfoForm,
        'title': 'Footer Contact',
    },
    'social': {
        'model': models.FooterSocialMedia,
        'form': forms.FooterSocialMediaForm,
        'title': 'Social Media',
    },
    'notice': {
        'model': models.Notice,
        'form': forms.NoticeForm,
        'title': 'Notices',
    },
    'attachment': {
        'model': models.NoticeAttachment,
        'form': forms.NoticeAttachmentForm,
        'title': 'Notice Attachments',
    },
}

# Add dynamic 'list_display' attribute to each config
for key, config in DASHBOARD_MODEL_MAP.items():
    config['list_display'] = get_list_display_for_model(config['model'])
