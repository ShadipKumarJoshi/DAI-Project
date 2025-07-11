# core/views/sme_profile_form_wizard.py
import os
from django.conf import settings
from formtools.wizard.views import SessionWizardView
from core.forms import SMEBusinessInfoWizardForm, SMEServicesOfferedWizardForm, SMEDocumentUploadWizardForm
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from core.models import SMEProfile

# Define the temporary file storage location for the wizard uploads
file_storage = FileSystemStorage(
    location=os.path.join(settings.MEDIA_ROOT, 'wizard_temp'))


FORMS = [
    ("step1", SMEBusinessInfoWizardForm),
    ("step2", SMEServicesOfferedWizardForm),
    ("step3", SMEDocumentUploadWizardForm),
]

TEMPLATES = {
    "step1": "core/accounts/sme_profile_form_wizard/step1_business_info.html",
    "step2": "core/accounts/sme_profile_form_wizard/step2_registration_details.html",
    "step3": "core/accounts/sme_profile_form_wizard/step3_certificates.html",
}


class SMERegistrationWizard(SessionWizardView):
    form_list = FORMS
    file_storage = file_storage

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
    
    def post(self, *args, **kwargs):
        """
        Allow users to go back without validating the current step's form.
        """
        # Check if user clicked the "Back" button
        if 'wizard_goto_step' in self.request.POST:
            goto_step = self.request.POST.get('wizard_goto_step')
            self.storage.current_step = goto_step
            return self.render_goto_step(goto_step)

        return super().post(*args, **kwargs)
    


    
    def done(self, form_list, **kwargs):
        business_info = form_list[0].cleaned_data
        services_info = form_list[1].cleaned_data
        documents_info = form_list[2].cleaned_data

        # Check if profile already exists
        if hasattr(self.request.user, 'sme_profile'):
            sme_profile = self.request.user.sme_profile
        else:
            sme_profile = SMEProfile(user=self.request.user)

        # Step 1 - Business Info
        sme_profile.business_name = business_info['business_name']
        sme_profile.business_size = business_info['business_size']
        sme_profile.industry_sector = business_info['industry_sector']
        sme_profile.business_legal_type = business_info['business_legal_type']
        sme_profile.business_stage = business_info['business_stage']
        sme_profile.ownership_type = business_info['ownership_type']

        # Step 2 - Service Info
        sme_profile.service_name = services_info['service_name']
        sme_profile.service_type = services_info['service_type']
        sme_profile.service_description = services_info['service_description']
        if services_info.get('service_logo'):
            sme_profile.service_logo = services_info['service_logo']

        # Step 3 - Documents (only replace if new file uploaded)
        if documents_info.get('registration_certificate'):
            sme_profile.registration_certificate = documents_info['registration_certificate']
        if documents_info.get('tax_clearance_certificate'):
            sme_profile.tax_clearance_certificate = documents_info['tax_clearance_certificate']

        sme_profile.save()

        return redirect('home')  

    def get_form_initial(self, step):
        """
        Pre-fill wizard forms with existing profile data if available.
        """
        if self.request.user.is_authenticated and hasattr(self.request.user, 'sme_profile'):
            profile = self.request.user.sme_profile

            if step == 'step1':
                return {
                    'business_name': profile.business_name,
                    'business_size': profile.business_size,
                    'industry_sector': profile.industry_sector,
                    'business_legal_type': profile.business_legal_type,
                    'business_stage': profile.business_stage,
                    'ownership_type': profile.ownership_type,
                }
            elif step == 'step2':
                return {
                    'service_name': profile.service_name,
                    'service_type': profile.service_type,
                    'service_description': profile.service_description,
                    #  file fields don't prefill
                }
            elif step == 'step3':
                return {}
        return {}
    
    def get_context_data(self, form, **kwargs):
        """
        Pass file URLs to template so uploaded files can be shown.
        """
        context = super().get_context_data(form=form, **kwargs)

        if self.request.user.is_authenticated and hasattr(self.request.user, 'sme_profile'):
            profile = self.request.user.sme_profile

            if self.steps.current == 'step3':
                context.update({
                    'existing_registration_certificate': profile.registration_certificate.url if profile.registration_certificate else None,
                    'existing_tax_clearance_certificate': profile.tax_clearance_certificate.url if profile.tax_clearance_certificate else None,
                })
            elif self.steps.current == 'step2':
                context.update({
                    'existing_service_logo': profile.service_logo.url if profile.service_logo else None,
            })

        return context
