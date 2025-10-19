from django.db import models
from django.contrib.auth.models import User

class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Aggiornamento Profilo'),
        ('skill_add', 'Aggiunta Competenza'),
        ('event_register', 'Registrazione Evento'),
        ('badge_earned', 'Badge Ottenuto'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    entity_type = models.CharField(max_length=50, blank=True)
    entity_id = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log Attività'
        verbose_name_plural = 'Log Attività'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown'} - {self.get_action_display()}"
