from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q, Avg
from datetime import timedelta

from skills.models import Skill, UserSkill, SkillCategory
from events.models import Event, EventRegistration
from mentorship.models import Mentorship, MentorshipSession
from challenges.models import Challenge, ChallengeParticipation
from badges.models import Badge, UserBadge

def home(request):
    """Homepage"""
    return render(request, 'core/home.html')

def about(request):
    """About page"""
    return render(request, 'core/about.html')

@login_required
def dashboard(request):
    """User dashboard - Vista completa e interattiva"""
    user = request.user
    now = timezone.now()
    
    # === STATISTICHE UTENTE ===
    user_stats = {
        'skills_count': user.skills.count(),
        'badges_count': user.badges.count(),
        'events_registered': EventRegistration.objects.filter(user=user).count(),
        'events_attended': EventRegistration.objects.filter(user=user, status='attended').count(),
        'challenges_joined': ChallengeParticipation.objects.filter(user=user).count(),
        'challenges_completed': ChallengeParticipation.objects.filter(user=user, completed=True).count(),
    }
    
    # Mentorship stats
    user_stats['mentorships_as_mentor'] = Mentorship.objects.filter(mentor=user).count()
    user_stats['mentorships_as_mentee'] = Mentorship.objects.filter(mentee=user).count()
    user_stats['total_mentorships'] = user_stats['mentorships_as_mentor'] + user_stats['mentorships_as_mentee']
    
    # Badge points totali
    user_badge_points = UserBadge.objects.filter(user=user).select_related('badge')
    user_stats['total_badge_points'] = sum([ub.badge.points for ub in user_badge_points])
    
    # Challenge points totali
    user_challenge_points = ChallengeParticipation.objects.filter(user=user)
    user_stats['total_challenge_points'] = sum([cp.points_earned for cp in user_challenge_points])
    
    user_stats['total_points'] = user_stats['total_badge_points'] + user_stats['total_challenge_points']
    
    # === LE MIE COMPETENZE ===
    my_skills = UserSkill.objects.filter(user=user).select_related('skill', 'skill__category').order_by('-proficiency', 'skill__name')[:8]
    
    # Competenze per categoria
    skills_by_category = {}
    for us in UserSkill.objects.filter(user=user).select_related('skill__category'):
        cat_name = us.skill.category.name if us.skill.category else 'Altro'
        if cat_name not in skills_by_category:
            skills_by_category[cat_name] = []
        skills_by_category[cat_name].append(us)
    
    # === I MIEI EVENTI ===
    # Eventi a cui sono iscritto (futuri)
    my_upcoming_events = EventRegistration.objects.filter(
        user=user,
        event__start_date__gte=now,
        status='registered'
    ).select_related('event', 'event__organizer').order_by('event__start_date')[:5]
    
    # Eventi passati recenti
    my_past_events = EventRegistration.objects.filter(
        user=user,
        event__end_date__lt=now
    ).select_related('event').order_by('-event__end_date')[:3]
    
    # === EVENTI DISPONIBILI ===
    # Eventi futuri a cui NON sono ancora iscritto
    registered_event_ids = EventRegistration.objects.filter(user=user).values_list('event_id', flat=True)
    available_events = Event.objects.filter(
        start_date__gte=now,
        status='published'
    ).exclude(
        id__in=registered_event_ids
    ).select_related('organizer').order_by('start_date')[:6]
    
    # === LE MIE MENTORSHIP ===
    # Come mentor
    my_mentorships_mentor = Mentorship.objects.filter(
        mentor=user,
        status__in=['pending', 'active']
    ).select_related('mentee', 'mentee__profile').order_by('-created_at')[:3]
    
    # Come mentee
    my_mentorships_mentee = Mentorship.objects.filter(
        mentee=user,
        status__in=['pending', 'active']
    ).select_related('mentor', 'mentor__profile').order_by('-created_at')[:3]
    
    # Prossime sessioni
    upcoming_sessions = MentorshipSession.objects.filter(
        Q(mentorship__mentor=user) | Q(mentorship__mentee=user),
        session_date__gte=now,
        completed=False,
        cancelled=False
    ).select_related('mentorship', 'mentorship__mentor', 'mentorship__mentee').order_by('session_date')[:5]
    
    # === LE MIE CHALLENGE ===
    my_challenges = ChallengeParticipation.objects.filter(
        user=user
    ).select_related('challenge').order_by('-joined_at')[:5]
    
    # Challenge attive disponibili
    my_challenge_ids = ChallengeParticipation.objects.filter(user=user).values_list('challenge_id', flat=True)
    available_challenges = Challenge.objects.filter(
        status='active',
        start_date__lte=now.date(),
        end_date__gte=now.date()
    ).exclude(
        id__in=my_challenge_ids
    ).order_by('-created_at')[:4]
    
    # === I MIEI BADGE ===
    my_badges = UserBadge.objects.filter(
        user=user
    ).select_related('badge').order_by('-awarded_at')[:6]
    
    # Badge disponibili (non ancora ottenuti)
    my_badge_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    available_badges = Badge.objects.filter(
        is_active=True
    ).exclude(
        id__in=my_badge_ids
    ).order_by('display_order', 'name')[:6]
    
    # === COMPETENZE SUGGERITE ===
    # Competenze popolari che l'utente non ha
    my_skill_ids = UserSkill.objects.filter(user=user).values_list('skill_id', flat=True)
    suggested_skills = Skill.objects.filter(
        is_active=True
    ).exclude(
        id__in=my_skill_ids
    ).annotate(
        total_users=Count('user_skills')
    ).order_by('-total_users')[:6]
    
    # === ATTIVITÀ RECENTI ===
    recent_activities = []
    
    # Badge recenti (ultimi 7 giorni)
    recent_badges = UserBadge.objects.filter(
        user=user,
        awarded_at__gte=now - timedelta(days=7)
    ).select_related('badge').order_by('-awarded_at')[:3]
    for ub in recent_badges:
        recent_activities.append({
            'type': 'badge',
            'icon': 'fa-award',
            'color': 'warning',
            'title': f'Badge ottenuto: {ub.badge.name}',
            'date': ub.awarded_at,
            'url': '#'
        })
    
    # Registrazioni eventi recenti
    recent_registrations = EventRegistration.objects.filter(
        user=user,
        registered_at__gte=now - timedelta(days=7)
    ).select_related('event').order_by('-registered_at')[:3]
    for reg in recent_registrations:
        recent_activities.append({
            'type': 'event',
            'icon': 'fa-calendar-check',
            'color': 'success',
            'title': f'Iscritto a: {reg.event.title}',
            'date': reg.registered_at,
            'url': '#'
        })
    
    # Challenge join recenti
    recent_challenge_joins = ChallengeParticipation.objects.filter(
        user=user,
        joined_at__gte=now - timedelta(days=7)
    ).select_related('challenge').order_by('-joined_at')[:3]
    for cp in recent_challenge_joins:
        recent_activities.append({
            'type': 'challenge',
            'icon': 'fa-trophy',
            'color': 'primary',
            'title': f'Partecipazione challenge: {cp.challenge.title}',
            'date': cp.joined_at,
            'url': '#'
        })
    
    # Ordina attività per data
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = recent_activities[:10]
    
    # === STATISTICHE GLOBALI ===
    global_stats = {
        'total_users': UserSkill.objects.values('user').distinct().count(),
        'total_skills': Skill.objects.filter(is_active=True).count(),
        'total_events': Event.objects.count(),
        'active_challenges': Challenge.objects.filter(status='active').count(),
        'total_badges_awarded': UserBadge.objects.count(),
    }
    
    context = {
        'user': user,
        'user_stats': user_stats,
        'my_skills': my_skills,
        'skills_by_category': skills_by_category,
        'my_upcoming_events': my_upcoming_events,
        'my_past_events': my_past_events,
        'available_events': available_events,
        'my_mentorships_mentor': my_mentorships_mentor,
        'my_mentorships_mentee': my_mentorships_mentee,
        'upcoming_sessions': upcoming_sessions,
        'my_challenges': my_challenges,
        'available_challenges': available_challenges,
        'my_badges': my_badges,
        'available_badges': available_badges,
        'suggested_skills': suggested_skills,
        'recent_activities': recent_activities,
        'global_stats': global_stats,
    }
    
    return render(request, 'core/dashboard.html', context)

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)
