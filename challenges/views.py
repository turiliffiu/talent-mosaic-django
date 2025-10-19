from django.shortcuts import render
from .models import Challenge

def challenge_list(request):
    """List active challenges"""
    challenges = Challenge.objects.filter(status='active').order_by('-start_date')
    context = {
        'challenges': challenges,
    }
    return render(request, 'challenges/challenge_list.html', context)
