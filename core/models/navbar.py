from django.db import models
from core import constants
from django.core.exceptions import ValidationError


class NavbarItem(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.PROTECT)
    order = models.PositiveIntegerField(default=0)
    is_button = models.BooleanField(default=False)
    button_style = models.CharField(
        max_length=10, choices=constants.BUTTON_STYLE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # New link fields
    link_type = models.CharField(
        max_length=10, choices=constants.LINK_TYPE_CHOICES, blank=True, null=True)
    module_name = models.CharField(max_length=100, blank=True, null=True)
    cms_page = models.ForeignKey(
        'CMSPage', null=True, blank=True, on_delete=models.CASCADE)
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
            raise ValidationError(
                "Non-button items cannot have a button as parent.")
        
         # Cyclic relationship prevention
        ancestor = self.parent
        while ancestor is not None:
            if ancestor == self:
                raise ValidationError("Cannot set a child as parent (cyclic relationship).")
            ancestor = ancestor.parent

        # Validate based on link_type
        if self.link_type == 'module' and not self.module_name:
            raise ValidationError(
                "Module name is required when link type is 'module'.")
        if self.link_type == 'cms' and not self.cms_page:
            raise ValidationError(
                "CMS Page is required when link type is 'cms'.")
        if self.link_type == 'external' and not self.external_url:
            raise ValidationError(
                "External URL is required when link type is 'external'.")

        # Ensure only one link is set
        links = [self.module_name, self.cms_page, self.external_url]
        if len([v for v in links if v]) > 1:
            raise ValidationError(
                "Only one of module, CMS page, or external URL can be set.")

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
