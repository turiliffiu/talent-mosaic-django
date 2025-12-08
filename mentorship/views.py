from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q, Count
from .models import Mentorship, MentorshipSession

@login_required
def mentorship_list(request):
    """Find mentors"""
    search_query = request.GET.get('search', '')
    
    # Trova utenti che possono essere mentor (hanno is_mentor=True nel profile)
    mentors = User.objects.filter(
        profile__is_mentor=True
    ).exclude(
        id=request.user.id
    ).select_related('profile').annotate(
        mentees_count=Count('mentorships_as_mentor')
    )
    
    # Ricerca
    if search_query:
        mentors = mentors.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(profile__job_title__icontains=search_query) |
            Q(profile__department__icontains=search_query)
        )
    
    # Check richieste già inviate
    existing_requests = Mentorship.objects.filter(
        mentee=request.user,
        status__in=['pending', 'active']
    ).values_list('mentor_id', flat=True)
    
    context = {
        'mentors': mentors,
        'search_query': search_query,
        'existing_requests': list(existing_requests),
    }
    return render(request, 'mentorship/mentorship_list.html', context)

@login_required
def my_mentorships(request):
    """User's mentorships"""
    # Come mentee
    my_mentorships_mentee = Mentorship.objects.filter(
        mentee=request.user
    ).select_related('mentor', 'mentor__profile').order_by('-created_at')
    
    # Come mentor
    my_mentorships_mentor = Mentorship.objects.filter(
        mentor=request.user
    ).select_related('mentee', 'mentee__profile').order_by('-created_at')
    
    # Statistiche
    stats = {
        'as_mentee': my_mentorships_mentee.count(),
        'as_mentor': my_mentorships_mentor.count(),
        'active_as_mentee': my_mentorships_mentee.filter(status='active').count(),
        'active_as_mentor': my_mentorships_mentor.filter(status='active').count(),
    }
    
    context = {
        'my_mentorships_mentee': my_mentorships_mentee,
        'my_mentorships_mentor': my_mentorships_mentor,
        'stats': stats,
    }
    return render(request, 'mentorship/my_mentorships.html', context)

@login_required
def request_mentor(request, mentor_id):
    """Request mentorship"""
    mentor = get_object_or_404(User, id=mentor_id, profile__is_mentor=True)
    
    # Check se richiesta già esiste
    if Mentorship.objects.filter(
        mentor=mentor,
        mentee=request.user,
        status__in=['pending', 'active']
    ).exists():
        messages.warning(request, 'Hai già una richiesta attiva con questo mentor')
        return redirect('mentorship:mentorship_list')
    
    # Check non può essere mentor di se stesso
    if mentor == request.user:
        messages.error(request, 'Non puoi richiedere mentorship a te stesso')
        return redirect('mentorship:mentorship_list')
    
    # Crea richiesta
    Mentorship.objects.create(
        mentor=mentor,
        mentee=request.user,
        status='pending'
    )
    
    messages.success(request, f'Richiesta di mentorship inviata a {mentor.get_full_name()}!')
    return redirect('mentorship:my_mentorships')

@login_required
def accept_mentorship(request, mentorship_id):
    """Accept mentorship request"""
    mentorship = get_object_or_404(
        Mentorship,
        id=mentorship_id,
        mentor=request.user,
        status='pending'
    )
    
    mentorship.status = 'active'
    mentorship.save()
    
    messages.success(request, f'Hai accettato la mentorship con {mentorship.mentee.get_full_name()}!')
    return redirect('mentorship:my_mentorships')

@login_required
def reject_mentorship(request, mentorship_id):
    """Reject mentorship request"""
    mentorship = get_object_or_404(
        Mentorship,
        id=mentorship_id,
        mentor=request.user,
        status='pending'
    )
    
    mentorship.status = 'rejected'
    mentorship.save()
    
    messages.info(request, 'Richiesta di mentorship rifiutata')
    return redirect('mentorship:my_mentorships')

@login_required
def end_mentorship(request, mentorship_id):
    """End mentorship"""
    mentorship = get_object_or_404(
        Mentorship,
        id=mentorship_id,
        status='active'
    )
    
    # Solo mentor o mentee possono terminare
    if mentorship.mentor != request.user and mentorship.mentee != request.user:
        messages.error(request, 'Non autorizzato')
        return redirect('mentorship:my_mentorships')
    
    mentorship.status = 'completed'
    mentorship.save()
    
    messages.success(request, 'Mentorship conclusa')
    return redirect('mentorship:my_mentorships')
