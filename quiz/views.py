import json
import random

# Create your views here.
from django.http import HttpResponse


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import CustomUser

from django.urls import reverse

# views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from .models import CustomUser


def login_signup_view(request):
    if request.method == 'POST':
        if 'login-form' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)

            if user:
                login(request, user)
                return redirect(reverse('home'))
            else:
                return render(request, 'login.html', {'login_error': True})

        elif 'signup-form' in request.POST:
            form = UserCreationForm(request.POST)

            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                # Check if the user already exists
                if CustomUser.objects.filter(email=email).exists():
                    return render(request, 'login.html', {'signup_error': True, 'error_message': 'User with this email already exists.'})

                # Create a new user
                user = CustomUser.objects.create_user(
                    email=email, password=password, name=name)
                login(request, user)
                return redirect(reverse('home'))
            else:
                return render(request, 'login.html', {'signup_error': True, 'form': form, 'error_message': 'Invalid form submission. Please check the form fields.'})

    return render(request, 'login.html')






def hello(request):
    return HttpResponse("Hello world!")


def signin(request):
    return render(request, 'signin.html')

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')


def game(request):
    return render(request, 'game.html')
