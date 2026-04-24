from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProfileEditForm, RegisterForm

User = get_user_model()


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile_me")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def private_page(request):
    return render(request, "private.html")


@permission_required("auth.view_group", raise_exception=True)
def reports_page(request):
    return render(request, "reports.html")


@login_required
def users_list(request):
    users = User.objects.exclude(pk=request.user.pk).order_by("username")
    friend_ids = set(request.user.friends.values_list("id", flat=True))
    return render(
        request,
        "users/list.html",
        {"users": users, "friend_ids": friend_ids},
    )


@login_required
def profile_me(request):
    return redirect("profile_detail", username=request.user.username)


@login_required
def profile_detail(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_self = request.user == profile_user
    is_friend = request.user.friends.filter(pk=profile_user.pk).exists()

    if not is_self and not is_friend:
        raise PermissionDenied("Нельзя просматривать профиль незнакомого пользователя.")

    return render(
        request,
        "users/profile_detail.html",
        {"profile_user": profile_user, "is_self": is_self, "is_friend": is_friend},
    )


@login_required
def add_friend(request, username):
    if request.method != "POST":
        raise PermissionDenied("Добавление в друзья доступно только через POST.")

    friend_user = get_object_or_404(User, username=username)
    if friend_user == request.user:
        raise PermissionDenied("Нельзя добавить себя в друзья.")

    request.user.friends.add(friend_user)
    return redirect("profile_detail", username=friend_user.username)


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile_me")
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})
