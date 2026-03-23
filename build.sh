#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
if command -v msgfmt >/dev/null 2>&1; then
  python manage.py compilemessages
else
  python compile_locale.py
fi
python manage.py collectstatic --noinput
python manage.py migrate
