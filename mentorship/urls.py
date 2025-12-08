from django.urls import path
from . import views

app_name = 'mentorship'

urlpatterns = [
    path('', views.mentorship_list, name='mentorship_list'),
    path('my/', views.my_mentorships, name='my_mentorships'),
    path('request/<int:mentor_id>/', views.request_mentor, name='request_mentor'),
    path('accept/<int:mentorship_id>/', views.accept_mentorship, name='accept_mentorship'),
    path('reject/<int:mentorship_id>/', views.reject_mentorship, name='reject_mentorship'),
    path('end/<int:mentorship_id>/', views.end_mentorship, name='end_mentorship'),
]
