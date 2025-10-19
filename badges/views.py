from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Badge

def badge_list(request):
    """List all badges"""
    badges = Badge.objects.filter(is_active=True).order_by('display_order')
    context = {
        'badges': badges,
    }
    return render(request, 'badges/badge_list.html', context)

@login_required
def my_badges(request):
    """List user's badges"""
    user_badges = request.user.badges.select_related('badge').order_by('-awarded_at')
    context = {
        'user_badges': user_badges,
    }
    return render(request, 'badges/my_badges.html', context)
