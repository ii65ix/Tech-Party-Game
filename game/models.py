from django.conf import settings
from django.db import models


class Category(models.Model):
    """Quiz, Bug Hunter, or Who is Most Likely."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    class Meta:
        ordering = ["id"]

    @property
    def options_list(self):
        return [
            ("A", self.option_a),
            ("B", self.option_b),
            ("C", self.option_c),
            ("D", self.option_d),
        ]

    def __str__(self):
        return self.text[:80]


class Score(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tech_party_scores",
    )
    player_name = models.CharField(max_length=100, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    score = models.IntegerField()
    max_score = models.IntegerField(default=0)
    game_mode = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.player_name or self.user or 'Guest'} — {self.score}/{self.max_score}"
