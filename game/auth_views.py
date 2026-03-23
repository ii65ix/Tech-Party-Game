from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm
from .models import Score


def _safe_next(request, default="/"):
    n = request.POST.get("next") or request.GET.get("next")
    if n and url_has_allowed_host_and_scheme(
        url=n,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return n
    return default


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("game:home")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome!")
            return redirect("game:home")
    else:
        form = SignUpForm()
    return render(request, "game/register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("game:home")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(_safe_next(request))
    else:
        form = AuthenticationForm()
    return render(request, "game/login.html", {"form": form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect("game:home")
    return redirect("game:home")


@login_required
def profile(request):
    scores = Score.objects.filter(user=request.user)[:100]
    return render(request, "game/profile.html", {"scores": scores})
