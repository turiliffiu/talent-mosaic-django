from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('my/', views.my_skills, name='my_skills'),
    path('add/<int:skill_id>/', views.add_skill, name='add_skill'),
    path('remove/<int:user_skill_id>/', views.remove_skill, name='remove_skill'),
    path('update/<int:user_skill_id>/', views.update_skill, name='update_skill'),
]
