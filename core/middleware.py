from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import logging
from datetime import datetime

class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # If the URL starts with /dashboard and user is not admin, redirect
        if path.startswith('/dashboard') or path.startswith('/admin'):
            if not request.user.is_authenticated or not request.user.is_staff:
                messages.error(request, "Access denied. Admins only.")
                return redirect(reverse('home'))

        return self.get_response(request)
    
from django.shortcuts import redirect
from django.urls import reverse

class RedirectAuthenticatedMiddleware:
    """
    Redirect authenticated users away from login and registration pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = [
            reverse('login'),
            reverse('register'),
            reverse('register_type'),
            reverse('sme_register'),
            reverse('bdsp_register'),
        ]

    def __call__(self, request):
        # If user is authenticated and trying to access any login/register page
        if request.user.is_authenticated and request.path in self.protected_paths:
            messages.info(request, "You are already logged in.")
            return redirect('home')

        response = self.get_response(request)
        return response



logger = logging.getLogger(__name__)  # Uses Django's logging config

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get request data
        method = request.method
        path = request.get_full_path()
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        ip = self.get_client_ip(request)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Process the response
        response = self.get_response(request)

        status = response.status_code

        # Log the data
        logger.info(f"[{timestamp}] {ip} - {user} - {method} {path} -> {status}")

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

