from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

class Challenge(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Bozza'),
        ('active', 'Attiva'),
        ('completed', 'Completata'),
        ('cancelled', 'Annullata'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    goal = models.TextField(help_text="Obiettivo della challenge")
    rules = models.TextField(help_text="Regole di partecipazione")
    points = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    cover_image = models.ImageField(upload_to='challenges/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='challenges_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Challenge'
        verbose_name_plural = 'Challenges'
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def participants_count(self):
        return self.participations.count()
    
    @property
    def is_active(self):
        now = timezone.now().date()
        return self.start_date <= now <= self.end_date and self.status == 'active'

class ChallengeParticipation(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_participations')
    points_earned = models.IntegerField(default=0)
    progress_data = models.JSONField(default=dict)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Partecipazione Challenge'
        verbose_name_plural = 'Partecipazioni Challenges'
        unique_together = ['challenge', 'user']
        ordering = ['-points_earned', 'user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} → {self.challenge.title}"
