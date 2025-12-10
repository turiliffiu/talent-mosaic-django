# projects/models.py
"""
Modelli per il sistema di progetti e team matching con AI
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json

class Project(models.Model):
    """Progetto che richiede un team di talenti"""
    
    STATUS_CHOICES = [
        ('draft', 'Bozza'),
        ('open', 'Aperto'),
        ('matching', 'In Matching'),
        ('active', 'Attivo'),
        ('completed', 'Completato'),
        ('cancelled', 'Annullato'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Bassa'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    # Info Base
    title = models.CharField(max_length=200, verbose_name="Titolo")
    description = models.TextField(verbose_name="Descrizione")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Manager/Creator
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_created')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects_managed')
    
    # Timeline
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    estimated_duration_weeks = models.IntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    
    # Budget & Resources
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    team_size_min = models.IntegerField(default=3, validators=[MinValueValidator(1)])
    team_size_max = models.IntegerField(default=8, validators=[MinValueValidator(1)])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    @property
    def team_members_count(self):
        return self.team_members.filter(status='accepted').count()
    
    @property
    def is_team_complete(self):
        return self.team_members_count >= self.team_size_min


class ProjectRequiredSkill(models.Model):
    """Competenze richieste per un progetto"""
    
    IMPORTANCE_CHOICES = [
        ('required', 'Obbligatoria'),
        ('preferred', 'Preferita'),
        ('nice_to_have', 'Nice to Have'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='required_skills')
    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE)
    
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='required')
    min_proficiency = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Livello minimo richiesto (1-5)"
    )
    min_years_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0,
        help_text="Anni esperienza minimi"
    )
    
    # Peso per algoritmo AI
    weight = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Peso nell'algoritmo di matching (1-100)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['project', 'skill']
        ordering = ['-importance', '-weight']
    
    def __str__(self):
        return f"{self.skill.name} per {self.project.title}"


class ProjectRole(models.Model):
    """Ruoli specifici richiesti nel progetto"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='roles')
    
    title = models.CharField(max_length=100, verbose_name="Titolo Ruolo")
    description = models.TextField(blank=True)
    positions_available = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    positions_filled = models.IntegerField(default=0)
    
    # Skill requirements per questo ruolo
    required_skills = models.ManyToManyField('skills.Skill', related_name='project_roles')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} - {self.project.title}"
    
    @property
    def is_filled(self):
        return self.positions_filled >= self.positions_available


class TeamMember(models.Model):
    """Membro del team di un progetto"""
    
    STATUS_CHOICES = [
        ('suggested', 'Suggerito da AI'),
        ('invited', 'Invitato'),
        ('accepted', 'Accettato'),
        ('declined', 'Rifiutato'),
        ('removed', 'Rimosso'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='team_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.ForeignKey(ProjectRole, on_delete=models.SET_NULL, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='invited')
    
    # AI Matching Score
    match_score = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Score di match AI (0-100)"
    )
    match_reasoning = models.JSONField(
        default=dict,
        help_text="Dettagli del perché è stato matchato"
    )
    
    # Dates
    invited_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(null=True, blank=True)
    
    # Contribution
    contribution_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['project', 'user']
        ordering = ['-match_score', '-invited_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} in {self.project.title}"


class AIMatchingRun(models.Model):
    """Traccia le esecuzioni dell'algoritmo di matching"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='matching_runs')
    
    # Execution info
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)
    
    # Parametri usati
    parameters = models.JSONField(
        default=dict,
        help_text="Parametri algoritmo (pesi, filtri, etc)"
    )
    
    # Risultati
    candidates_found = models.IntegerField(default=0)
    candidates_data = models.JSONField(
        default=list,
        help_text="Lista candidati con score e dettagli"
    )
    
    # Performance
    execution_time_seconds = models.FloatField(default=0)
    
    # Status
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-executed_at']
    
    def __str__(self):
        return f"Matching per {self.project.title} - {self.executed_at.strftime('%Y-%m-%d %H:%M')}"


class MatchingPreference(models.Model):
    """Preferenze globali per l'algoritmo di matching"""
    
    # Pesi features
    skill_match_weight = models.IntegerField(default=40, validators=[MinValueValidator(0), MaxValueValidator(100)])
    experience_weight = models.IntegerField(default=25, validators=[MinValueValidator(0), MaxValueValidator(100)])
    availability_weight = models.IntegerField(default=20, validators=[MinValueValidator(0), MaxValueValidator(100)])
    past_performance_weight = models.IntegerField(default=15, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Filtri
    min_overall_score = models.FloatField(default=60.0, help_text="Score minimo per essere considerato")
    max_candidates_per_run = models.IntegerField(default=20, help_text="Max candidati da restituire")
    
    # Diversity
    promote_diversity = models.BooleanField(default=True, help_text="Promuovi diversità nel team")
    diversity_weight = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Active
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Preferenza Matching"
        verbose_name_plural = "Preferenze Matching"
    
    def __str__(self):
        return f"Config {self.id} - {'Attiva' if self.is_active else 'Inattiva'}"


# Admin & Analytics Models

class AdminAction(models.Model):
    """Log delle azioni admin per audit"""
    
    ACTION_TYPES = [
        ('create', 'Creazione'),
        ('update', 'Modifica'),
        ('delete', 'Eliminazione'),
        ('approve', 'Approvazione'),
        ('reject', 'Rifiuto'),
        ('ban', 'Ban'),
        ('unban', 'Rimozione Ban'),
        ('export', 'Export Dati'),
        ('matching', 'Esecuzione Matching'),
    ]
    
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    
    # Target
    content_type = models.CharField(max_length=50)  # 'Project', 'Event', 'Challenge', etc
    object_id = models.IntegerField()
    object_repr = models.CharField(max_length=200)
    
    # Details
    description = models.TextField()
    changes = models.JSONField(default=dict, help_text="Cosa è cambiato")
    
    # Context
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=250, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Azione Admin"
        verbose_name_plural = "Azioni Admin"
    
    def __str__(self):
        return f"{self.admin.username} - {self.get_action_type_display()} - {self.object_repr}"
