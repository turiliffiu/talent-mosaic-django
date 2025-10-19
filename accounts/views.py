from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account creato con successo!')
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """View own profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    """Edit own profile"""
    return render(request, 'accounts/profile_edit.html', {'user': request.user})
