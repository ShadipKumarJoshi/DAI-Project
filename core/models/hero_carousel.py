from django.db import models
from core import constants



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
