#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Usage:
    ./manage.py <command> [options]

Options:
    <command>          The command to execute (e.g., runserver, makemigrations).
    -h, --help         Show this help message and exit.
    --settings=FILE    The Python path to a settings module, e.g., "myproject.settings".
                      If this isn't provided, the DJANGO_SETTINGS_MODULE environment variable will be used.
    --pythonpath=PATH  A directory to add to the Python path, e.g., "/home/user/myproject".

Examples:
    ./manage.py runserver
    ./manage.py makemigrations
    ./manage.py migrate

For more information on Django management commands, see:
https://docs.djangoproject.com/en/stable/ref/django-admin/

For the latest version of this script and additional management commands, visit:
https://github.com/django/django
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_game.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
