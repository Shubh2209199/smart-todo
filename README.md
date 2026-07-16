# Smart To-Do App

A Flask to-do list with login/register, an AI-style reminder & insights
engine, search & filtering, dark/light mode, and a mobile-responsive UI.

## ✨ Features

- 🔐 Login & registration (hashed passwords, CSRF-protected forms)
- ✅ Add / edit / delete / complete tasks with priority & due date+time
- 🤖 **AI Reminders** — banners for tasks due soon or overdue
- 🧠 **AI Insights** — completion rate, streaks, most productive time of
  day, high-priority nudges, etc. (rule-based, computed from your own
  task data — no external AI API or key required)
- 🔍 Search & filter by status/priority
- 🌙 Dark / light mode (persisted per user)
- 👤 Profile page with stats & password change
- 📱 Mobile-responsive layout
- 🚀 Ready to deploy with gunicorn (Render, Railway, Heroku, etc.)

## 📁 Project Structure

```
smart_todo/
├── app/
│   ├── __init__.py        # app factory
│   ├── config.py          # reads secrets from environment only
│   ├── extensions.py      # db, login_manager, csrf
│   ├── models.py          # User, Todo
│   ├── forms.py           # WTForms (CSRF + validation)
│   ├── ai_reminder.py     # AI reminder & insights engine
│   ├── routes/
│   │   ├── auth.py        # login/register/logout
│   │   ├── todos.py       # dashboard, CRUD, search/filter
│   │   ├── profile.py     # stats, password change, theme toggle
│   │   └── main.py        # about page
│   ├── templates/
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── requirements.txt
├── run.py                 # local dev entrypoint
├── wsgi.py                # production entrypoint (gunicorn wsgi:app)
├── Procfile                # for Render/Heroku
├── .env.example            # copy to .env locally — no real secrets in git
└── .gitignore
```

## 🖥️ Run locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then open .env and set SECRET_KEY to a random string, e.g.:
python -c "import secrets; print(secrets.token_hex(32))"

python run.py
```

Visit http://127.0.0.1:5000 — a local `instance/todo.db` SQLite file is
created automatically on first run.

## ☁️ Deploy (e.g. Render)

1. Push this project to a GitHub repo (`.env` and `instance/` are already
   git-ignored, so no secrets or local data get committed).
2. Create a new **Web Service** on Render pointing at the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn wsgi:app`
5. In the service's **Environment** settings, add:
   - `SECRET_KEY` — a long random string
   - `DATABASE_URL` — leave unset to keep using SQLite, or attach a
     Render Postgres database (its URL is provided automatically and
     the app fixes the `postgres://` → `postgresql://` scheme for you)

No secret values ever need to live in the code or in git — everything
sensitive is read from environment variables at runtime.

## 🔒 Security notes

- Passwords are hashed with Werkzeug's `generate_password_hash`.
- All state-changing forms (add/edit/delete/complete task, login,
  register, password change, theme toggle) are CSRF-protected via
  Flask-WTF.
- Session cookies are `HttpOnly`, `SameSite=Lax`, and `Secure` in
  production (`FLASK_ENV=production`).
