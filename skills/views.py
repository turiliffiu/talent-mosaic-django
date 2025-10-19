from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Skill, UserSkill

@login_required
def my_skills(request):
    """List user's skills"""
    user_skills = request.user.skills.select_related('skill', 'skill__category').all()
    context = {
        'user_skills': user_skills,
    }
    return render(request, 'skills/my_skills.html', context)

@login_required
def skill_list(request):
    """List all available skills"""
    skills = Skill.objects.filter(is_active=True).select_related('category')
    context = {
        'skills': skills,
    }
    return render(request, 'skills/skill_list.html', context)
