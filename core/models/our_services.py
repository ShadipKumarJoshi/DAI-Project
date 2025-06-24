from django.db import models

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

