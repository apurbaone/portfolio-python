# Deploy & GitHub push

This guide shows exact commands to push the project to GitHub from Windows PowerShell and a compact checklist to deploy the app from GitHub to a Hostinger server.

---

## 1) Push the local project to your GitHub repo (PowerShell)

Run these from your project root (C:\wamp64\www\Portfolio\new-app-for-me):

```powershell
# activate virtualenv (optional)
.\.venv\Scripts\Activate

# ensure .gitignore exists and sensitive files are excluded (e.g. .env)
git status

git add .
git commit -m "Import project"

# if you didn't set remote yet (you already added it in your snippet), set it now:
# git remote add origin https://github.com/<your-user>/<your-repo>.git

# push to main
git branch -M main
git push -u origin main
```

Notes:
- Remove secrets (SECRET_KEY, email credentials) from files before pushing. Use environment variables or a `.env` excluded by `.gitignore`.
- If your repository already contains a README commit (as in your snippet), running `git add .` and `git push` will sync the rest of the files.

---

## 2) Quick Hostinger deploy (SSH) — recommended if you have SSH access

1. SSH into the Hostinger account (get credentials from hPanel):

```bash
ssh <user>@<your-hostinger-ip-or-hostname>
```

2. Clone the repo and enter the folder:

```bash
cd ~
git clone https://github.com/<your-user>/<your-repo>.git
cd <your-repo>
```

3. Create and activate a virtualenv, install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

4. Set environment variables (example using a `.env` file or export):

```bash
export DJANGO_SETTINGS_MODULE=portfolio_site.settings
export SECRET_KEY='change-me'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com'
# and email env vars if needed
```

5. Prepare the Django project:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # run once interactively if needed
```

6. Run with Gunicorn (temporary test):

```bash
gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:8000
```

Then configure the Hostinger web panel to proxy the HTTP(S) requests to this port or set up a systemd service and Nginx reverse proxy. Hostinger's hPanel often provides a "Python app" or Git-deploy feature that simplifies these steps.

---

## 3) Hostinger hPanel (Git deployment) — easier, no SSH steps

1. In Hostinger hPanel, look for "Git" or "Python Apps".
2. Add a new Git deployment and point it to your GitHub repo and branch (`main`).
3. In Python app settings, set the path to your project and configure the entry point as `portfolio_site.wsgi:application` (or follow Hostinger UI guidance).
4. Provide environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB settings).
5. Run `pip install -r requirements.txt` via the panel or SSH and run migrations/collectstatic as above.

---

## 4) Serving static & media files

- For static files, set `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` in `settings.py` (or use Hostinger's `public_html/static`).
- Run `python manage.py collectstatic` to populate `STATIC_ROOT` and configure the web server to serve it.
- For user uploads (`MEDIA_ROOT`), configure the server to serve `/media/` from the `media/` directory.

Security note

- Do not commit `.env` or secrets to GitHub. Use Hostinger's environment variable UI or a `.env` file listed in `.gitignore`.

If you want, I can:
- Create a small `systemd` service file or a `Procfile` for Gunicorn.
- Add WhiteNoise to serve static files (quick fix) and update `requirements.txt`.
- Run the local git commit & push commands here (if you want me to run them). 

Tell me which of the above you'd like me to do next.
