from django.db import models
from django.core.validators import URLValidator


class NavbarItem(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_button = models.BooleanField(default=False)
    button_style = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White')],
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Unnamed Item"

# hero_carousel_section.html
class Slider(models.Model):
    title = models.TextField()
    description = models.TextField()

    is_slide_active = models.BooleanField(default=True)  # Slide visibility

    # Button 1
    is_button1_active = models.BooleanField(default=False)
    button1_text = models.CharField(max_length=50, blank=True, null=True)
    button1_class = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue')],
        null=True, blank=True
    )
    button1_url = models.URLField(max_length=255, blank=True, null=True)

    # Button 2
    is_button2_active = models.BooleanField(default=False)
    button2_text = models.CharField(max_length=50, blank=True, null=True)
    button2_class = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue')],
        null=True, blank=True
    )
    button2_url = models.URLField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title[:50]

# sme_development_steps_section.html
class SMEDevelopmentStepSection(models.Model):
    title = models.CharField(max_length=200, default="SME Development Steps")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # Optional button
    is_button_active = models.BooleanField(default=False)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_class = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue')],
        null=True, blank=True
    )
    button_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class SMEDevelopmentStep(models.Model):
    section = models.ForeignKey(
        SMEDevelopmentStepSection, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=150)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Optional Button
    is_button_active = models.BooleanField(default=False)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_class = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue')],
        null=True, blank=True
    )
    button_url = models.URLField(max_length=255, blank=True, null=True)

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
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

# sme_guidelines_section.html
class SMEGuidelineCard(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title