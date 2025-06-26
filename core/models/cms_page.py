from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

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