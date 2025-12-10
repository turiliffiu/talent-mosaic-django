# projects/views.py
"""
Views per Admin Dashboard con gestione progetti e AI matching
"""
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_required, supervisor_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q, Avg, Sum, F
from django.utils import timezone
from datetime import timedelta
import json

from .models import (
    Project, ProjectRequiredSkill, ProjectRole, TeamMember,
    AIMatchingRun, AdminAction, MatchingPreference
)
from .ai_matching import TalentMatcher
from events.models import Event
from challenges.models import Challenge, ChallengeParticipation
from skills.models import Skill, UserSkill
from django.contrib.auth.models import User


# ========== ADMIN DASHBOARD MAIN ==========

@admin_required
def admin_dashboard(request):
    """Dashboard principale amministrazione"""
    
    # Stats generali
    stats = {
        'total_users': User.objects.filter(is_active=True).count(),
        'total_projects': Project.objects.count(),
        'active_projects': Project.objects.filter(status='active').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(start_date__gte=timezone.now()).count(),
        'total_challenges': Challenge.objects.count(),
        'active_challenges': Challenge.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).count(),
    }
    
    # Ultimi progetti
    recent_projects = Project.objects.select_related('created_by', 'manager').order_by('-created_at')[:5]
    
    # Progetti che necessitano attenzione
    projects_needing_attention = Project.objects.filter(
        Q(status='open') | Q(status='matching')
    ).annotate(
        team_size=Count('team_members', filter=Q(team_members__status='accepted'))
    ).filter(
        team_size__lt=F('team_size_min')
    )[:5]
    
    # Ultimi eventi
    recent_events = Event.objects.order_by('-start_date')[:5]
    
    # Challenge più popolari
    popular_challenges = Challenge.objects.annotate(
        participants=Count('participations')
    ).order_by('-participants')[:5]
    
    # Attività recente admin
    recent_actions = AdminAction.objects.select_related('admin').order_by('-created_at')[:10]
    
    # Trend ultimi 30 giorni
    thirty_days_ago = timezone.now() - timedelta(days=30)
    trends = {
        'new_users': User.objects.filter(date_joined__gte=thirty_days_ago).count(),
        'new_projects': Project.objects.filter(created_at__gte=thirty_days_ago).count(),
        'new_events': Event.objects.filter(created_at__gte=thirty_days_ago).count(),
    }
    
    context = {
        'stats': stats,
        'recent_projects': recent_projects,
        'projects_needing_attention': projects_needing_attention,
        'recent_events': recent_events,
        'popular_challenges': popular_challenges,
        'recent_actions': recent_actions,
        'trends': trends,
    }
    
    return render(request, 'admin_dashboard/dashboard.html', context)


# ========== GESTIONE PROGETTI ==========

@admin_required
def project_list(request):
    """Lista progetti con filtri"""
    
    # Filtri
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search = request.GET.get('search', '')
    
    projects = Project.objects.select_related('created_by', 'manager').annotate(
        team_size=Count('team_members', filter=Q(team_members__status='accepted')),
        pending_invites=Count('team_members', filter=Q(team_members__status='invited'))
    )
    
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    if priority_filter:
        projects = projects.filter(priority=priority_filter)
    
    if search:
        projects = projects.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    projects = projects.order_by('-created_at')
    
    # Stats per filtri
    status_counts = Project.objects.values('status').annotate(count=Count('id'))
    priority_counts = Project.objects.values('priority').annotate(count=Count('id'))
    
    context = {
        'projects': projects,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search': search,
        'status_counts': {s['status']: s['count'] for s in status_counts},
        'priority_counts': {p['priority']: p['count'] for p in priority_counts},
        'status_choices': Project.STATUS_CHOICES,
        'priority_choices': Project.PRIORITY_CHOICES,
    }
    
    return render(request, 'admin_dashboard/project_list.html', context)


@admin_required
def project_detail(request, project_id):
    """Dettaglio progetto con team e matching"""
    
    project = get_object_or_404(
        Project.objects.prefetch_related(
            'required_skills__skill',
            'roles',
            'team_members__user__userskill_set__skill',
            'matching_runs'
        ),
        id=project_id
    )
    
    # Team attuale
    team_members = project.team_members.select_related('user', 'role').order_by('-match_score')
    
    # Ultimi matching runs
    matching_runs = project.matching_runs.order_by('-executed_at')[:5]
    
    # Candidati suggeriti dall'AI
    suggested_candidates = team_members.filter(status='suggested').order_by('-match_score')[:10]
    
    context = {
        'project': project,
        'team_members': team_members,
        'matching_runs': matching_runs,
        'suggested_candidates': suggested_candidates,
        'team_completion': (team_members.filter(status='accepted').count() / project.team_size_min * 100) if project.team_size_min > 0 else 0,
    }
    
    return render(request, 'admin_dashboard/project_detail.html', context)


@admin_required
def project_create(request):
    """Crea nuovo progetto"""
    
    if request.method == 'POST':
        # Crea progetto
        project = Project.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            status=request.POST.get('status', 'draft'),
            priority=request.POST.get('priority', 'medium'),
            created_by=request.user,
            manager=request.user,
            estimated_duration_weeks=request.POST.get('duration', 4),
            team_size_min=request.POST.get('team_min', 3),
            team_size_max=request.POST.get('team_max', 8),
        )
        
        # Log azione
        AdminAction.objects.create(
            admin=request.user,
            action_type='create',
            content_type='Project',
            object_id=project.id,
            object_repr=str(project),
            description=f"Creato progetto: {project.title}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, f'Progetto "{project.title}" creato con successo!')
        return redirect('admin_dashboard:project_detail', project_id=project.id)
    
    # GET - mostra form
    skills = Skill.objects.all().order_by('category__name', 'name')
    
    context = {
        'skills': skills,
        'status_choices': Project.STATUS_CHOICES,
        'priority_choices': Project.PRIORITY_CHOICES,
    }
    
    return render(request, 'admin_dashboard/project_form.html', context)


@admin_required
def project_edit(request, project_id):
    """Modifica progetto"""
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        # Salva vecchi valori per log
        old_values = {
            'title': project.title,
            'status': project.status,
            'priority': project.priority,
        }
        
        # Aggiorna
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.status = request.POST.get('status', project.status)
        project.priority = request.POST.get('priority', project.priority)
        project.estimated_duration_weeks = request.POST.get('duration', project.estimated_duration_weeks)
        project.team_size_min = request.POST.get('team_min', project.team_size_min)
        project.team_size_max = request.POST.get('team_max', project.team_size_max)
        project.save()
        
        # Log modifiche
        changes = {}
        for key, old_val in old_values.items():
            new_val = getattr(project, key)
            if old_val != new_val:
                changes[key] = {'old': old_val, 'new': new_val}
        
        AdminAction.objects.create(
            admin=request.user,
            action_type='update',
            content_type='Project',
            object_id=project.id,
            object_repr=str(project),
            description=f"Modificato progetto: {project.title}",
            changes=changes,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Progetto aggiornato!')
        return redirect('admin_dashboard:project_detail', project_id=project.id)
    
    # GET
    skills = Skill.objects.all().order_by('category__name', 'name')
    required_skills = project.required_skills.all()
    
    context = {
        'project': project,
        'skills': skills,
        'required_skills': required_skills,
        'status_choices': Project.STATUS_CHOICES,
        'priority_choices': Project.PRIORITY_CHOICES,
    }
    
    return render(request, 'admin_dashboard/project_form.html', context)


# ========== AI MATCHING ==========

@admin_required
def run_ai_matching(request, project_id):
    """Esegue algoritmo AI matching per un progetto"""
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        try:
            # Inizializza matcher
            matcher = TalentMatcher(project)
            
            # Esegui matching
            matching_run = matcher.run_matching(executed_by=request.user)
            
            # Log azione
            AdminAction.objects.create(
                admin=request.user,
                action_type='matching',
                content_type='Project',
                object_id=project.id,
                object_repr=str(project),
                description=f"Eseguito AI matching per progetto: {project.title}",
                changes={'candidates_found': matching_run.candidates_found},
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(
                request,
                f'✅ Matching completato! Trovati {matching_run.candidates_found} candidati in {matching_run.execution_time_seconds:.2f}s'
            )
            
            # Se AJAX, ritorna JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'candidates_found': matching_run.candidates_found,
                    'execution_time': matching_run.execution_time_seconds,
                    'redirect_url': f'/admin-dashboard/projects/{project_id}/'
                })
            
        except Exception as e:
            messages.error(request, f'❌ Errore nel matching: {str(e)}')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return redirect('admin_dashboard:project_detail', project_id=project_id)


@admin_required
def matching_results(request, project_id, run_id):
    """Visualizza risultati dettagliati di un matching run"""
    
    project = get_object_or_404(Project, id=project_id)
    matching_run = get_object_or_404(AIMatchingRun, id=run_id, project=project)
    
    # Parse candidati
    candidates = matching_run.candidates_data
    
    # Ordina per score
    candidates.sort(key=lambda x: x.get('score', 0), reverse=True)
    
    context = {
        'project': project,
        'matching_run': matching_run,
        'candidates': candidates,
    }
    
    return render(request, 'admin_dashboard/matching_results.html', context)


@admin_required
def invite_candidate(request, project_id, user_id):
    """Invita un candidato suggerito dall'AI a unirsi al progetto"""
    
    project = get_object_or_404(Project, id=project_id)
    user = get_object_or_404(User, id=user_id)
    
    # Trova o crea TeamMember
    team_member, created = TeamMember.objects.get_or_create(
        project=project,
        user=user,
        defaults={'status': 'invited'}
    )
    
    if not created:
        # Aggiorna status se era suggested
        if team_member.status == 'suggested':
            team_member.status = 'invited'
            team_member.save()
    
    # TODO: Invia notifica/email all'utente
    
    # Log azione
    AdminAction.objects.create(
        admin=request.user,
        action_type='update',
        content_type='TeamMember',
        object_id=team_member.id,
        object_repr=f"{user.get_full_name()} → {project.title}",
        description=f"Invitato {user.get_full_name()} al progetto {project.title}",
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    messages.success(request, f'✅ {user.get_full_name()} invitato al progetto!')
    
    return redirect('admin_dashboard:project_detail', project_id=project_id)


# ========== GESTIONE EVENTI ==========

@admin_required
def event_list_admin(request):
    """Lista eventi per admin"""
    
    # Filtri
    event_type = request.GET.get('type', '')
    status = request.GET.get('status', '')
    
    events = Event.objects.select_related('organizer').annotate(
        registrations_count=Count('registrations'),
        confirmed_count=Count('registrations', filter=Q(registrations__status='confirmed'))
    )
    
    # Applica filtri
    if event_type:
        events = events.filter(event_type=event_type)
    
    if status == 'upcoming':
        events = events.filter(start_date__gte=timezone.now())
    elif status == 'past':
        events = events.filter(start_date__lt=timezone.now())
    
    events = events.order_by('-start_date')
    
    # Stats
    stats = {
        'total': Event.objects.count(),
        'upcoming': Event.objects.filter(start_date__gte=timezone.now()).count(),
        'past': Event.objects.filter(start_date__lt=timezone.now()).count(),
    }
    
    context = {
        'events': events,
        'event_types': Event.EVENT_TYPES,
        'stats': stats,
        'type_filter': event_type,
        'status_filter': status,
    }
    
    return render(request, 'admin_dashboard/event_list.html', context)


# ========== GESTIONE CHALLENGE ==========

@admin_required
def challenge_list_admin(request):
    """Lista challenge per admin"""
    
    challenges = Challenge.objects.select_related('created_by').annotate(
        total_participants=Count('participations'),
        total_completed=Count('participations', filter=Q(participations__completed=True))
    ).order_by('-created_at')
    
    # Stats
    stats = {
        'total': Challenge.objects.count(),
        'active': Challenge.objects.filter(
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).count(),
        'upcoming': Challenge.objects.filter(start_date__gt=timezone.now()).count(),
        'total_participations': ChallengeParticipation.objects.count(),
    }
    
    context = {
        'challenges': challenges,
        'stats': stats,
    }
    
    return render(request, 'admin_dashboard/challenge_list.html', context)


# ========== ANALYTICS ==========

@admin_required
def analytics_dashboard(request):
    """Dashboard analytics avanzata"""
    
    # Periodo
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)
    
    # User growth
    user_growth = User.objects.filter(
        date_joined__gte=start_date
    ).extra(
        select={'day': 'date(date_joined)'}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    # Project creation trend
    project_trend = Project.objects.filter(
        created_at__gte=start_date
    ).extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(count=Count('id')).order_by('day')
    
    # Top skills
    top_skills = UserSkill.objects.values(
        'skill__name'
    ).annotate(
        users=Count('user', distinct=True),
        avg_proficiency=Avg('proficiency')
    ).order_by('-users')[:10]
    
    # Project status distribution
    project_status_dist = Project.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'days': days,
        'user_growth': list(user_growth),
        'project_trend': list(project_trend),
        'top_skills': top_skills,
        'project_status_dist': {item['status']: item['count'] for item in project_status_dist},
    }
    
    return render(request, 'admin_dashboard/analytics.html', context)


# ========== SETTINGS ==========

@admin_required
def matching_preferences(request):
    """Gestisci preferenze algoritmo matching"""
    
    pref = MatchingPreference.objects.filter(is_active=True).first()
    
    if not pref:
        pref = MatchingPreference.objects.create()
    
    if request.method == 'POST':
        # Aggiorna pesi
        pref.skill_match_weight = int(request.POST.get('skill_weight', 40))
        pref.experience_weight = int(request.POST.get('experience_weight', 25))
        pref.availability_weight = int(request.POST.get('availability_weight', 20))
        pref.past_performance_weight = int(request.POST.get('performance_weight', 15))
        pref.diversity_weight = int(request.POST.get('diversity_weight', 10))
        
        # Filtri
        pref.min_overall_score = float(request.POST.get('min_score', 60))
        pref.max_candidates_per_run = int(request.POST.get('max_candidates', 20))
        
        # Diversity
        pref.promote_diversity = request.POST.get('promote_diversity') == 'on'
        
        pref.save()
        
        # Log
        AdminAction.objects.create(
            admin=request.user,
            action_type='update',
            content_type='MatchingPreference',
            object_id=pref.id,
            object_repr='AI Matching Settings',
            description='Aggiornate preferenze matching AI',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, '✅ Preferenze matching aggiornate!')
        return redirect('admin_dashboard:matching_preferences')
    
    context = {
        'preferences': pref,
    }
    
    return render(request, 'admin_dashboard/matching_preferences.html', context)
