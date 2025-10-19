from django.shortcuts import render
from .models import Event

def event_list(request):
    """List all published events"""
    events = Event.objects.filter(status='published').order_by('start_date')
    context = {
        'events': events,
    }
    return render(request, 'events/event_list.html', context)
