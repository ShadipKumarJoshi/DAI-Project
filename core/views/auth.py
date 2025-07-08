from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import SMERegistrationForm, BDSPRegistrationForm
from django.contrib.auth import get_user_model

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


User = get_user_model()


def register_type(request):
    return render(request, 'core/accounts/register_type.html')


def sme_register(request):
    if request.method == 'POST':
        form = SMERegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User with this email already exists.')
            else:
                user = form.save(commit=False)
                user.username = email  # set username as email
                user.role = 'sme'
                user.set_password(form.cleaned_data['password'])
                user.save()
                # Authenticate to get backend set
                authenticated_user = authenticate(request, username=email, password=form.cleaned_data['password'])
                if authenticated_user is not None:
                    auth_login(request, authenticated_user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Authentication failed after registration.')
    else:
        form = SMERegistrationForm()
    return render(request, 'core/accounts/sme_register.html', {'form': form})


def bdsp_register(request):
    if request.method == 'POST':
        form = BDSPRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User with this email already exists.')
            else:
                user = form.save(commit=False)
                user.username = email
                user.role = 'bdsp'
                user.set_password(form.cleaned_data['password'])
                user.save()
                # Authenticate to get backend set
                authenticated_user = authenticate(request, username=email, password=form.cleaned_data['password'])
                if authenticated_user is not None:
                    auth_login(request, authenticated_user)
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Authentication failed after registration.')
    else:
        form = BDSPRegistrationForm()
    return render(request, 'core/accounts/bdsp_register.html', {'form': form})
