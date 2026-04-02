from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Project,Task,Comment
from .serializers import ProjectSerializer,TaskSerializer,CommentSerializer
from organizations.permissions import IsOrgAdmin

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            organization__memberships__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsOrgAdmin()]
        return [IsAuthenticated()]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()   
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]
    filterset_fields = ["status", "assigned_to"]
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "created_at"]
    def get_queryset(self):
        return Task.objects.filter(
            project__organization__memberships__user=self.request.user
        )

    # def get_permissions(self):
    #     if self.action in ["create", "update", "destroy"]:
    #         return [IsOrgAdmin()]
    #     return [IsAuthenticated()]

class CommentViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            task__project__organization__memberships__user=self.request.user
        )