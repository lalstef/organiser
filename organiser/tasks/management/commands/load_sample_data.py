import names
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from organiser.tasks.utils import RandomTaskGenerator


class Command(BaseCommand):
    help = 'Creates some users and tasks associated with them'

    def add_arguments(self, parser):
        parser.add_argument('--tasks', type=int, default=100)
        parser.add_argument('--users', type=int, default=10)

    def handle(self, *args, **options):
        # Create some users
        # User generation pattern is as follows:
        #   first_name = [generate_first_name]
        #   last_name = [generate_last_name]
        #   username = [first_name]_[last_name]
        #   email = [username]@organiser.com
        #   password = 'organiser123'
        users = []

        # Create superuser
        user = User(username='admin', first_name='Admin', last_name='Admin', email='admin@organiser.com', is_superuser=True, is_staff=True)
        user.set_password('adminadmin')
        users.append(user)

        for _ in range(options['users']):
            last_name = names.get_first_name()
            first_name = names.get_last_name()
            username = '{}_{}'.format(first_name.lower(), last_name.lower())
            email = '{}@organiser.com'.format(username)
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password('organiser123')
            users.append(user)
        User.objects.bulk_create(users)

        # Create auth tokens
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)

        # Create some tasks for the users
        owners = User.objects.all()
        task_generator = RandomTaskGenerator(owners=owners)
        task_generator.generate(number=options['tasks'], save=True)

        self.stdout.write(self.style.SUCCESS('Successfully created {} users and {} tasks.'.format(options['users'], options['tasks'])))
