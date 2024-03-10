from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_signup_view, name='login_signup'),
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password_view, name='reset_password'),

]
