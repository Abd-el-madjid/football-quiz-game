from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from django.db.models import Count
import random
from .models import Question
from django.http import JsonResponse
from django.utils import timezone
from .models import Game
from django.db.models import Max


from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def login_signup_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login-form':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)

            if user:
                auth_login(request, user)
                messages.success(request, 'Your have been log in')
                return redirect(reverse('home'))

            else:
                messages.error(request, 'Your user name or passoqrd incorrect.')
                return render(request, 'login.html', {'login_error': True})

        elif form_type == 'signup-form':
            print("hi")
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            print(name)
            # Check if the user already exists
            if CustomUser.objects.filter(email=email).exists():
                print(CustomUser.objects.filter(email=email))
                print("hi2211")
                messages.error(request, 'account exict use another email')
                return render(request, 'login.html', {'signup_error': True, 'error_message': 'User with this email already exists.'})
            print("hi22")
            # Create a new user with the hashed password
            hashed_password = make_password(password)
            user = CustomUser.objects.create(name=name, email=email,username = email, password=hashed_password)
            messages.success(request, 'your account hav been created')

            auth_login(request, user)
            messages.success(request, 'Your have been log in')
            
            return redirect(reverse('game'))
        else:
            return render(request, 'login.html', {'signup_error': True, 'error_message': 'Invalid form submission. Please check the form fields.'})

    return render(request, 'login.html')

def hello(request):
    return HttpResponse("Hello world!")


def signin(request):
    return render(request, 'signin.html')



def home(request):
    # Fetch the user ID (adjust this based on your actual user identification logic)
    user_id = 1  # Replace 1 with the actual user ID

    # Fetch best 5 scores for the specified user
    user_scores = Game.objects.filter(user__id=user_id).order_by('-score', 'game_date')[:5]

    return render(request, 'home.html', {'user_scores': user_scores})





def login(request):
    return render(request, 'login.html')



def game(request):
  
    
    random_questions = Question.objects.annotate(num=Count('id')).order_by('?')[:5]
    score = 0
    is_true = False
    result_data = []
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'quiz-form':
            total_questions = len(random_questions)
            

            for question in random_questions:
                question_id = question.id
                user_answer = request.POST.get(f'answer_{question_id}')
                # Replace with the actual field name for correct answer
                correct_answer = question.correct_option.lower()
                print("correct answer is :",correct_answer)
                

                if user_answer and user_answer.lower() == correct_answer:
                    is_true = True
                    score += 20
                    print("score is  : ",score)
                    # Define the correct answer value based on correct_answer_letter
                correct_answer_value = getattr(
                    question, f'option_{correct_answer.lower()}')

                # Define the user answer value based on chosen_answer_letter
                user_answer_value = getattr(
                    question, f'option_{user_answer.lower()}') if user_answer else None

                # Append question details to the result_data list
                result_data.append({
                    'question': question.question_text,
                    'correct_answer_letter': correct_answer.upper(),
                    'correct_answer_value': correct_answer_value,
                    'chosen_answer_letter': user_answer,
                    'user_answer_value': user_answer_value,
                    'correct': is_true ,
                })

            # You can now use the 'score' variable to display the result or save it to the database
            game_instance = Game.objects.create(user=request.user, score=score)
            result_message = score
            return JsonResponse({'result_message': result_message, 'result_data': result_data})

    return render(request, 'game.html', {'questions': random_questions, 'score': score})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')  # Optional: add a logout message
    return redirect('home') 