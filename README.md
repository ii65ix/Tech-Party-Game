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

### Arabic & English (العربية والإنجليزية)

- Use the **language** dropdown in the navbar: **English** or **العربية** (stored in the session/cookie via Django’s `set_language`).
- **Questions** are stored twice in the database (`language=en` and `language=ar`) — 100 rows after `seed_questions`. The active UI language picks the matching set.
- **Interface strings** (buttons, menus, messages) are translated via `locale/ar/LC_MESSAGES/django.po`. Compile them with either:
  - `python manage.py compilemessages` (requires GNU **gettext** / `msgfmt`), or
  - `python compile_locale.py` (uses **polib**, no gettext — works on Windows out of the box).
  The `build.sh` script runs `compilemessages` when `msgfmt` exists; otherwise it runs `compile_locale.py` automatically.

---

## GitHub + GitHub Pages (مهم)

- **GitHub** مناسب جداً لرفع **كود المشروع** (`git push`) والنسخ الاحتياطي والتعاون.
- **GitHub Pages** يستضيف **مواقع ثابتة فقط** (HTML / CSS / JavaScript بدون سيرفر Python خلفها).  
  **لا يمكن تشغيل مشروع Django كامل** (قاعدة بيانات، تسجيل دخول، لوحة إدارة) على GitHub Pages لأنها لا تشغّل بايثون ولا Gunicorn.

إذا أردت **لعبة تعمل على الإنترنت** بنفس هذا المشروع (Django)، تحتاج خدمة **استضافة Python** تربطها بمستودع GitHub، مثل: **Railway**، **Fly.io**، **PythonAnywhere**، **Koyeb**، أو غيرها — وليس GitHub Pages.

**ملخص:** استخدم GitHub للمستودع، واستخدم أي منصة تدعم تطبيقات Python للنشر الفعلي.

---

## Deploy on Render (النشر على Render)

**GitHub Pages لا يشغّل Django** — استخدم **Render** (أو أي PaaS) لرفع التطبيق الحقيقي. المشروع جاهز لـ Render عبر `build.sh` و `Procfile` و `render.yaml`.

### طريقة سريعة (Blueprint)

1. ارفع المشروع إلى مستودع **GitHub**.
2. في [Render](https://render.com): **New** → **Blueprint** → اختر المستودع → Render يقرأ `render.yaml`.
3. يُنشأ **Web Service** + قاعدة **PostgreSQL** ويُربط `DATABASE_URL` تلقائياً.
4. بعد أول نشر ناجح، افتح **Shell** لخدمة الويب وشغّل مرة واحدة:
   ```bash
   python manage.py seed_questions
   python manage.py createsuperuser
   ```
   (`seed_questions` يملأ 100 سؤالاً بلغتين؛ يمكن إعادة تشغيله لإعادة الضبط.)

### طريقة يدوية (لوحة Render)

1. **New** → **PostgreSQL** — أنشئ قاعدة بيانات (احفظ الرابط أو اربطها لاحقاً).
2. **New** → **Web Service** — اربط نفس المستودع.
3. اضبط:
   - **Build command:** `chmod +x build.sh && ./build.sh`
   - **Start command:** `gunicorn tech_party_game.wsgi:application --bind 0.0.0.0:$PORT`
4. في **Environment** أضف:
   - `SECRET_KEY` — عشوائي طويل (أو استخدم Generate في Render).
   - `DEBUG` = `False`
   - `DATABASE_URL` — من قاعدة PostgreSQL (**Internal** أو **External** حسب ما يوصي Render).
5. Render يضيف تلقائياً `RENDER_EXTERNAL_HOSTNAME` — الإعدادات تستخدمه لـ `ALLOWED_HOSTS` ولـ **CSRF** على `https://اسم-الخدمة.onrender.com` دون أن تنسى `CSRF_TRUSTED_ORIGINS` يدوياً (يمكنك إضافة نطاقات إضافية في المتغير نفسه إن لزم).

### ملفات مهمة للنشر

| File | Purpose |
|------|---------|
| `build.sh` | تثبيت الحزم، ترجمة الواجهة (`compile_locale` أو gettext)، `collectstatic`، `migrate` |
| `Procfile` | تشغيل Gunicorn على `$PORT` |
| `render.yaml` | تعريف خدمة الويب + PostgreSQL (Blueprint) |

---

## Deploy Django (generic — أي منصة Python)

نفس فكرة البناء والتشغيل أعلاه يمكن استخدامها على Railway و Fly.io وغيرها:

1. اربط المستودع، أضف PostgreSQL و `DATABASE_URL`.
2. **Build:** `chmod +x build.sh && ./build.sh`
3. **Start:** `gunicorn tech_party_game.wsgi:application --bind 0.0.0.0:$PORT`
4. متغيرات: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`

بعد أول نشر:

```bash
python manage.py seed_questions
python manage.py createsuperuser
```

---

## Project layout

- `game/` — app code: models, views, auth, templates, static assets
- `game/management/commands/seed_questions.py` — loads 50 starter questions
- `tech_party_game/` — project settings and root URLconf
- `build.sh` — install deps, `collectstatic`, `migrate` (for PaaS deploys)
- `Procfile` — Gunicorn start command (if the platform reads it)

## Game flow

1. Optional display name + choose a mode.
2. Quiz and Bug Hunter show feedback with the correct answer highlighted.
3. `Score` rows store guest sessions or logged-in users.

## Customizing

- Edit questions in the admin, or change `seed_questions.py` and run `python manage.py seed_questions` (this **replaces** all questions).
