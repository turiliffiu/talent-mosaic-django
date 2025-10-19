from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('training', 'Training'),
        ('webinar', 'Webinar'),
        ('conference', 'Conferenza'),
        ('social', 'Social'),
        ('other', 'Altro'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Bozza'),
        ('published', 'Pubblicato'),
        ('cancelled', 'Annullato'),
        ('completed', 'Completato'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    location_url = models.URLField(blank=True)
    is_online = models.BooleanField(default=False)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    max_participants = models.IntegerField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='events/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    related_skills = models.ManyToManyField('skills.Skill', blank=True, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventi'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%d/%m/%Y')}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def is_past(self):
        return self.end_date < timezone.now()
    
    @property
    def is_full(self):
        if not self.max_participants:
            return False
        return self.registrations.filter(status='registered').count() >= self.max_participants
    
    @property
    def registered_count(self):
        return self.registrations.filter(status='registered').count()
    
    @property
    def available_spots(self):
        if not self.max_participants:
            return None
        return max(0, self.max_participants - self.registered_count)

class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registrato'),
        ('attended', 'Partecipato'),
        ('no_show', 'Assente'),
        ('cancelled', 'Annullato'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    checked_in = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Registrazione Evento'
        verbose_name_plural = 'Registrazioni Eventi'
        unique_together = ['event', 'user']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} → {self.event.title}"
