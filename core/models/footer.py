from django.db import models

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
