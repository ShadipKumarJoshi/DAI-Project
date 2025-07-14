from django.db import models
from django.conf import settings
from core.constants import BUSINESS_SIZES, INDUSTRY_SECTORS, LEGAL_TYPES, BUSINESS_STAGES, OWNERSHIP_TYPES, SERVICE_TYPES

class BDSPProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bdsp_profile',
        null=True,
        blank=True
    )
    
    # Step 1 form wizard - Business info (example fields)
    organization_name = models.CharField(max_length=100)
    organization_size = models.CharField(max_length=20, choices=BUSINESS_SIZES)
    industry_sector = models.CharField(max_length=50, choices=INDUSTRY_SECTORS)
    legal_type = models.CharField(max_length=50, choices=LEGAL_TYPES)
    stage_of_development = models.CharField(max_length=50, choices=BUSINESS_STAGES)
    ownership_type = models.CharField(max_length=50, choices=OWNERSHIP_TYPES)
    
    # Step 2 form wizard - Services offered by BDSP
    service_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    service_description = models.TextField(default="Not provided.")
    service_logo = models.ImageField(upload_to='bdsp_service_logos/', null=True, blank=True)
    
    # Step 3 form wizard - Certificates & documents
    business_registration_certificate = models.FileField(upload_to='bdsp_certificates/')
    tax_clearance_certificate = models.FileField(upload_to='bdsp_certificates/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name
