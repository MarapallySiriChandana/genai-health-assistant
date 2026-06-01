from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from chatbot.models import ChatHistory
from ml_module.models import SymptomPrediction
from image_module.models import ImageAnalysis

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, full_name=user.username)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def dashboard_view(request):
    # Fetch recent activities
    chats = ChatHistory.objects.filter(user=request.user)[:5]
    predictions = SymptomPrediction.objects.filter(user=request.user).order_by('-timestamp')[:5]
    uploads = ImageAnalysis.objects.filter(user=request.user).order_by('-timestamp')[:5]
    
    context = {
        'recent_chats': chats,
        'recent_predictions': predictions,
        'recent_uploads': uploads,
    }
    return render(request, 'accounts/dashboard.html', context)
