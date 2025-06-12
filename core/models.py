from django.db import models

class Slider(models.Model):
    title = models.TextField()
    description = models.TextField()
    button1_text = models.CharField(max_length=50)
    button1_class = models.CharField(max_length=50, default='btn-black')
    button2_text = models.CharField(max_length=50, blank=True)
    button2_class = models.CharField(max_length=50, default='btn-white', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title[:50]
