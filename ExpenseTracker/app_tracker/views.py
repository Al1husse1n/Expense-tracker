from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Expense
from django.views.generic import TemplateView   #Provides a generic class-based view to render a static or context-driven template
from django.views.generic.edit import FormView  #CBV for forms
from django.views.generic  import ListView      #CBV for displaying list of objects
from datetime import datetime

def home(request):
    return render(request, "home/home.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})
