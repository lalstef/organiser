from django.contrib.auth.models import User
from rest_framework import serializers
from organiser.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    due_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'status', 'owner', 'owner_username', 'due_datetime',
                  'create_timestamp', 'update_timestamp', 'create_user', 'update_user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
