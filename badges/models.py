from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Badge(models.Model):
    RARITY_CHOICES = [
        ('common', 'Comune'),
        ('uncommon', 'Non Comune'),
        ('rare', 'Raro'),
        ('epic', 'Epico'),
        ('legendary', 'Leggendario'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    criteria = models.JSONField(default=dict)
    points = models.IntegerField(default=0)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    auto_award = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#3B82F6')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def times_awarded(self):
        return self.user_badges.count()

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    awarded_at = models.DateTimeField(auto_now_add=True)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='badges_awarded')
    notes = models.TextField(blank=True)
    blockchain_tx = models.CharField(max_length=200, blank=True)
    nft_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name = 'Badge Utente'
        verbose_name_plural = 'Badges Utenti'
        unique_together = ['user', 'badge']
        ordering = ['-awarded_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.badge.name}"
