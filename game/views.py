import time

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .models import Category, Question, Score
from .utils import content_language

MODE_SLUGS = {"quiz", "bug", "funny"}
TIMER_SECONDS = {
    "quiz": 12,
    "bug": 25,
    "funny": 9999,
}


def home(request):
    categories = Category.objects.all()
    return render(
        request,
        "game/home.html",
        {"categories": categories},
    )


def about(request):
    return render(request, "game/about.html")


@require_http_methods(["POST"])
def start_game(request, mode_slug):
    if mode_slug not in MODE_SLUGS:
        messages.error(request, _("Unknown game mode."))
        return redirect("game:home")

    cat = Category.objects.filter(slug=mode_slug).first()
    if not cat:
        messages.error(request, _("Category not found. Run seed_questions."))
        return redirect("game:home")

    lang = content_language(request)
    qids = list(
        cat.questions.filter(language=lang).order_by("id").values_list("id", flat=True)
    )
    if not qids:
        messages.error(
            request,
            _("No questions for this mode in your language yet."),
        )
        return redirect("game:home")

    player_name = (request.POST.get("player_name") or "").strip()[:100]
    if not player_name and request.user.is_authenticated:
        u = request.user
        player_name = (u.get_full_name() or u.username or "")[:100]
    request.session["game"] = {
        "mode": mode_slug,
        "category_slug": mode_slug,
        "qids": qids,
        "idx": 0,
        "score": 0,
        "player_name": player_name,
        "question_shown_at": None,
    }
    request.session.pop("feedback", None)
    return redirect("game:play")


def _get_game(request):
    return request.session.get("game")


def _current_question(request):
    g = _get_game(request)
    if not g:
        return None, None
    idx = g["idx"]
    qids = g["qids"]
    if idx >= len(qids):
        return g, None
    q = Question.objects.filter(pk=qids[idx], category__slug=g["category_slug"]).first()
    return g, q


@require_http_methods(["GET", "POST"])
def play(request):
    g = _get_game(request)
    if not g:
        messages.warning(request, _("Start a game from the home page."))
        return redirect("game:home")

    if request.method == "GET":
        g, question = _current_question(request)
        if not question:
            return redirect("game:result")
        g["question_shown_at"] = time.time()
        request.session["game"] = g
        idx = g["idx"]
        total = len(g["qids"])
        timer = TIMER_SECONDS.get(g["mode"], 12)
        return render(
            request,
            "game/play.html",
            {
                "question": question,
                "progress_index": idx + 1,
                "progress_total": total,
                "progress_pct": int((idx / total) * 100) if total else 0,
                "timer_seconds": timer,
                "show_timer": g["mode"] != "funny",
                "game_mode": g["mode"],
            },
        )

    # POST — answer (or timer expiry)
    client_timeout = request.POST.get("timed_out") == "1"
    choice = (request.POST.get("choice") or "").upper().strip()

    g, question = _current_question(request)
    if not g or not question:
        return redirect("game:result")

    mode = g["mode"]
    timed_out = False
    if client_timeout:
        choice = ""
        timed_out = True
    elif choice not in {"A", "B", "C", "D"}:
        messages.error(request, _("Pick A, B, C, or D."))
        return redirect("game:play")
    elif g.get("question_shown_at") and mode != "funny":
        limit = TIMER_SECONDS.get(mode, 12)
        if time.time() - g["question_shown_at"] > limit:
            timed_out = True

    if mode == "funny":
        g["score"] += 1
        correct = True
    elif timed_out:
        correct = False
    else:
        correct = choice == question.correct_answer
        if correct:
            g["score"] += 1

    g["idx"] += 1
    g["question_shown_at"] = None
    request.session["game"] = g

    finished = g["idx"] >= len(g["qids"])

    if mode in ("quiz", "bug"):
        request.session["feedback"] = {
            "question_id": question.id,
            "user_choice": choice or ("—" if timed_out else ""),
            "correct_answer": question.correct_answer,
            "was_correct": correct,
            "timed_out": timed_out,
            "finished": finished,
        }
        return redirect("game:feedback")

    # Funny: no feedback screen
    if finished:
        return redirect("game:result")
    return redirect("game:play")


@require_http_methods(["GET", "POST"])
def feedback(request):
    g = _get_game(request)
    fb = request.session.get("feedback")
    if not g or not fb:
        return redirect("game:home")

    q = Question.objects.filter(pk=fb["question_id"]).first()
    if not q:
        request.session.pop("feedback", None)
        return redirect("game:result")

    if request.method == "POST":
        request.session.pop("feedback", None)
        if fb.get("finished"):
            return redirect("game:result")
        return redirect("game:play")

    return render(
        request,
        "game/feedback.html",
        {
            "question": q,
            "user_choice": fb["user_choice"],
            "correct_answer": fb["correct_answer"],
            "was_correct": fb["was_correct"],
            "timed_out": fb["timed_out"],
            "finished": fb["finished"],
            "game_mode": g["mode"],
        },
    )


def result(request):
    g = _get_game(request)
    if not g:
        messages.warning(request, _("No game in progress."))
        return redirect("game:home")

    total = len(g["qids"])
    score = g["score"]
    mode = g["mode"]
    player_name = g.get("player_name", "")

    Score.objects.create(
        user=request.user if request.user.is_authenticated else None,
        player_name=player_name,
        session_key=request.session.session_key or "",
        score=score,
        max_score=total,
        game_mode=mode,
    )

    request.session.pop("feedback", None)
    del request.session["game"]

    mode_labels = {
        "quiz": _("Quiz Mode"),
        "bug": _("Bug Hunter"),
        "funny": _("Who is Most Likely"),
    }

    return render(
        request,
        "game/result.html",
        {
            "score": score,
            "max_score": total,
            "mode": mode,
            "mode_label": mode_labels.get(mode, mode),
            "player_name": player_name,
            "percent": int((score / total) * 100) if total else 0,
            "home_url": reverse("game:home"),
        },
    )
