from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_signup_view, name='login_signup'),
    path('home/', views.home, name='home'),
    path('game/', views.game, name='game'),



]
