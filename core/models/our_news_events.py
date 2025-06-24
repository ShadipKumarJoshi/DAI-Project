from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    
    def clean(self):
        # Ensure end is not earlier than start
        if self.publication_start and self.publication_end:
            if self.publication_end < self.publication_start:
                raise ValidationError("Publication end date cannot be earlier than start date.")
