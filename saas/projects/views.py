from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Project,Task,Comment
from .serializers import ProjectSerializer,TaskSerializer,CommentSerializer
from organizations.permissions import IsOrgAdmin
from .services import create_project,create_task
from .selectors import get_user_projects,get_user_tasks
from .services import create_task

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_projects(self.request.user)

    def perform_create(self, serializer):
        create_project(
            user=self.request.user,
            organization=serializer.validated_data["organization"],
            name=serializer.validated_data["name"],
            description=serializer.validated_data.get("description", "")
        )
    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsOrgAdmin()]
        return [IsAuthenticated()]

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_tasks(self.request.user)

    def perform_create(self, serializer):
        create_task(
            project=serializer.validated_data["project"],
            title=serializer.validated_data["title"],
            assigned_to=serializer.validated_data.get("assigned_to")
        )

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsOrgAdmin()]
        return [IsAuthenticated()]

class CommentViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            task__project__organization__memberships__user=self.request.user
        )