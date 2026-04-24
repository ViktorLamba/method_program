import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import SimpleTestCase

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        phone="+79990000001",
        password="StrongPass123",
    )


@pytest.fixture
def auth_client(client, user):
    client.login(username="testuser", password="StrongPass123")
    return client


@pytest.fixture
def user_with_permission(db):
    user = User.objects.create_user(
        username="permuser",
        email="permuser@example.com",
        phone="+79990000002",
        password="StrongPass123",
    )
    permission = Permission.objects.get(codename="view_group")
    user.user_permissions.add(permission)
    return user


@pytest.fixture
def friend_user(db):
    return User.objects.create_user(
        username="friend",
        email="friend@example.com",
        phone="+79990000003",
        password="StrongPass123",
    )


@pytest.fixture
def stranger_user(db):
    return User.objects.create_user(
        username="stranger",
        email="stranger@example.com",
        phone="+79990000004",
        password="StrongPass123",
    )


@pytest.fixture
def redirect_assertor():
    return SimpleTestCase()
