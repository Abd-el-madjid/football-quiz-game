# Quiz Game Django Project

This is a Django project for a quiz game with MySQL as the database. Follow the steps below to set up the project locally.

## Prerequisites

- Python 3.x
- MySQL installed

## Setup Instructions

1. **Create a Virtual Environment:**
   ```bash
   python -m venv venv

Activate the Virtual Environment:

 ```bash

source venv/bin/activate  # On Unix or MacOS
.\venv\Scripts\activate 
 ```
Navigate to the Project Directory:

 ```bash

cd quiz_game
 ```
Install Dependencies from requirements.txt:

 ```bash

pip install -r requirements.txt
 ```

Change MySQL Database Settings:

Open the settings.py file in the quiz_game project.
Locate the DATABASES configuration section.
Update the USER and PASSWORD fields with your MySQL database username and password.
Example:

python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quiz',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

Create MySQL Schema:

In your MySQL database, create a schema named 'quiz'.
Run Migrations:

 ```bash

python manage.py makemigrations
python manage.py migrate
 ```
after that  you can file table of question  with insertion  in bd.txt
Run the Development Server:

 ```bash

python manage.py runserver
 ```
Visit http://127.0.0.1:8000/ in your browser to access the quiz game.
