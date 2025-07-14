# core/views/bdsp_profile.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelform_factory
from core.models import BDSPProfile

@login_required
def bdsp_profile_view(request):
    user = request.user
    try:
        profile = user.bdsp_profile
    except BDSPProfile.DoesNotExist:
        messages.error(request, "BDSP Profile not found. Please complete your profile.")
        return redirect('bdsp_profile_form')

    return render(request, "core/accounts/bdsp_profile_view.html", {
        "profile": profile,
    })

@login_required
def bdsp_profile_form(request):
    user = request.user
    try:
        profile = user.bdsp_profile
    except BDSPProfile.DoesNotExist:
        profile = None

    BDSPProfileForm = modelform_factory(
        BDSPProfile,
        fields=[
            'organization_name', 'organization_size', 'industry_sector',
            'legal_type', 'stage_of_development', 'ownership_type',
            'service_name', 'service_type', 'service_description', 'service_logo',
            'business_registration_certificate', 'tax_clearance_certificate',
        ]
    )

    if request.method == "POST":
        form = BDSPProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.save()
            messages.success(request, "BDSP Profile updated.")
            return redirect('bdsp_profile_view')
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = BDSPProfileForm(instance=profile)

    # Split form into steps
    fields = list(form.visible_fields())
    return render(request, "core/accounts/bdsp_profile_form.html", {
        "form_step1": fields[0:6],
        "form_step2": fields[6:10],
        "form_step3": fields[10:],
    })
