from django.urls import path
from . import views

app_name = 'badges'

urlpatterns = [
    path('', views.badge_list, name='badge_list'),
    path('my/', views.my_badges, name='my_badges'),
]
