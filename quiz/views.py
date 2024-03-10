from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from random import shuffle, sample
from django.utils import timezone
import random

from .models import CustomUser, Question, Game
from .backends import CustomUserBackend
from django.contrib.auth.hashers import make_password

def login_signup_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login-form':
            email = request.POST['email']
            password = request.POST['password']
            backend = CustomUserBackend()
            user = backend.authenticate(request, username=email, password=password)
            
            print(
                f"Email: {email}, Password: {password}, Hashed Password: {user.password if user else 'N/A'}, Authenticated User: {user}")

            if user:
                auth_login(request, user)
                messages.success(request, 'welcome back ')
                return redirect('home')
            else:
                messages.error(request, 'wrong password or email')
                return render(request, 'login.html', {'login_error': True})

        elif form_type == 'signup-form':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']

            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'login.html', {'signup_error': True, 'error_message': 'User with this email already exists.'})

            
            user = CustomUser.objects.create_user(
                username=email, name=name, email=email, password=password)

            auth_login(request, user, backend='quiz.backends.CustomUserBackend')
            messages.success(
                request, 'welcome , you have been created your account  successfully')
            return redirect(reverse('home'))
        else:
            messages.error(
                request, 'Invalid form submission. Please check the form fields.')
            return render(request, 'login.html', {'signup_error': True, 'error_message': 'Invalid form submission. Please check the form fields.'})

    return render(request, 'login.html')


def hello(request):
    return HttpResponse("Hello world!")


def signin(request):
    return render(request, 'signin.html')


def home(request):
    user_scores = None
    name = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user)
        name = user.name
        # Fetch the user ID (adjust this based on your actual user identification logic)
        user_id = user.id
        # Fetch best 5 scores for the specified user
        user_scores = Game.objects.filter(
            user__id=user_id).order_by('-score', 'game_date')[:5]
    return render(request, 'home.html', {'user_scores': user_scores, 'name': name})


def reset_password_view(request):
    return render(request, 'reset_password.html')


def game(request):
    name = None
    if request.user.is_authenticated:
        user = CustomUser.objects.get(email=request.user)
        name = user.name

        # Get all question IDs
        question_ids = list(Question.objects.values_list('id', flat=True))
        # Shuffle the question IDs for randomness
        shuffle(question_ids)
        # Check if random questions are already selected for this session
        if 'random_question_ids' not in request.session:
            
            random_question_ids = sample(question_ids, 5)

            # Store the random question IDs in the session
            request.session['random_question_ids'] = random_question_ids
        else:
            # Retrieve random question IDs from the session
            random_question_ids = request.session['random_question_ids']

        # Get the corresponding questions for the random question IDs
        random_questions = Question.objects.filter(id__in=random_question_ids)

        score = 0
        is_true = False
        result_data = []

        if request.method == 'POST':
            form_type = request.POST.get('form_type')

            if form_type == 'quiz-form':
                for question in random_questions:
                    print("inside post ", question.id)

                total_questions = len(random_questions)

                for question in random_questions:
                    question_id = question.id
                    print("question_id ", question_id)
                    user_answer = request.POST.get(f'answer_h_{question_id}')
                    print("user_answer ", user_answer)

                    correct_answer = question.correct_option.lower()
                    print("correct answer is :", correct_answer)

                    if user_answer and user_answer.lower() == correct_answer:
                        is_true = True
                        score += 20
                        print("score is  : ", score)

                    correct_answer_value = getattr(
                        question, f'option_{correct_answer.lower()}')

                    user_answer_value = getattr(
                        question, f'option_{user_answer.lower()}') if user_answer else None

                    result_data.append({
                        'question': question.question_text,
                        'correct_answer_letter': correct_answer.upper(),
                        'correct_answer_value': correct_answer_value,
                        'chosen_answer_letter': user_answer,
                        'user_answer_value': user_answer_value,
                        'correct': is_true,
                    })

                # Clear the session variable holding random question IDs for the next game
                del request.session['random_question_ids']

                game_instance = Game.objects.create(
                    user=request.user, score=score)
                result_message = score
                return JsonResponse({'result_message': result_message, 'result_data': result_data})

        return render(request, 'game.html', {'questions': random_questions, 'score': score, 'name': name})
    return redirect('login_signup')


# @login_required
# def game(request):
#     name = None
#     if request.user.is_authenticated:
#         user = CustomUser.objects.get(email=request.user)
#         name = user.name

#         random_questions = Question.objects.annotate(num=Count('id')).order_by('?')[:7]
#         score = 0
#         is_true = False
#         result_data = []
#         if request.method == 'POST':
#             form_type = request.POST.get('form_type')

#             if form_type == 'quiz-form':
#                 total_questions = len(random_questions)


#                 for question in random_questions:
#                     question_id = question.id
#                     user_answer = request.POST.get(f'answer_{question_id}')
#                     # Replace with the actual field name for correct answer
#                     correct_answer = question.correct_option.lower()
#                     print("correct answer is :",correct_answer)


#                     if user_answer and user_answer.lower() == correct_answer:
#                         is_true = True
#                         score += 20
#                         print("score is  : ",score)
#                         # Define the correct answer value based on correct_answer_letter
#                     correct_answer_value = getattr(
#                         question, f'option_{correct_answer.lower()}')

#                     # Define the user answer value based on chosen_answer_letter
#                     user_answer_value = getattr(
#                         question, f'option_{user_answer.lower()}') if user_answer else None

#                     # Append question details to the result_data list
#                     result_data.append({
#                         'question': question.question_text,
#                         'correct_answer_letter': correct_answer.upper(),
#                         'correct_answer_value': correct_answer_value,
#                         'chosen_answer_letter': user_answer,
#                         'user_answer_value': user_answer_value,
#                         'correct': is_true ,
#                     })

#                 # You can now use the 'score' variable to display the result or save it to the database
#                 # Change this line in your views.py
#                 print(request.user)
#                 if request.user.is_authenticated:
#                     print(request.user)
#                     game_instance = Game.objects.create(
#                         user=request.user, score=score)

#                 result_message = score
#                 print("this is data" ,result_data)
#                 return JsonResponse({'result_message': result_message, 'result_data': result_data})

#     return render(request, 'game.html', {'questions': random_questions, 'score': score, 'name': name})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    else:
        messages.warning(request, 'You are not logged in.')
    # Optional: add a logout message
    messages.success(request, 'You have been logged out.')
    return redirect('home')
