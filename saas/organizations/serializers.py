from rest_framework import serializers
from .models import Organization, Membership
from users.serializers import UserSerializer

class MembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Membership
        fields = ["id", "user", "role", "joined_at"]

class OrganizationSerializer(serializers.ModelSerializer):
    memberships = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ["id", "name", "owner", "created_at", "memberships"]