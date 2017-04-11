from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from organiser.tasks.models import Task


class Command(BaseCommand):
    help = 'Creates random Tasks'

    def add_arguments(self, parser):
        parser.add_argument('--owner', type=str, default='')

    def handle(self, *args, **options):
        queryset = Task.objects.all()
        if options['owner']:
            owner = User.objects.filter(email=options['owner'])
            if not owner:
                raise ValueError('User with email "{}" does not exist!'.format(options['owner']))
            else:
                owner = owner[0]
            queryset = queryset.filter(owner=owner)

        deleted_tasks, _ = queryset.delete_forever()

        self.stdout.write(self.style.SUCCESS('Successfully deleted {} tasks.'.format(deleted_tasks)))
