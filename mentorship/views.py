from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def mentorship_list(request):
    """List user's mentorships"""
    context = {}
    return render(request, 'mentorship/mentorship_list.html', context)
