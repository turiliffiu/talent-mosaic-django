from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Skill, UserSkill, SkillCategory

@login_required
def my_skills(request):
    """List user's skills"""
    user_skills = request.user.skills.select_related('skill', 'skill__category').all()
    
    # Statistiche
    stats = {
        'total': user_skills.count(),
        'expert': user_skills.filter(proficiency=5).count(),
        'advanced': user_skills.filter(proficiency=4).count(),
        'verified': user_skills.filter(verified=True).count(),
    }
    
    # Raggruppa per categoria
    skills_by_category = {}
    for us in user_skills:
        cat_name = us.skill.category.name if us.skill.category else 'Altro'
        if cat_name not in skills_by_category:
            skills_by_category[cat_name] = []
        skills_by_category[cat_name].append(us)
    
    context = {
        'user_skills': user_skills,
        'skills_by_category': skills_by_category,
        'stats': stats,
    }
    return render(request, 'skills/my_skills.html', context)

@login_required
def skill_list(request):
    """List all available skills to add"""
    # Get user's current skills
    user_skill_ids = request.user.skills.values_list('skill_id', flat=True)
    
    # Filtri
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    
    # Query base
    skills = Skill.objects.filter(is_active=True).exclude(id__in=user_skill_ids)
    
    # Applica filtri
    if search_query:
        skills = skills.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if category_id:
        skills = skills.filter(category_id=category_id)
    
    skills = skills.select_related('category').annotate(
        total_users=Count('user_skills')
    ).order_by('category__name', 'name')
    
    # Categorie per filtro
    categories = SkillCategory.objects.all().order_by('name')
    
    context = {
        'skills': skills,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
    }
    return render(request, 'skills/skill_list.html', context)

@login_required
def add_skill(request, skill_id):
    """Add a skill to user's profile"""
    skill = get_object_or_404(Skill, id=skill_id, is_active=True)
    
    # Check if already exists
    if UserSkill.objects.filter(user=request.user, skill=skill).exists():
        messages.warning(request, f'Hai già la competenza "{skill.name}"')
    else:
        # Get proficiency from POST or default to 1
        proficiency = int(request.POST.get('proficiency', 1))
        years = float(request.POST.get('years', 0))
        
        UserSkill.objects.create(
            user=request.user,
            skill=skill,
            proficiency=proficiency,
            years_experience=years
        )
        messages.success(request, f'Competenza "{skill.name}" aggiunta con successo!')
    
    return redirect('skills:skill_list')

@login_required
def remove_skill(request, user_skill_id):
    """Remove a skill from user's profile"""
    user_skill = get_object_or_404(UserSkill, id=user_skill_id, user=request.user)
    skill_name = user_skill.skill.name
    user_skill.delete()
    messages.success(request, f'Competenza "{skill_name}" rimossa')
    return redirect('skills:my_skills')

@login_required
def update_skill(request, user_skill_id):
    """Update skill proficiency"""
    user_skill = get_object_or_404(UserSkill, id=user_skill_id, user=request.user)
    
    if request.method == 'POST':
        proficiency = int(request.POST.get('proficiency', user_skill.proficiency))
        years = float(request.POST.get('years', user_skill.years_experience))
        notes = request.POST.get('notes', user_skill.notes)
        
        user_skill.proficiency = proficiency
        user_skill.years_experience = years
        user_skill.notes = notes
        user_skill.save()
        
        messages.success(request, f'Competenza "{user_skill.skill.name}" aggiornata!')
    
    return redirect('skills:my_skills')
