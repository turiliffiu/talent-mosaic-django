from django import forms
from .models import UserSkill

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['proficiency', 'years_experience', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
