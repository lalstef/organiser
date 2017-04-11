from django.db import models


class TaskQuerySet(models.QuerySet):
    """
    QuerySet class which by default only 'archives' the Tasks instead of actually deleting them.
    The delete_forever() method must be used for the Tasks to actually be deleted.
    """

    def all(self, include_archived=False):
        clone = super(self.__class__, self).all()
        if not include_archived:
            clone = clone.filter(archived=False)
        return clone

    def filter(self, *args, **kwargs):
        """
        NB: Accepts additional parameter 'include_archived' (False by default).

        By default this method filters out the archived items. If 'archived' key-word argument
        is specified, then 'include_archived' is disregarded. Otherwise 'include_archived' is
        honored and it defines whether only non-archived or all Tasks will be acted upon.

        There are 3 possible scenarios:
            1. Non-Archived Tasks Only
            2. Archived Tasks Only
            3. All Tasks

        archived = False         -> Scenario #1 (Default)
        archived = True          -> Scenario #2
        include_archived = True  -> Scenario #3 (The only way to act upon all Tasks!)
        include_archived = False -> Scenario #1 (Default)
        """
        # If not explicitly requested otherwise, only act on the non-archived Tasks
        if 'archived' not in kwargs:
            if not kwargs.get('include_archived'):
                kwargs['archived'] = False

            # Remove 'include_archived' from kwargs since it's not a real field to filter on
            if 'include_archived' in kwargs:
                del kwargs['include_archived']

        return super(self.__class__, self).filter(*args, **kwargs)

    def delete(self):
        archived_tasks = self.update(archived=True)

        # Be consistent with the regular delete() method's return value
        return archived_tasks, {self.model._meta.label: archived_tasks}

    def delete_forever(self):
        return super(self.__class__, self).delete()


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(model=self.model, using=self._db, hints=self._hints)

    def all(self, include_archived=False):
        queryset = self.get_queryset()
        if not include_archived:
            queryset = queryset.filter(archived=False)
        return queryset
