from django.db import models

# Notice
class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    pop_up = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class NoticeAttachment(models.Model):
    notice = models.ForeignKey(Notice, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='notice_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.notice.title}"
