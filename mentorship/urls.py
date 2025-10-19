from django.urls import path
from . import views

app_name = 'mentorship'

urlpatterns = [
    path('', views.mentorship_list, name='mentorship_list'),
]
