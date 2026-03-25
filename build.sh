#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
if command -v msgfmt >/dev/null 2>&1; then
  python manage.py compilemessages
else
  python compile_locale.py
fi
python manage.py collectstatic --noinput
# Only touch the real DB when DATABASE_URL is set. Without it, migrate/seed would
# run against SQLite in the build container and NOT populate Postgres at runtime.
if [ -n "${DATABASE_URL:-}" ]; then
  python manage.py migrate --noinput
  python manage.py seed_questions
else
  echo "Skipping migrate/seed (DATABASE_URL unset). For local dev run: python manage.py migrate && python manage.py seed_questions"
fi
