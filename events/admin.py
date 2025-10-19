from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'status', 'max_participants')
    list_filter = ('event_type', 'status', 'is_online', 'start_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    filter_horizontal = ('related_skills',)

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'checked_in', 'registered_at')
    list_filter = ('status', 'checked_in', 'registered_at')
    search_fields = ('event__title', 'user__username', 'user__email')
    raw_id_fields = ('event', 'user')
    date_hierarchy = 'registered_at'
