from django.core.management.base import BaseCommand

from game.data.questions_ar import DATA as DATA_AR
from game.data.questions_en import DATA as DATA_EN
from game.models import Category, Question


class Command(BaseCommand):
    help = "Seed categories and 100 questions (English + Arabic)."

    def handle(self, *args, **options):
        cats = {
            "quiz": "Quiz",
            "bug": "Bug Hunter",
            "funny": "Who is Most Likely",
        }
        for slug, name in cats.items():
            Category.objects.update_or_create(slug=slug, defaults={"name": name})

        Question.objects.all().delete()

        banks = {"en": DATA_EN, "ar": DATA_AR}
        total = 0
        for lang_code, data in banks.items():
            for slug, rows in data.items():
                cat = Category.objects.get(slug=slug)
                for text, a, b, c, d, correct in rows:
                    Question.objects.create(
                        language=lang_code,
                        text=text,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=correct,
                        category=cat,
                    )
                    total += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {total} questions ({len(banks)} languages × 50 questions)."
            )
        )
