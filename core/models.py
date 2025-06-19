from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from django.db.models import Q
from . import constants 
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError

class NavbarItem(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    is_button = models.BooleanField(default=False)
    button_style = models.CharField(max_length=10, choices=constants.BUTTON_STYLE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # New link fields
    link_type = models.CharField(max_length=10, choices=constants.LINK_TYPE_CHOICES, blank=True, null=True)
    module_name = models.CharField(max_length=100, blank=True, null=True)
    cms_page = models.ForeignKey('CMSPage', null=True, blank=True, on_delete=models.SET_NULL)
    external_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title or "Unnamed Item"

    def clean(self):
        # Button rules
        if self.is_button:
            if self.parent is not None:
                raise ValidationError("Button items cannot have a parent.")
            if self.pk and self.children.exists():
                raise ValidationError("Button items cannot have children.")
        if self.parent and self.parent.is_button:
            raise ValidationError("Non-button items cannot have a button as parent.")

        # Validate based on link_type
        if self.link_type == 'module' and not self.module_name:
            raise ValidationError("Module name is required when link type is 'module'.")
        if self.link_type == 'cms' and not self.cms_page:
            raise ValidationError("CMS Page is required when link type is 'cms'.")
        if self.link_type == 'external' and not self.external_url:
            raise ValidationError("External URL is required when link type is 'external'.")

        # Ensure only one link is set
        links = [self.module_name, self.cms_page, self.external_url]
        if len([v for v in links if v]) > 1:
            raise ValidationError("Only one of module, CMS page, or external URL can be set.")

    def get_resolved_url(self):
        if self.link_type == 'module' and self.module_name:
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse(self.module_name)
            except NoReverseMatch:
                return '#'
        if self.link_type == 'cms' and self.cms_page:
            from django.urls import reverse
            try:
                return reverse('cms_page', kwargs={'slug': self.cms_page.slug})
            except Exception:
                return f"/{self.cms_page.slug}/"  # fallback
        if self.link_type == 'external' and self.external_url:
            return self.external_url
        return '#'
    @property
    def url(self):
        return self.get_resolved_url()

class HeroCarousel(models.Model):
    title = models.TextField()
    description = models.TextField()

    is_slide_active = models.BooleanField(default=True)  # Slide visibility

    # Button 1
    button1_text = models.CharField(max_length=50, blank=True, null=True)
    button1_class = models.CharField(
        max_length=10,
        choices=constants.BUTTON_STYLE_CHOICES,
        null=True, blank=True
    )
    button1_url = models.URLField(max_length=255, blank=True, null=True)

    # Button 2
    button2_text = models.CharField(max_length=50, blank=True, null=True)
    button2_class = models.CharField(
        max_length=10,
        choices=constants.BUTTON_STYLE_CHOICES,
        null=True, blank=True
    )
    button2_url = models.URLField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title[:50]

class SMEDevelopmentStepSection(models.Model):
    title = models.CharField(max_length=200, default="SME Development Steps")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Optional button
    is_button_active = models.BooleanField(default=False)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_class = models.CharField(
        max_length=10,
        choices=constants.BUTTON_STYLE_CHOICES,
        null=True, blank=True
    )
    button_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

class SMEDevelopmentStep(models.Model):
    section = models.ForeignKey(
        SMEDevelopmentStepSection, on_delete=models.CASCADE, related_name='steps')
    image = models.ImageField(upload_to='development_steps_images', null=True,
        blank=True,
        default='development_steps_images/default_img.png')
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# our_services_section.html    
class ServiceTag(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ServiceCard(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_path = models.CharField(max_length=255, blank=True, null=True)  # Static path or URL
    tags = models.ManyToManyField(ServiceTag, related_name='services', blank=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class SMEGuidelineCard(models.Model):
    icon = models.ImageField(upload_to='guidelines_icons', null=True,
        blank=True,
        default='guidelines_icons/default.svg')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    
# our_news_events_section.html
class NewsEventType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class NewsEventStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class NewsEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news_images', null=True,
        blank=True,
        default='news_images/default_news.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status_tag = models.ForeignKey(
        NewsEventStatus, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.ForeignKey(
        NewsEventType, on_delete=models.SET_NULL, null=True, blank=True)

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    publication_start = models.DateTimeField(null=True, blank=True)
    publication_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_published_now(self):
        now = timezone.now()
        if self.publication_start and now < self.publication_start:
            return False
        if self.publication_end and now > self.publication_end:
            return False
        return True

# Footer
class FooterQuickLink(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class FooterContactInfo(models.Model):
    icon = models.FileField(upload_to='footer_icons', blank=True, null=True)
    label = models.CharField(max_length=100)  # e.g. "Email", "Phone", "Location"
    value = models.CharField(max_length=255)  # e.g. email address, phone number, location text
    url = models.URLField(blank=True, null=True)  # optional clickable link (e.g. mailto: or tel:)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.value}"

class FooterSocialMedia(models.Model):
    platform_name = models.CharField(max_length=50)  # e.g. Twitter, Facebook
    icon = models.FileField(upload_to='social_icons')  # icon image
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.platform_name

# Notice
class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    pop_up = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class NoticeAttachment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='notice_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.notice.title}"

class CMSPage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="URL path, e.g., 'about-us'")
    image = models.ImageField(upload_to='cms_images/', null=True, blank=True) 
    content = RichTextUploadingField(help_text="HTML or Markdown content")
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional SEO fields
    seo_title = models.CharField(max_length=70, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title