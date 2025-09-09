# Hostinger (hPanel) — GUI deploy & auto-deploy via GitHub Actions

This document shows the GUI-only steps to connect this repository to Hostinger and enable automatic deploys using the GitHub Action `trigger-hostinger.yml` already present in `.github/workflows/`.

Summary
- Add Hostinger deploy server's SSH public key as a Deploy Key on this GitHub repo (so Hostinger can clone the private repo).
- Configure Hostinger Git repository to deploy to a folder (for example `/home/<user>/public_html`).
- Copy the Hostinger deploy webhook URL and save it as the `HOSTINGER_DEPLOY_URL` Actions secret in GitHub.
- Trigger an initial deploy from the hPanel UI and then verify the GitHub Action auto-deploy.

Step 1 — Add Hostinger SSH public key to GitHub (Deploy key)
1. In hPanel: open the server account where the repo will be deployed and find the SSH public key used by hPanel Git (Web Terminal → `cat ~/.ssh/id_ed25519.pub` or the SSH keys view in hPanel).
2. GitHub → this repo → Settings → Deploy keys → Add deploy key.
   - Title: `Hostinger hPanel` (or similar)
   - Key: paste the public key from hPanel
   - Leave "Allow write access" unchecked (not required for deploy)
3. Click Add key.

Step 2 — Create the Git repository entry in hPanel (GUI)
1. hPanel → Files → Git Repositories → Create repository → Choose "Clone from remote".
2. Repository URL: use the SSH URL (git@github.com:apurbaone/portfolio-python.git).
3. Branch: `main`.
4. Deploy path: pick the target (for example `/home/<your-hpanel-user>/public_html` or `/home/<your>/portfolio-python`).
5. Click Deploy. Wait for the initial clone to finish.

Step 3 — Copy Hostinger webhook and add GitHub secret
1. In hPanel → Files → Git Repositories → open the repository entry. Look for "Deploy webhook" or "Auto-deploy". Click "Show webhook" and copy the webhook URL (it looks like `https://webhooks.hostinger.com/deploy/<token>`).
2. GitHub → your repo → Settings → Secrets and variables → Actions → New repository secret
   - Name: `HOSTINGER_DEPLOY_URL`
   - Value: paste the webhook URL you copied from hPanel
   - Save.

Note: if Hostinger's webhook UI shows a header/token requirement (e.g. `X-Deploy-Token`), create an additional secret (for example `HOSTINGER_DEPLOY_TOKEN`) and tell the workflow to send it. The current workflow supports only the webhook URL; if Hostinger requires a header, ask me to update the workflow.

Step 4 — Verify auto-deploy using GitHub Actions
1. The repo already contains `.github/workflows/trigger-hostinger.yml`. When you push to `main` the Action will run quick checks and POST the webhook URL stored in `HOSTINGER_DEPLOY_URL`.
2. Trigger a push: edit a small file via GitHub web (e.g., `README.md`) and commit to `main`.
3. GitHub → Actions → open the latest workflow run. Under job `trigger-deploy` inspect the logs for the "Trigger Hostinger deploy webhook" step — it should show a successful POST and "Webhook POSTed".

Step 5 — Finish server-side steps (hPanel GUI)
1. hPanel → Files → File Manager → navigate to the deploy path. Confirm `manage.py`, `portfolio_site/`, `static/` are present.
2. Configure environment variables:
   - Preferred: hPanel → Advanced → Python Apps → select the app → Environment Variables
     - SECRET_KEY (a long random string)
     - DEBUG = False
     - ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com
   - If Python App UI is not available: File Manager → create `.env` in project root and paste the variables (do not commit `.env`).
3. Run server-side commands:
   - If the Python App UI provides a command console, run:
     - `python manage.py migrate --noinput`
     - `python manage.py collectstatic --noinput`
   - Otherwise use hPanel Cron Jobs to run `bash scripts/hostinger_deploy.sh` once (the repo contains that script).
4. Ensure `media/` exists and is writable (File Manager → create `media` if missing → set owner write permissions).
5. Restart the app: either use the Python App "Restart" button or create `tmp/restart.txt` in the project root to trigger Passenger reload.

Troubleshooting
- If the GitHub Action step returns curl exit code 22 (HTTP 4xx/5xx): open the Action logs and the Hostinger Deploy log. Common issues:
  - 403: wrong webhook URL or missing token/header. Recopy webhook from hPanel and set `HOSTINGER_DEPLOY_URL`.
  - 404: webhook not found — copy the correct URL; do not use GitHub settings URLs.
- If hPanel deploy logs show Git clone auth errors, re-check the Deploy key added to GitHub.
- If static files are missing, confirm `python manage.py collectstatic` ran successfully and `STATIC_ROOT` is correct.

If you want, I can:
- Update the workflow to send an auth header if Hostinger requires one (you would add the token as a secret), or
- Add a short `docs/hostinger-troubleshoot.md` extracting the exact error messages and fixes.

Done — this file is tracked in `docs/hostinger.md` in the repository.
