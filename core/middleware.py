from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

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
