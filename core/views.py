from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def home(request):
    """Homepage"""
    return render(request, 'core/home.html')

def about(request):
    """About page"""
    return render(request, 'core/about.html')

@login_required
def dashboard(request):
    """User dashboard"""
    context = {
        'user': request.user,
        'skills_count': request.user.skills.count(),
        'badges_count': request.user.badges.count(),
    }
    return render(request, 'core/dashboard.html', context)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
