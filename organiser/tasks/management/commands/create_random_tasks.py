from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from organiser.tasks.utils import RandomTaskGenerator


class Command(BaseCommand):
    help = 'Creates random Tasks'

    def add_arguments(self, parser):
        parser.add_argument('--number', type=int, default=10)
        parser.add_argument('--owner', type=str, default='')

    def handle(self, *args, **options):
        if options['owner']:
            owners = User.objects.filter(email=options['owner'])
        else:
            owners = User.objects.all()

        task_generator = RandomTaskGenerator(owners=owners)
        task_generator.generate(number=options['number'], save=True)

        self.stdout.write(self.style.SUCCESS('Successfully created {} tasks.'.format(options['number'])))
