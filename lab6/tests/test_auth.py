import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.mark.django_db
def test_registration_success_autologin_and_phone(client):
    response = client.post(
        reverse("register"),
        {
            "username": "new_user",
            "email": "new@example.com",
            "phone": "+79990000005",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("profile_me")
    user = User.objects.get(username="new_user")
    assert user.phone == "+79990000005"
    assert str(user.pk) == client.session.get("_auth_user_id")

    profile_response = client.get(reverse("profile_me"))
    assert profile_response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload, error_field",
    [
        (
            {
                "username": "bad_user_1",
                "email": "bad@example.com",
                "phone": "+79990000006",
                "password1": "ComplexPass123",
                "password2": "AnotherPass123",
            },
            "password2",
        ),
        (
            {
                "username": "",
                "email": "bad2@example.com",
                "phone": "+79990000007",
                "password1": "ComplexPass123",
                "password2": "ComplexPass123",
            },
            "username",
        ),
        (
            {
                "username": "bad_user_3",
                "email": "bad3@example.com",
                "phone": "not-a-phone",
                "password1": "ComplexPass123",
                "password2": "ComplexPass123",
            },
            "phone",
        ),
    ],
)
def test_registration_errors(client, payload, error_field):
    response = client.post(reverse("register"), payload)

    assert response.status_code == 200
    assert error_field in response.context["form"].errors


@pytest.mark.django_db
def test_login_success_redirects_to_home(client, user, redirect_assertor):
    response = client.post(
        reverse("login"),
        {"username": "testuser", "password": "StrongPass123"},
    )

    redirect_assertor.assertRedirects(response, reverse("profile_me"), fetch_redirect_response=True)


@pytest.mark.django_db
def test_login_error_with_wrong_password(client, user):
    response = client.post(
        reverse("login"),
        {"username": "testuser", "password": "wrong"},
    )

    assert response.status_code == 200
    assert "__all__" in response.context["form"].errors


@pytest.mark.django_db
def test_logout(client, user):
    client.login(username="testuser", password="StrongPass123")
    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("home")
