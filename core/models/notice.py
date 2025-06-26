from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import os

# Notice
class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(help_text="HTML or Markdown content")
    published_date = models.DateField()
    image = models.FileField(upload_to='notices/', blank=True, null=True, help_text="Upload an image or PDF file")
    pop_up = models.BooleanField(default=False)
    
    popup_start_date = models.DateField(null=True, blank=True)
    popup_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        super().clean()
        
         # Validate image field to accept only images or PDFs
        if self.image:
            ext = os.path.splitext(self.image.name)[1].lower()
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
            if ext not in allowed_extensions:
                raise ValidationError({'image': 'Only image or PDF files are allowed.'})

        # Only validate date order if both are set
        if self.popup_start_date and self.popup_end_date:
            if self.popup_end_date < self.popup_start_date:
                raise ValidationError({
                    'popup_end_date': "Popup end date cannot be earlier than popup start date."
                })
        if self.pop_up:
            # popup_start_date is required
            if not self.popup_start_date:
                raise ValidationError({
                    'popup_start_date': "Popup start date must be set when pop_up is enabled."
                })
            # popup_end_date (if set) must not be earlier than start date
            if self.popup_start_date and self.popup_end_date:
                if self.popup_end_date < self.popup_start_date:
                    raise ValidationError({
                        'popup_end_date': "Popup end date cannot be earlier than popup start date."
                    })
    
    def save(self, *args, **kwargs):
        # Automatically disable popup if it's expired
        today = timezone.now().date()
        if self.pop_up and self.popup_start_date and self.popup_end_date:
            if self.popup_end_date < today:
                self.pop_up = False  # auto-uncheck
        super().save(*args, **kwargs)


class NoticeAttachment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='notice_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.notice.title}"
