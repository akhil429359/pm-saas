from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from organizations.models import Organization, Membership
from projects.models import Project
from rest_framework_simplejwt.tokens import RefreshToken

class BaseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="password123"
        )

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

        self.organization = Organization.objects.create(
            name="Test Org",
            owner=self.user
        )

class ProjectTests(BaseTestCase):

    def test_create_project(self):
        url = "/api/projects/"

        data = {
            "name": "Test Project",
            "organization": self.organization.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

def test_member_cannot_create_project(self):
    member = User.objects.create_user(
        email="member@test.com",
        username="member",
        password="password123"
    )

    Membership.objects.create(
        user=member,
        organization=self.organization,
        role="MEMBER"
    )

    refresh = RefreshToken.for_user(member)

    self.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    url = "/api/projects/"

    data = {
        "name": "Invalid Project",
        "organization": self.organization.id
    }

    response = self.client.post(url, data)

    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_user_cannot_see_other_org_data(self):
    other_user = User.objects.create_user(
        email="other@test.com",
        username="other",
        password="password123"
    )

    other_org = Organization.objects.create(
        name="Other Org",
        owner=other_user
    )

    Project.objects.create(
        name="Secret Project",
        organization=other_org,
        created_by=other_user
    )

    url = "/api/projects/"
    response = self.client.get(url)

    self.assertEqual(len(response.data["results"]), 0)