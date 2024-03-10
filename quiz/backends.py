from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import connection


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            print(f"User with email {username} does not exist.")
            return None

        stored_hashed_password = user.password
        print(
            f"Stored Hashed Password in CustomUserBackend: {stored_hashed_password}")

        if user.check_password(password):
            print(f"User {username} authenticated successfully.")
            return user
        else:
            print(f"User {username} authentication failed. Incorrect password.")
            return None


