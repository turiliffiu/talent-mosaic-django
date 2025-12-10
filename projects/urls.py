# projects/urls.py
"""
URL patterns per Admin Dashboard
"""
from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # Dashboard principale
    path('', views.admin_dashboard, name='dashboard'),
    
    # Progetti
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    
    # AI Matching
    path('projects/<int:project_id>/run-matching/', views.run_ai_matching, name='run_ai_matching'),
    path('projects/<int:project_id>/matching/<int:run_id>/', views.matching_results, name='matching_results'),
    path('projects/<int:project_id>/invite/<int:user_id>/', views.invite_candidate, name='invite_candidate'),
    
    # Eventi
    path('events/', views.event_list_admin, name='event_list'),
    
    # Challenge
    path('challenges/', views.challenge_list_admin, name='challenge_list'),
    
    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics'),
    
    # Settings
    path('settings/matching/', views.matching_preferences, name='matching_preferences'),
]
