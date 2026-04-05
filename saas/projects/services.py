from .models import Project
from .models import Task

def create_project(*, user, organization, name, description=""):
    return Project.objects.create(
        name=name,
        description=description,
        organization=organization,
        created_by=user
    )

def create_task(*, project, title, assigned_to=None):
    return Task.objects.create(
        project=project,
        title=title,
        assigned_to=assigned_to
    )