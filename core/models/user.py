from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('sme', 'SME'),
        ('bdsp', 'BDSP'),
    )

    # Role and business info
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    business_name = models.CharField(max_length=255)
    pan_vat = models.CharField(max_length=100, blank=True, null=True, unique=True)

    # User info
    full_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)

    # SME specific
    business_registration_number = models.CharField(max_length=100, blank=True, null=True, unique=True)

    # BDSP specific
    business_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
