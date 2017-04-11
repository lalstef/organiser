from django.contrib import admin
from organiser.tasks.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name_formatted', 'description_formatted', 'status', 'is_overdue', 'due_datetime', 'archived')

    def name_formatted(self, obj):
        MAX_DISPLAY_CHARACTERS = 20
        if len(obj.name) > MAX_DISPLAY_CHARACTERS:
            name = '{} ...'.format(obj.name[:MAX_DISPLAY_CHARACTERS])
        else:
            name = obj.name
        return name
    name_formatted.short_description = 'name'

    def description_formatted(self, obj):
        MAX_DISPLAY_CHARACTERS = 35
        if len(obj.description) > MAX_DISPLAY_CHARACTERS:
            description = '{} ...'.format(obj.description[:MAX_DISPLAY_CHARACTERS])
        else:
            description = obj.description
        return description
    description_formatted.short_description = 'description'


admin.site.register(Task, TaskAdmin)
