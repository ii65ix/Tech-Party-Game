from django.urls import path

from . import auth_views, views

app_name = "game"

urlpatterns = [
    path("accounts/register/", auth_views.register, name="register"),
    path("accounts/login/", auth_views.login_view, name="login"),
    path("accounts/logout/", auth_views.logout_view, name="logout"),
    path("accounts/profile/", auth_views.profile, name="profile"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("start/<slug:mode_slug>/", views.start_game, name="start_game"),
    path("play/", views.play, name="play"),
    path("feedback/", views.feedback, name="feedback"),
    path("result/", views.result, name="result"),
]
