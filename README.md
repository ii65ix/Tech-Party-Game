# Tech Party Game

A Django web game with three modes: **Quiz** (timed multiple choice), **Bug Hunter** (broken code snippets), and **Who is Most Likely** (fun tech prompts). Includes **user accounts** (sign up, log in, profile with score history), a dark UI with Bootstrap 5, custom CSS animations, and session-based play.

## Requirements

- Python 3.10 or newer
- pip

## Local setup

```bash
cd game.py
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_questions
python manage.py createsuperuser
python manage.py runserver
```

Open **http://127.0.0.1:8000/** for the game and **http://127.0.0.1:8000/admin/** to manage categories, questions, and scores.

### Accounts

- **Sign up** — `/accounts/register/`
- **Log in** — `/accounts/login/`
- **Profile** (recent scores) — `/accounts/profile/` (requires login)
- **Log out** — POST from the navbar

If you are logged in, your display name on the home page defaults to your name/username and scores are saved to your user.

---

## Deploy on Render (النشر على Render)

1. Push this project to **GitHub**.
2. In [Render](https://render.com), create a **PostgreSQL** database (free tier is fine).
3. Create a **Web Service** from the same repo:
   - **Build command:** `chmod +x build.sh && ./build.sh`
   - **Start command:** `gunicorn tech_party_game.wsgi:application --bind 0.0.0.0:$PORT`
4. In the web service **Environment** tab, add:
   - `SECRET_KEY` — long random string (Render can generate one).
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = your Render hostname, e.g. `myapp.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://myapp.onrender.com` (use your real URL, with `https://`)
   - `DATABASE_URL` — paste the **Internal Database URL** from the PostgreSQL instance (Render often fills this when you link the DB).
5. After the first successful deploy, open **Shell** on the web service and run:

   ```bash
   python manage.py seed_questions
   python manage.py createsuperuser
   ```

   (`seed_questions` replaces all questions in the DB — run once after first deploy.)

**ملخص:** اربط قاعدة بيانات PostgreSQL على Render، عيّن المتغيرات أعلاه، واستخدم أوامر البناء والتشغيل المذكورة. بعد النشر شغّل `seed_questions` مرة واحدة ثم أنشئ حساب مدير من `createsuperuser`.

---

## Project layout

- `game/` — app code: models, views, auth, templates, static assets
- `game/management/commands/seed_questions.py` — loads 50 starter questions
- `tech_party_game/` — project settings and root URLconf
- `build.sh` — install deps, `collectstatic`, `migrate` (for Render)
- `Procfile` — Gunicorn command (optional if you set start command in the dashboard)

## Game flow

1. Optional display name + choose a mode.
2. Quiz and Bug Hunter show feedback with the correct answer highlighted.
3. `Score` rows store guest sessions or logged-in users.

## Customizing

- Edit questions in the admin, or change `seed_questions.py` and run `python manage.py seed_questions` (this **replaces** all questions).
# Tech-Party-Game
# Tech-Party-Game
# Tech-Party-Game
# Tech-Party-Game
