# core/middleware.py
"""
Middleware per redirect automatico superuser/staff
"""
from django.shortcuts import redirect
from django.urls import reverse


class AdminDashboardRedirectMiddleware:
    """
    Middleware che redirige automaticamente staff/superuser alla dashboard admin
    quando accedono alla dashboard normale
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Controlla solo se l'utente è autenticato
        if request.user.is_authenticated:
            # Se sta accedendo alla dashboard normale
            if request.path == '/dashboard/' or request.path == reverse('core:dashboard'):
                # E se è staff o superuser
                if request.user.is_staff or request.user.is_superuser:
                    # Redirect alla dashboard admin
                    return redirect('admin_dashboard:dashboard')
        
        response = self.get_response(request)
        return response
