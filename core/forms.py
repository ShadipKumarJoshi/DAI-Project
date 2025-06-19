from django import forms
from django.core.exceptions import ValidationError
from django.urls import get_resolver, Resolver404, reverse
from . import models
from . import constants
from django.utils.text import slugify


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

        # Build dropdown choices for module_name based on named URLs
        choices = [('', 'Select Module (Named URL)')]

        # Get all named URL patterns from the default resolver
        url_patterns = get_resolver().reverse_dict.items()

        # Filter for named URLs which are strings and exclude admin URLs or undesired ones
        for name, data in url_patterns:
            if isinstance(name, str):
                # Optionally, exclude admin and other internal routes here
                if name.startswith('admin:'):
                    continue
                # Add choice tuple (value, display)
                choices.append((name, name))

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

