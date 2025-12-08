from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Challenge, ChallengeParticipation

def challenge_list(request):
    """List active challenges with filters"""
    now = timezone.now().date()
    
    # Filtri
    status_filter = request.GET.get('status', 'active')  # active, upcoming, completed
    search_query = request.GET.get('search', '')
    
    # Query base
    challenges = Challenge.objects.all().select_related('created_by').annotate(
        total_participants=Count('participations')
    )
    
    # Filtro status
    if status_filter == 'active':
        challenges = challenges.filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now
        )
    elif status_filter == 'upcoming':
        challenges = challenges.filter(start_date__gt=now)
    elif status_filter == 'completed':
        challenges = challenges.filter(status='completed')
    
    # Ricerca
    if search_query:
        challenges = challenges.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    challenges = challenges.order_by('-created_at')
    
    # Check partecipazioni utente
    user_participating_ids = []
    if request.user.is_authenticated:
        user_participating_ids = list(
            ChallengeParticipation.objects.filter(user=request.user)
            .values_list('challenge_id', flat=True)
        )
    
    context = {
        'challenges': challenges,
        'status_filter': status_filter,
        'search_query': search_query,
        'user_participating_ids': user_participating_ids,
        'now': now,
    }
    return render(request, 'challenges/challenge_list.html', context)

@login_required
def my_challenges(request):
    """List user's challenge participations"""
    now = timezone.now().date()
    
    # Challenge attive
    active_participations = ChallengeParticipation.objects.filter(
        user=request.user,
        challenge__status='active',
        challenge__end_date__gte=now
    ).select_related('challenge').order_by('-joined_at')
    
    # Challenge completate
    completed_participations = ChallengeParticipation.objects.filter(
        user=request.user,
        completed=True
    ).select_related('challenge').order_by('-completed_at')
    
    # Statistiche
    stats = {
        'total': ChallengeParticipation.objects.filter(user=request.user).count(),
        'active': active_participations.count(),
        'completed': completed_participations.count(),
        'total_points': sum([p.points_earned for p in ChallengeParticipation.objects.filter(user=request.user)]),
    }
    
    context = {
        'active_participations': active_participations,
        'completed_participations': completed_participations,
        'stats': stats,
        'now': now,
    }
    return render(request, 'challenges/my_challenges.html', context)

@login_required
def challenge_participate(request, challenge_id):
    """Join a challenge"""
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
    # Check se già partecipa
    if ChallengeParticipation.objects.filter(user=request.user, challenge=challenge).exists():
        messages.warning(request, 'Partecipi già a questa challenge')
        return redirect('challenges:my_challenges')
    
    # Check se challenge è attiva
    if challenge.status != 'active':
        messages.error(request, 'Questa challenge non è attiva')
        return redirect('challenges:challenge_list')
    
    # Crea partecipazione
    ChallengeParticipation.objects.create(
        user=request.user,
        challenge=challenge,
        points_earned=0
    )
    
    messages.success(request, f'Hai aderito alla challenge "{challenge.title}"!')
    return redirect('challenges:my_challenges')

@login_required
def challenge_leave(request, participation_id):
    """Leave a challenge"""
    participation = get_object_or_404(
        ChallengeParticipation,
        id=participation_id,
        user=request.user
    )
    
    # Check se già completata
    if participation.completed:
        messages.error(request, 'Non puoi abbandonare una challenge completata')
        return redirect('challenges:my_challenges')
    
    challenge_title = participation.challenge.title
    participation.delete()
    
    messages.success(request, f'Hai abbandonato la challenge "{challenge_title}"')
    return redirect('challenges:my_challenges')

@login_required
def challenge_update_progress(request, participation_id):
    """Update challenge progress"""
    participation = get_object_or_404(
        ChallengeParticipation,
        id=participation_id,
        user=request.user
    )
    
    if request.method == 'POST':
        points = int(request.POST.get('points', participation.points_earned))
        progress = int(request.POST.get('progress', 0))
        notes = request.POST.get('notes', '')
        
        participation.points_earned = min(points, participation.challenge.points)
        
        # Usa progress_data JSON per salvare progress e notes
        participation.progress_data = {
            'progress': min(progress, 100),
            'notes': notes
        }
        
        # Auto-complete se raggiunge 100%
        if progress >= 100 and not participation.completed:
            participation.completed = True
            participation.completed_at = timezone.now()
            participation.save()
            messages.success(request, f'🎉 Congratulazioni! Hai completato la challenge "{participation.challenge.title}"!')
        else:
            participation.save()
            messages.success(request, 'Progress aggiornato!')
    
    return redirect('challenges:my_challenges')
