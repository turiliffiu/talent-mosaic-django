from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Mentorship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'In Attesa'),
        ('active', 'Attiva'),
        ('completed', 'Completata'),
        ('cancelled', 'Annullata'),
    ]
    
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorships_as_mentor')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentorships_as_mentee')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    focus_areas = models.JSONField(default=list)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mentorships_created')
    
    class Meta:
        verbose_name = 'Mentorship'
        verbose_name_plural = 'Mentorships'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(mentor=models.F('mentee')),
                name='mentor_mentee_different'
            )
        ]
    
    def __str__(self):
        return f"{self.mentor.get_full_name()} → {self.mentee.get_full_name()}"
    
    @property
    def sessions_count(self):
        return self.sessions.count()

class MentorshipSession(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE, related_name='sessions')
    session_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    location = models.CharField(max_length=200, blank=True)
    agenda = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    mentor_notes = models.TextField(blank=True)
    mentee_notes = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Sessione Mentorship'
        verbose_name_plural = 'Sessioni Mentorship'
        ordering = ['-session_date']
    
    def __str__(self):
        return f"Sessione {self.mentorship} - {self.session_date.strftime('%d/%m/%Y')}"
