from rest_framework.permissions import BasePermission
from .models import Membership


class IsOrgAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Get organization safely
        if hasattr(obj, "organization"):
            org = obj.organization
        elif hasattr(obj, "project"):
            org = obj.project.organization
        elif hasattr(obj, "task"):
            org = obj.task.project.organization
        else:
            return False

        return Membership.objects.filter(
            user=request.user,
            organization=org,
            role="ADMIN"
        ).exists()