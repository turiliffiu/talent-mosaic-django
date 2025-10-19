from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Categoria Competenza'
        verbose_name_plural = 'Categorie Competenze'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.SET_NULL, null=True, related_name='skills')
    description = models.TextField(blank=True)
    keywords = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Competenza'
        verbose_name_plural = 'Competenze'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def users_count(self):
        return self.user_skills.count()

class UserSkill(models.Model):
    PROFICIENCY_CHOICES = [
        (1, 'Principiante'),
        (2, 'Base'),
        (3, 'Intermedio'),
        (4, 'Avanzato'),
        (5, 'Esperto'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='user_skills')
    proficiency = models.IntegerField(choices=PROFICIENCY_CHOICES, default=1)
    years_experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_skills')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Competenza Utente'
        verbose_name_plural = 'Competenze Utenti'
        unique_together = ['user', 'skill']
        ordering = ['-proficiency', 'skill__name']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name} ({self.get_proficiency_display()})"
