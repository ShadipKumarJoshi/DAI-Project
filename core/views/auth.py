from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from core.forms import SMERegistrationForm, BDSPRegistrationForm
from core.models import Profile

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # username=email due to custom backend
        user = authenticate(request, username=email, password=password)
        if user:
            auth_login(request, user)
            if user.is_staff or user.is_superuser:
                # Admin users go to dashboard
                return redirect('dashboard')
            else:
                # Other users go to home
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'core/accounts/login.html',)


@login_required(login_url='login')
def logout_view(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    return render(request, 'core/accounts/register.html',)


def register_type(request):
    return render(request, 'core/accounts/register_type.html')


def sme_register(request):
    if request.method == 'POST':
        form = SMERegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(username=email).exists():
                messages.error(request, 'User with this email already exists.')
            else:
                user = User.objects.create_user(username=email, email=email)
                user.set_password(password)
                user.save()

                # Create profile
                Profile.objects.create(
                    user=user,
                    role='sme',
                    business_name=form.cleaned_data['business_name'],
                    pan_vat=form.cleaned_data['pan_vat'],
                    full_name=form.cleaned_data['full_name'],
                    mobile=form.cleaned_data['mobile'],
                    registration_number=form.cleaned_data['registration_number'],
                )
                
                user.backend = 'core.backends.EmailBackend'
                auth_login(request, user)
                return redirect('dashboard')  # or wherever you want

    else:
        form = SMERegistrationForm()

    return render(request, 'core/accounts/sme_register.html', {'form': form})


def bdsp_register(request):
    if request.method == 'POST':
        form = BDSPRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(username=email).exists():
                messages.error(request, 'User with this email already exists.')
            else:
                user = User.objects.create_user(username=email, email=email)
                user.set_password(password)
                user.save()

                Profile.objects.create(
                    user=user,
                    role='bdsp',
                    business_name=form.cleaned_data['business_name'],
                    pan_vat=form.cleaned_data['pan_vat'],
                    full_name=form.cleaned_data['full_name'],
                    mobile=form.cleaned_data['mobile'],
                    business_type=form.cleaned_data['business_type'],
                )
                
                user.backend = 'core.backends.EmailBackend'
                auth_login(request, user)
                return redirect('dashboard')  # or wherever you want

    else:
        form = BDSPRegistrationForm()

    return render(request, 'core/accounts/bdsp_register.html', {'form': form})