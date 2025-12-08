from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('my/', views.my_events, name='my_events'),
    path('register/<int:event_id>/', views.event_register, name='event_register'),
    path('unregister/<int:registration_id>/', views.event_unregister, name='event_unregister'),
]
