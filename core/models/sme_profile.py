from django.db import models
from django.conf import settings
from core.constants import BUSINESS_SIZES, INDUSTRY_SECTORS, LEGAL_TYPES, BUSINESS_STAGES, OWNERSHIP_TYPES, SERVICE_TYPES


class SMEProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sme_profile',
        null=True,
        blank=True
    )
    
    # Step 1 form wizard
    business_name = models.CharField(max_length=100)
    business_size = models.CharField(max_length=20, choices=BUSINESS_SIZES)  # e.g., small, medium, large
    industry_sector = models.CharField(max_length=50, choices=INDUSTRY_SECTORS)
    business_legal_type = models.CharField(max_length=50, choices=LEGAL_TYPES)
    business_stage = models.CharField(max_length=50, choices=BUSINESS_STAGES)
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_TYPES)
    
    # Step 2 Form wizard
    service_name = models.CharField(max_length=100 )
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES )  # e.g., consulting, development, marketing
    service_description = models.TextField(default="Not provided.")
    service_logo = models.ImageField(upload_to='service_logos/', null=True, blank=True)
    
    # Step 3 form wizard
    registration_certificate = models.FileField(upload_to='certificates/')
    tax_clearance_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


