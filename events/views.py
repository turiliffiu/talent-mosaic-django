from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Event, EventRegistration

def event_list(request):
    """List all published events with filters"""
    now = timezone.now()
    
    # Filtri
    event_type = request.GET.get('type', '')
    time_filter = request.GET.get('time', 'upcoming')  # upcoming, past, all
    search_query = request.GET.get('search', '')
    
    # Query base
    events = Event.objects.filter(status='published').select_related('organizer')
    
    # Filtro temporale
    if time_filter == 'upcoming':
        events = events.filter(start_date__gte=now)
    elif time_filter == 'past':
        events = events.filter(end_date__lt=now)
    
    # Filtro tipo
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Ricerca
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Annotazioni
    events = events.annotate(
        registrations_count=Count('registrations')
    ).order_by('start_date' if time_filter == 'upcoming' else '-start_date')
    
    # Event types per filtro
    event_types = Event.EVENT_TYPES
    
    # Check registrazioni utente
    user_registered_ids = []
    if request.user.is_authenticated:
        user_registered_ids = list(
            EventRegistration.objects.filter(user=request.user)
            .values_list('event_id', flat=True)
        )
    
    context = {
        'events': events,
        'event_types': event_types,
        'selected_type': event_type,
        'time_filter': time_filter,
        'search_query': search_query,
        'user_registered_ids': user_registered_ids,
        'now': now,
    }
    return render(request, 'events/event_list.html', context)

@login_required
def event_register(request, event_id):
    """Register user to an event"""
    event = get_object_or_404(Event, id=event_id, status='published')
    
    # Check se già registrato
    if EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'Sei già iscritto a questo evento')
        return redirect('events:event_list')
    
    # Check posti disponibili
    if event.max_participants and event.is_full:
        messages.error(request, 'Evento al completo')
        return redirect('events:event_list')
    
    # Check data passata
    if event.start_date < timezone.now():
        messages.error(request, 'Non puoi iscriverti a un evento già iniziato')
        return redirect('events:event_list')
    
    # Crea registrazione
    EventRegistration.objects.create(
        user=request.user,
        event=event,
        status='registered'
    )
    
    messages.success(request, f'Iscrizione a "{event.title}" confermata!')
    return redirect('events:my_events')

@login_required
def event_unregister(request, registration_id):
    """Cancel event registration"""
    registration = get_object_or_404(
        EventRegistration, 
        id=registration_id, 
        user=request.user
    )
    
    event_title = registration.event.title
    
    # Check se evento già passato
    if registration.event.end_date < timezone.now():
        messages.error(request, 'Non puoi annullare iscrizione a evento passato')
        return redirect('events:my_events')
    
    registration.delete()
    messages.success(request, f'Iscrizione a "{event_title}" annullata')
    return redirect('events:my_events')

@login_required
def my_events(request):
    """List user's event registrations"""
    now = timezone.now()
    
    # Eventi futuri
    upcoming = EventRegistration.objects.filter(
        user=request.user,
        event__start_date__gte=now
    ).select_related('event', 'event__organizer').order_by('event__start_date')
    
    # Eventi passati
    past = EventRegistration.objects.filter(
        user=request.user,
        event__end_date__lt=now
    ).select_related('event', 'event__organizer').order_by('-event__end_date')
    
    context = {
        'upcoming_registrations': upcoming,
        'past_registrations': past,
        'now': now,
    }
    return render(request, 'events/my_events.html', context)
