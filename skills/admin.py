from django.contrib import admin
from .models import SkillCategory, Skill, UserSkill

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'color')
    list_editable = ('display_order',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'proficiency', 'years_experience', 'verified', 'created_at')
    list_filter = ('proficiency', 'verified', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'skill__name')
    raw_id_fields = ('user', 'skill', 'verified_by')
    date_hierarchy = 'created_at'
