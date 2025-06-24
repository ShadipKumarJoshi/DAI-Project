from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)  # username=email due to custom backend
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
    return render(request, 'accounts/login.html',)

@login_required(login_url='login')
def logout_view(request):
    auth_logout(request)  
    return redirect('login')

def register(request):
    return render(request, 'accounts/register.html',)
