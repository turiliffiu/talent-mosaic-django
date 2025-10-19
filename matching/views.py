from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def matches(request):
    """List matching users"""
    context = {
        'matches': [],
    }
    return render(request, 'matching/matches.html', context)
