# Oddaj-rzeczy

Portfolio lab project

in progress

Download and use it in your local environment:
Fork repository
Clone it into your computer
Create virtualenv for the project, install requirements using:
$ pip install -r Requirements.txt
create file local_settings.py with your local configuration:
DATABASES = {
'default': {
'HOST': 'localhost', 'NAME': 'your_db_name',
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'USER': 'username',
'PASSWORD': 'password',
}
}

create empty database in psql
run python manage.py makemigrations``python manage.py migrate
start test server.
Enjoy :)
