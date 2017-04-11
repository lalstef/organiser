import datetime
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, mixins, authentication, status
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from rest_framework.response import Response

from organiser.tasks.serializers import TaskSerializer, UserSerializer
from organiser.tasks.models import Task
from organiser.tasks.permissions import IsOwnerOrReadOnly


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('-create_timestamp')
    serializer_class = TaskSerializer

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['owner'] = request.user.id
        data['create_user'] = request.user.id
        data['update_user'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route()
    def overdue(self, request):
        overdue_tasks = Task.objects.all().filter(due_datetime__lt=datetime.datetime.now())
        page = self.paginate_queryset(overdue_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)

    @list_route()
    def mine(self, request):
        my_tasks = Task.objects.all().filter(owner=request.user)
        page = self.paginate_queryset(my_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_tasks, many=True)
        return Response(serializer.data)

    @list_route()
    def recent(self, request):
        recent_tasks = Task.objects.all().filter(create_timestamp__gt=datetime.datetime.now() - datetime.timedelta(minutes=60))
        page = self.paginate_queryset(recent_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_tasks, many=True)
        return Response(serializer.data)


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AuthenticationView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'token': user.auth_token.key})
        else:
            return Response({'token': ''})


