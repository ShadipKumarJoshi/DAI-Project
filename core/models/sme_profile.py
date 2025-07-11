from django.db import models
from django.conf import settings


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
    business_size = models.CharField(max_length=20)  # e.g., small, medium, large
    industry_sector = models.CharField(max_length=50)
    business_legal_type = models.CharField(max_length=50)
    business_stage = models.CharField(max_length=50)
    ownership_type = models.CharField(max_length=50)
    
    # Step 2 Form wizard
    service_name = models.CharField(max_length=100 )
    service_type = models.CharField(max_length=50 )  # e.g., consulting, development, marketing
    service_description = models.TextField(default="Not provided.")
    service_logo = models.ImageField(upload_to='service_logos/', null=True, blank=True)
    
    # Step 3 form wizard
    registration_certificate = models.FileField(upload_to='certificates/')
    tax_clearance_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


# class ServiceOffered(models.Model):
#     sme_profile = models.ForeignKey(SMEProfile, on_delete=models.CASCADE, related_name='services')
    
#     service_name = models.CharField(max_length=100)
#     service_type = models.CharField(max_length=50)  # e.g., consulting, development, marketing
#     service_description = models.TextField()
#     service_logo = models.ImageField(upload_to='service_logos/', null=True, blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.service_name} ({self.sme_profile.business_name})"
