from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("private/", views.private_page, name="private_page"),
    path("reports/", views.reports_page, name="reports_page"),
    path("users/", views.users_list, name="users_list"),
    path("profile/", views.profile_me, name="profile_me"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile_detail, name="profile_detail"),
    path("friends/add/<str:username>/", views.add_friend, name="add_friend"),
]
