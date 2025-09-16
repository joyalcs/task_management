from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
# from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in
from rest_framework import permissions, status

from task.models import Task

from .serializers import LoginSerializer, TaskSerializer, TaskUpdateSerializer


# @extend_schema(responses=LoginSerializer, tags=['Account'])
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Authenticates a user and generates an access token and refresh token.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data['username']
            password = data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)

                user_logged_in.send(
                    sender=user.__class__,
                    request=request,
                    user=user
                )

                response_data = {
                    "status_code": 6000,
                    "data": {
                        "title": "success",
                        "message": "Login Successful",
                        "accesstoken": str(refresh.access_token),
                        "refreshtoken": str(refresh),
                        "name": username,
                    },
                }
            else:
                response_data = {
                    "status_code": 6001,
                    "data": {
                        "title": "Failed",
                        "message": "Invalid credentials",
                    },
                }
        else:
            response_data = {
                "status_code": 6001,
                "data": {
                    "title": "Validation error",
                },
            }

        return Response(response_data, status=status.HTTP_200_OK)
    

class UserTaskListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TaskUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
