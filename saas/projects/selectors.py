from .models import Project, Task


def get_user_projects(user):
    return Project.objects.filter(
        organization__memberships__user=user
    ).select_related("organization", "created_by")


def get_user_tasks(user):
    return Task.objects.filter(
        project__organization__memberships__user=user
    ).select_related("assigned_to", "project")