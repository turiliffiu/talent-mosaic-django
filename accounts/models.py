from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Pubblico'),
        ('private', 'Privato'),
        ('connections', 'Solo Connessioni'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    department = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    linkedin_url = models.URLField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profilo Utente'
        verbose_name_plural = 'Profili Utenti'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.job_title}"
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def skills_count(self):
        return self.user.skills.count()
    
    @property
    def badges_count(self):
        return self.user.badges.count()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
