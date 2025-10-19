from django.contrib import admin
from .models import Challenge, ChallengeParticipation

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'status', 'points')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'

@admin.register(ChallengeParticipation)
class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'user', 'points_earned', 'completed', 'joined_at')
    list_filter = ('completed', 'joined_at')
    search_fields = ('challenge__title', 'user__username')
    raw_id_fields = ('challenge', 'user')
