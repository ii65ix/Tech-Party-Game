# Generated manually for bilingual questions

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("ar", "Arabic")],
                db_index=True,
                default="en",
                max_length=5,
            ),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(
                fields=["category", "language"],
                name="game_question_cat_lang_idx",
            ),
        ),
    ]
