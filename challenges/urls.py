from django.urls import path
from . import views

app_name = 'challenges'

urlpatterns = [
    path('', views.challenge_list, name='challenge_list'),
    path('my/', views.my_challenges, name='my_challenges'),
    path('participate/<int:challenge_id>/', views.challenge_participate, name='challenge_participate'),
    path('leave/<int:participation_id>/', views.challenge_leave, name='challenge_leave'),
    path('update-progress/<int:participation_id>/', views.challenge_update_progress, name='challenge_update_progress'),
]
