from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('my/', views.my_skills, name='my_skills'),
]
