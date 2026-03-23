from django.contrib import admin

from .models import Category, Question, Score

admin.site.site_header = "Tech Party Game"
admin.site.site_title = "Tech Party Admin"
admin.site.index_title = "Manage questions and scores"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text_preview", "category", "language", "correct_answer")
    list_filter = ("category", "language")
    search_fields = ("text", "option_a", "option_b")

    @admin.display(description="Question")
    def text_preview(self, obj):
        return (obj.text[:60] + "…") if len(obj.text) > 60 else obj.text


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("player_name", "user", "score", "max_score", "game_mode", "created_at")
    list_filter = ("game_mode", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("player_name", "session_key")
