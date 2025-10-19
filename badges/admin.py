from django.contrib import admin
from .models import Badge, UserBadge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rarity', 'points', 'auto_award', 'is_active')
    list_filter = ('rarity', 'auto_award', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at', 'awarded_by')
    list_filter = ('awarded_at',)
    search_fields = ('user__username', 'badge__name')
    raw_id_fields = ('user', 'badge', 'awarded_by')
    date_hierarchy = 'awarded_at'
