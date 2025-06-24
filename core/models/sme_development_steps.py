from django.db import models
from core import constants



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
