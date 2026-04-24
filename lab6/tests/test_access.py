import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_private_page_requires_auth(client, redirect_assertor):
    response = client.get(reverse("private_page"))

    expected = f"{reverse('login')}?next={reverse('private_page')}"
    redirect_assertor.assertRedirects(response, expected, fetch_redirect_response=True)


@pytest.mark.django_db
def test_private_page_for_authorized(auth_client):
    response = auth_client.get(reverse("private_page"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_permission_denied_without_permission(auth_client):
    response = auth_client.get(reverse("reports_page"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_permission_allowed_with_permission(client, user_with_permission):
    client.login(username="permuser", password="StrongPass123")
    response = client.get(reverse("reports_page"))

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("url_name", ["home", "register", "login"])
def test_public_pages_available(client, url_name):
    response = client.get(reverse(url_name))

    assert response.status_code == 200


@pytest.mark.django_db
def test_users_list_requires_auth(client, redirect_assertor):
    response = client.get(reverse("users_list"))
    expected = f"{reverse('login')}?next={reverse('users_list')}"
    redirect_assertor.assertRedirects(response, expected, fetch_redirect_response=True)


@pytest.mark.django_db
def test_users_list_available_for_authorized(auth_client):
    response = auth_client.get(reverse("users_list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_friend_profile_visible_after_adding_friend(auth_client, friend_user):
    response = auth_client.post(reverse("add_friend", kwargs={"username": friend_user.username}))
    assert response.status_code == 302

    profile_response = auth_client.get(reverse("profile_detail", kwargs={"username": friend_user.username}))
    assert profile_response.status_code == 200


@pytest.mark.django_db
def test_non_friend_profile_forbidden(auth_client, stranger_user):
    response = auth_client.get(reverse("profile_detail", kwargs={"username": stranger_user.username}))
    assert response.status_code == 403


@pytest.mark.django_db
def test_can_edit_own_profile(auth_client):
    response = auth_client.post(
        reverse("edit_profile"),
        {
            "first_name": "Иван",
            "last_name": "Петров",
            "email": "testuser@example.com",
            "phone": "+79990000111",
        },
    )

    assert response.status_code == 302


def test_404_error_page(client):
    response = client.get("/missing-page/")

    assert response.status_code == 404
