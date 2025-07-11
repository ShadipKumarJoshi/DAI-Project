from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import SMEProfile
from django.contrib import messages


@login_required
def sme_profile_view(request):
    try:
        profile = request.user.sme_profile
    except SMEProfile.DoesNotExist:
        # Redirect to the wizard if no profile exists
        messages.error(request, 'Please complete your profile before accessing this page.')
        return redirect('sme_profile_wizard')

    return render(request, 'core/accounts/sme_profile_view.html', {
        'profile': profile,
    })
