from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import UserRegistrationForm
from django.urls import reverse_lazy

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been successfully created!')
            return redirect('profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        request.user.email  = request.POST.get('email')
        request.user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'blog/profile.html')

