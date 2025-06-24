from django.db import models

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
   