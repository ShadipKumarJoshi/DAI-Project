from django import forms
from django.core.exceptions import ValidationError
from django.urls import get_resolver, Resolver404, reverse
from . import models
from core import constants
from django.utils.text import slugify
import re  # for pattern matching


# Custom ModelChoiceField to display "title - slug" in the dropdown
class CMSPageModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.title} - {obj.slug}"

class NavbarItemForm(forms.ModelForm):
    class Meta:
        model = models.NavbarItem
        fields = '__all__'
    
    class Media:
        js = ('admin/js/vendor/jquery/jquery.js',  
            'js/navbar_item_admin.js',)
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style the dropdown
        self.fields['link_type'].widget.attrs.update({'class': 'vSelect'})

        # Use the custom ModelChoiceField for cms_page
        if 'cms_page' in self.fields:
            self.fields['cms_page'] = CMSPageModelChoiceField(
                queryset=models.CMSPage.objects.filter(published=True),
                required=False,
                empty_label="Select CMS Page"
            )
            
          # Helper to prettify URL names: replace _ and - with spaces, title case
        def prettify_name(name):
            return name.replace('_', ' ').replace('-', ' ').title()

        # CHANGE HERE: Logic to auto-exclude dynamic/internal/debug/detail URLs
        def is_allowed_named_url(name, data):
            # Exclude admin, dashboard, debug, ckeditor, and internal routes
            if (
                name.startswith('admin:') or
                name.startswith('ckeditor') or
                name.startswith('debug') or
                name.startswith('dashboard') or
                name.startswith('api') or
                'upload' in name or
                'browse' in name
            ):
                return False

            # Exclude common dynamic/detail/edit/delete/view slugs
            if re.search(r'(detail|edit|delete|update|view)$', name):
                return False

            # Exclude routes that have path converters like <int:pk>, <slug:...>
            for entry in data:
                if isinstance(entry, (list, tuple)):
                    pattern = entry[0]
                    if hasattr(pattern, 'pattern') and '<' in str(pattern.pattern):
                        return False

            return True

        # Manual overrides (optional)
        OVERRIDE_LABELS = {
            'cms_page': 'CMS Page',
            'dummy': 'Dummy Page',
        }


        # Build dropdown choices for module_name based on named URLs
        choices = [('', 'Select Module (Named URL)')]

        # Get all named URL patterns from the default resolver
        url_patterns = get_resolver().reverse_dict.items()

        # Filter for named URLs which are strings and exclude admin URLs or undesired ones
        for name, data in url_patterns:
            if isinstance(name, str) and is_allowed_named_url(name, data):  # CHANGE HERE
                label = OVERRIDE_LABELS.get(name, prettify_name(name))
                choices.append((name, label))

               

        # Replace the module_name field widget with ChoiceField with these choices
        self.fields['module_name'] = forms.ChoiceField(
            choices=choices,
            required=False,
            widget=forms.Select(attrs={'class': 'vSelect'})
        )

    def clean(self):
        cleaned_data = super().clean()

        is_button = cleaned_data.get('is_button')
        parent = cleaned_data.get('parent')
        link_type = cleaned_data.get('link_type')
        module_name = cleaned_data.get('module_name')
        cms_page = cleaned_data.get('cms_page')
        external_url = cleaned_data.get('external_url')

        # ---------- Button / Hierarchy Rules ----------
        if is_button and parent is not None:
            raise ValidationError("Button items cannot have a parent.")
        if is_button and self.instance.pk and self.instance.children.exists():
            raise ValidationError("Button items cannot have children.")
        if parent and parent.is_button:
            raise ValidationError("Non-button items cannot have a button as parent.")

        # ---------- Link Validation ----------
        if link_type == 'module':
            if not module_name:
                raise ValidationError("Module name must be provided when link type is 'module'.")
            cleaned_data['cms_page'] = None
            cleaned_data['external_url'] = ''
        elif link_type == 'cms':
            if not cms_page:
                raise ValidationError("CMS Page must be selected when link type is 'cms'.")
            cleaned_data['module_name'] = ''
            cleaned_data['external_url'] = ''
        elif link_type == 'external':
            if not external_url:
                raise ValidationError("External URL must be provided when link type is 'external'.")
            cleaned_data['module_name'] = ''
            cleaned_data['cms_page'] = None
        else:
            # If no link_type selected, clear all link fields
            cleaned_data['module_name'] = ''
            cleaned_data['cms_page'] = None
            cleaned_data['external_url'] = ''

        return cleaned_data
    
    

class CMSPageForm(forms.ModelForm):
    class Meta:
        model = models.CMSPage
        fields = '__all__'

    def clean_slug(self):
        # Slug from input or title
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')
        base_slug = slugify(slug or title)
        slug = base_slug
        counter = 1

        # Avoid conflict with existing slugs
        while models.CMSPage.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

class HeroCarouselForm(forms.ModelForm):
    class Meta:
        model = models.HeroCarousel
        fields = '__all__'

class SMEDevelopmentStepSectionForm(forms.ModelForm):
    class Meta:
        model = models.SMEDevelopmentStepSection
        fields = '__all__'

class SMEDevelopmentStepForm(forms.ModelForm):
    class Meta:
        model = models.SMEDevelopmentStep
        fields = '__all__'

class ServiceTagForm(forms.ModelForm):
    class Meta:
        model = models.ServiceTag
        fields = '__all__'

class ServiceCardForm(forms.ModelForm):
    class Meta:
        model = models.ServiceCard
        fields = '__all__'

class SMEGuidelineCardForm(forms.ModelForm):
    class Meta:
        model = models.SMEGuidelineCard
        fields = '__all__'

class NewsEventTypeForm(forms.ModelForm):
    class Meta:
        model = models.NewsEventType
        fields = '__all__'

class NewsEventStatusForm(forms.ModelForm):
    class Meta:
        model = models.NewsEventStatus
        fields = '__all__'

class NewsEventForm(forms.ModelForm):
    class Meta:
        model = models.NewsEvent
        fields = '__all__'

class FooterQuickLinkForm(forms.ModelForm):
    class Meta:
        model = models.FooterQuickLink
        fields = '__all__'

class FooterContactInfoForm(forms.ModelForm):
    class Meta:
        model = models.FooterContactInfo
        fields = '__all__'

class FooterSocialMediaForm(forms.ModelForm):
    class Meta:
        model = models.FooterSocialMedia
        fields = '__all__'

class NoticeForm(forms.ModelForm):
    class Meta:
        model = models.Notice
        fields = '__all__'

class NoticeAttachmentForm(forms.ModelForm):
    class Meta:
        model = models.NoticeAttachment
        fields = '__all__'