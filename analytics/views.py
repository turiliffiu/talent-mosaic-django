from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """Analytics dashboard"""
    context = {}
    return render(request, 'analytics/dashboard.html', context)
