# projects/decorators.py
"""
Decorators personalizzati per Admin Dashboard
"""
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator che richiede utente staff o con permessi admin
    Redirect a login se non autenticato, a dashboard normale se non autorizzato
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Devi effettuare il login per accedere all\'admin dashboard.')
            return redirect('accounts:login')
        
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Non hai i permessi per accedere all\'admin dashboard.')
            return redirect('core:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def supervisor_required(view_func):
    """
    Decorator che richiede utente staff/superuser
    Più restrittivo di admin_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Devi effettuare il login.')
            return redirect('accounts:login')
        
        if not request.user.is_staff:
            messages.error(request, 'Accesso riservato al personale amministrativo.')
            return redirect('core:dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
