from django.db import models


class NavbarItem(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=255, null=True,
                           blank=True)  # USE NAMED URL ONLY
    order = models.PositiveIntegerField(default=0)
    is_button = models.BooleanField(default=False)
    button_style = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White')],
        null=True, blank=True
    )
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Unnamed Item"


class Slider(models.Model):
    title = models.TextField()
    description = models.TextField()

    is_slide_visible = models.BooleanField(default=True) # Slide visibility

    # Button 1
    is_button1_visible = models.BooleanField(default=False)
    button1_text = models.CharField(max_length=50, blank=True, null=True)
    button1_class = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue')],
        null=True, blank=True
    )
    button1_url = models.CharField(max_length=255, blank=True, null=True, help_text="Enter the named URL (e.g., 'home', 'about', 'contact')")
    

    # Button 2
    is_button2_visible = models.BooleanField(default=False)
    button2_text = models.CharField(max_length=50, blank=True, null=True)
    button2_class = models.CharField(
        max_length=10,
        choices=[('black', 'Black'), ('white', 'White'), ('blue', 'Blue')],
        null=True, blank=True
    )
    button2_url = models.CharField(max_length=255, blank=True, null=True, help_text="Enter the named URL (e.g., 'home', 'about', 'contact')")
    

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title[:50]