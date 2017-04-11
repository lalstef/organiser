pip install -r requirements/development.txt

export DJANGO_SETTINGS_MODULE="organiser.settings.development"
python manage.py makemigrations tasks
python manage.py migrate
python manage.py load_sample_data
python manage.py runserver
