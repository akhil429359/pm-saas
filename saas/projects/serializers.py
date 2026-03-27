from rest_framework import serializers
from .models import Project, Task, Comment
from users.serializers import UserSerializer
from users.models import User

class ProjectSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ["id","name","description","organization","created_by","created_at",]

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assigned_to",
        write_only=True
    )
    class Meta:
        model = Task
        fields = ["id","title","description","status","assigned_to","due_date","project","created_at",]

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id","content","author","task","created_at",]