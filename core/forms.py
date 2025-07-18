from django import forms
from django.core.exceptions import ValidationError
from django.urls import get_resolver, Resolver404, reverse
from . import models
from core import constants
from django.utils.text import slugify
import re  # for pattern matching
from ckeditor_uploader.widgets import CKEditorUploadingWidget



from django.contrib.auth import get_user_model

User = get_user_model()


class BaseRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password',
                  'full_name', 'mobile', 'pan_vat', 'business_name']


    def clean(self):
        cleaned_data = super().clean()
        
        full_name = cleaned_data.get('full_name')
        mobile = cleaned_data.get('mobile')
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        
        if full_name and not re.fullmatch(r'^([A-Za-z]+\.?)( [A-Za-z]+\.?)*$', full_name):
            self.add_error('full_name', "Full name must contain only words with alphabets.")

        if mobile and not re.fullmatch(r'9\d{9}', mobile):
            self.add_error('mobile', "Mobile number must start with 9 and be exactly 10 digits long.")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data



class SMERegistrationForm(BaseRegistrationForm):
    business_registration_number = forms.CharField()

    class Meta(BaseRegistrationForm.Meta):
        fields = BaseRegistrationForm.Meta.fields + \
            ['business_registration_number']


class BDSPRegistrationForm(BaseRegistrationForm):
    business_type = forms.ChoiceField(choices=[
        ('firm', 'Firm'),
        ('company', 'Company'),
        ('partnership', 'Partnership'),
        ('proprietorship', 'Proprietorship'),
        ('nonprofit', 'Non-profit'),
    ])

    class Meta(BaseRegistrationForm.Meta):
        fields = BaseRegistrationForm.Meta.fields + ['business_type']

# ------------------------------
# SME Profile Wizard Forms
# ------------------------------


class SMEBusinessInfoWizardForm(forms.Form):
   

    business_name = forms.CharField(
        label="Business Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'abc company'
        })
    )

    business_size = forms.ChoiceField(
        label="Business Size",
        choices=[('', 'Select your business type')] + constants.BUSINESS_SIZES
    )

    industry_sector = forms.ChoiceField(
        label="Industry Sector",
        choices=[('', 'Select your business legal type')] + constants.INDUSTRY_SECTORS
    )

    business_legal_type = forms.ChoiceField(
        label="Business Legal Type",
        choices=[('', 'Select your business legal type')] + constants.LEGAL_TYPES
    )

    business_stage = forms.ChoiceField(
        label="Business Stage",
        choices=[('', 'Select your business stage')] + constants.BUSINESS_STAGES
    )

    ownership_type = forms.ChoiceField(
        label="Ownership Type",
        choices=[('', 'Select your business ownership type')] + constants.OWNERSHIP_TYPES
    )


class SMEServicesOfferedWizardForm(forms.Form):


    service_name = forms.CharField(
        label="Service Name",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your service name'})
    )

    service_type = forms.ChoiceField(
        label="Service Type",
        choices=[('', 'Your service type')] + constants.SERVICE_TYPES
    )

    service_description = forms.CharField(
        label="Service Description",
        widget=forms.Textarea(attrs={
            'placeholder': 'write your service description',
            'rows': 4
        })
    )

    service_logo = forms.FileField(
        label="Upload Logo (optional)",
        required=False
    )

    ALLOWED_LOGO_CONTENT_TYPES = [
            'image/jpeg',
            'image/jpg',
            'image/gif',
            'image/svg+xml',
            'image/png',
    ]
    

    def clean(self):
        cleaned_data = super().clean()

        service_name = cleaned_data.get('service_name')
        service_logo = cleaned_data.get('service_logo')

        # Validate service_name: only letters and spaces
        if service_name and not re.fullmatch(r'[A-Za-z ]+', service_name):
            self.add_error('service_name', "Service name must contain only letters and spaces.")

        # Validate service_logo: must be an allowed image type
        if service_logo:
            content_type = service_logo.content_type
            if content_type not in self.ALLOWED_LOGO_CONTENT_TYPES:
                self.add_error('service_logo', "Only image files (jpeg, jpg, gif, svg, png) are allowed for the logo.")

        return cleaned_data
    
class SMEDocumentUploadWizardForm(forms.Form):
    registration_certificate = forms.FileField(
        label="Registration Certificate",
        required=True)
    tax_clearance_certificate = forms.FileField(
        label="Tax Clearance Certificate", required=False)
    
    ALLOWED_CONTENT_TYPES = [
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/jpg',

    ]
    def clean(self):
        cleaned_data = super().clean()

        registration_certificate = cleaned_data.get('registration_certificate')
        tax_clearance_certificate = cleaned_data.get('tax_clearance_certificate')

        allowed_types = self.ALLOWED_CONTENT_TYPES

        # Validate registration_certificate
        if registration_certificate:
            content_type = registration_certificate.content_type
            if content_type not in allowed_types:
                self.add_error('registration_certificate', "Only PDF and image files are allowed for Registration Certificate.")

        # Validate tax_clearance_certificate
        if tax_clearance_certificate:
            content_type = tax_clearance_certificate.content_type
            if content_type not in allowed_types:
                self.add_error('tax_clearance_certificate', "Only PDF and image files are allowed for Tax Clearance Certificate.")

        return cleaned_data


# ------------------------------
# BDSP Profile Wizard Forms
# ------------------------------



class BDSPProfileForm(forms.ModelForm):
    class Meta:
        model = models.BDSPProfile
        fields = [
            'organization_name',
            'organization_size',
            'industry_sector',
            'legal_type',
            'stage_of_development',
            'ownership_type',
            'service_name',
            'service_type',
            'service_description',
            'service_logo',
            'business_registration_certificate',
            'tax_clearance_certificate',
        ]

    ALLOWED_LOGO_CONTENT_TYPES = [
        'image/jpeg', 'image/jpg', 'image/gif', 'image/svg+xml', 'image/png',
    ]

    ALLOWED_CERT_CONTENT_TYPES = [
        'application/pdf', 'image/jpeg', 'image/png', 'image/jpg',
    ]

    def clean(self):
        cleaned_data = super().clean()

        service_name = cleaned_data.get('service_name')
        service_logo = cleaned_data.get('service_logo')
        business_registration_certificate = cleaned_data.get('business_registration_certificate')
        tax_clearance_certificate = cleaned_data.get('tax_clearance_certificate')

        # Validate service_name: only letters and spaces
        if service_name and not re.fullmatch(r'^[A-Za-z]+(?: [A-Za-z]+)*$', service_name.strip()):
            self.add_error('service_name', "Service name must contain only letters and spaces (no numbers or special characters).")

        #  Validate service_logo
        if service_logo:
            if service_logo.content_type not in self.ALLOWED_LOGO_CONTENT_TYPES:
                self.add_error('service_logo', "Only image files (jpeg, jpg, gif, svg, png) are allowed for the logo.")

        #  Validate business_registration_certificate
        if business_registration_certificate:
            if business_registration_certificate.content_type not in self.ALLOWED_CERT_CONTENT_TYPES:
                self.add_error('business_registration_certificate', "Only PDF and image files are allowed for Registration Certificate.")

        #  Validate tax_clearance_certificate
        if tax_clearance_certificate:
            if tax_clearance_certificate.content_type not in self.ALLOWED_CERT_CONTENT_TYPES:
                self.add_error('tax_clearance_certificate', "Only PDF and image files are allowed for Tax Clearance Certificate.")

        return cleaned_data



# ------------------------------
# CMS Forms
# ------------------------------

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
            if re.search(r'(detail|edit|delete|update)$', name):
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
            raise ValidationError(
                "Non-button items cannot have a button as parent.")

        # ---------- Link Validation ----------
        if link_type == 'module':
            if not module_name:
                raise ValidationError(
                    "Module name must be provided when link type is 'module'.")
            cleaned_data['cms_page'] = None
            cleaned_data['external_url'] = ''
        elif link_type == 'cms':
            if not cms_page:
                raise ValidationError(
                    "CMS Page must be selected when link type is 'cms'.")
            cleaned_data['module_name'] = ''
            cleaned_data['external_url'] = ''
        elif link_type == 'external':
            if not external_url:
                raise ValidationError(
                    "External URL must be provided when link type is 'external'.")
            cleaned_data['module_name'] = ''
            cleaned_data['cms_page'] = None
        else:
            # If no link_type selected, clear all link fields
            cleaned_data['module_name'] = ''
            cleaned_data['cms_page'] = None
            cleaned_data['external_url'] = ''

        return cleaned_data


class CMSPageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

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
    # content = forms.CharField(widget=CKEditorUploadingWidget())
    publication_start = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    publication_end = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

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
    published_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    popup_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    popup_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = models.Notice
        fields = '__all__'


class NoticeAttachmentForm(forms.ModelForm):
    class Meta:
        model = models.NoticeAttachment
        fields = '__all__'
