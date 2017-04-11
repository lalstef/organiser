import datetime

from django.conf import settings
from django.db import models
from django.utils.timezone import make_aware
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from organiser.tasks.managers import TaskManager

class Base(models.Model):
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_tasks')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='updated_tasks')
    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Task(Base):
    STATUS = {
        'NOT_STARTED': 0,
        'IN_PROGRESS': 1,
        'DONE': 2,
        'CANCELLED': 3,
    }

    STATUS_LABEL_BY_CODE = {
        STATUS['NOT_STARTED']: 'NOT_STARTED',
        STATUS['IN_PROGRESS']: 'IN_PROGRESS',
        STATUS['DONE']: 'DONE',
        STATUS['CANCELLED']: 'CANCELLED',
    }

    STATUS_CHOICES = [
        (STATUS['NOT_STARTED'], 'NOT_STARTED'),
        (STATUS['IN_PROGRESS'], 'IN_PROGRESS'),
        (STATUS['DONE'], 'DONE'),
        (STATUS['CANCELLED'], 'CANCELLED'),
    ]

    name = models.CharField(max_length=64)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS['NOT_STARTED'])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_tasks', blank=True)
    due_datetime = models.DateTimeField(null=True, blank=True)

    objects = TaskManager()

    def __str__(self):
        MAX_DISPLAY_CHARACTERS = 10

        name = self.name
        if len(self.name) > MAX_DISPLAY_CHARACTERS:
            name = '{}...'.format(self.name[:MAX_DISPLAY_CHARACTERS])

        archived = ''
        if self.archived:
            archived = '(X)'

        return '{} [{}] - {} {}'.format(name, self.STATUS_LABEL_BY_CODE[self.status], self.owner.email, archived)

    def delete(self):
        """
        Don't actually delete the task, only set its 'archived' flag to True.
        """
        self.archived = True
        self.save()

        # Be consistent with the regular delete() method's return value
        return 1, {self._meta.label: 1}

    def undelete(self):
        self.archived = False
        self.save()

    def delete_forever(self, **kwargs):
        """
        Delete the tasks completely and definitely.
        """
        return super(self.__class__, self).delete(**kwargs)

    def set_status(self, status):
        if not status in self.STATUS.values():
            raise ValueError('Allowed values for status are: {}'.format(', '.join(self.STATUS.values())))
        self.status = status
        self.save()

    def set_status_not_started(self):
        self.status = self.STATUS['NOT_STARTED']
        self.save()

    def set_status_in_progress(self):
        self.status = self.STATUS['IN_PROGRESS']
        self.save()

    def set_status_done(self):
        self.status = self.STATUS['DONE']
        self.save()

    def set_status_cancelled(self):
        self.status = self.STATUS['CANCELLED']
        self.save()

    def is_not_started(self):
        return self.status == self.STATUS['NOT_STARTED']

    def is_in_progress(self):
        return self.status == self.STATUS['IN_PROGRESS']

    def is_done(self):
        return self.status == self.STATUS['DONE']

    def is_cancelled(self):
        return self.status == self.STATUS['CANCELLED']

    def is_overdue(self):
        if self.due_datetime is None:
            return False
        return self.due_datetime > make_aware(datetime.datetime.utcnow())

    @classmethod
    def get_not_started_tasks(cls, include_archived=False):
        queryset = cls.objects.filter(status=cls.STATUS['NOT_STARTED'])
        if not include_archived:
            queryset = queryset.filter(archived=False)
        return queryset

    @classmethod
    def get_in_progress_tasks(cls, include_archived=False):
        queryset = cls.objects.filter(status=cls.STATUS['IN_PROGRESS'])
        if not include_archived:
            queryset = queryset.filter(archived=False)
        return queryset

    @classmethod
    def get_done_tasks(cls, include_archived=False):
        queryset = cls.objects.filter(status=cls.STATUS['DONE'])
        if not include_archived:
            queryset = queryset.filter(archived=False)
        return queryset

    @classmethod
    def get_cancelled_tasks(cls, include_archived=False):
        queryset = cls.objects.filter(status=cls.STATUS['CANCELLED'])
        if not include_archived:
            queryset = queryset.filter(archived=False)
        return queryset

    @classmethod
    def get_overdue_tasks(cls, include_archived=False):
        queryset = cls.objects.filter(due_datetime__gt=datetime.datetime.utcnow())
        if not include_archived:
            queryset = queryset.filter(archived=False)
        return queryset


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
