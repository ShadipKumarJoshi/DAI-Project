from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('sme', 'SME'),
        ('bdsp', 'BDSP'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Shared fields for SME and BDSP
    business_name = models.CharField(max_length=255)
    pan_vat = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255)  # Person managing the business
    mobile = models.CharField(max_length=20)

    # SME-only field
    registration_number = models.CharField(max_length=100, blank=True, null=True)

    # BDSP-only field
    business_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
