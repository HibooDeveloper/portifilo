#!/usr/bin/env bash
# scripts/deploy.sh — First-time VPS setup on Hostinger Ubuntu 24.04
set -euo pipefail

DOMAIN="${DOMAIN:-hibbo.tech}"
REPO_URL="${REPO_URL:-https://github.com/HibooDeveloper/portifilo.git}"
APP_DIR="/opt/portfolio"
BACKUP_DIR="/opt/backups"

echo "═══════════════════════════════════════"
echo "  Abubaker Portfolio — VPS Deploy"
echo "  Domain: $DOMAIN"
echo "  Repo:   $REPO_URL"
echo "═══════════════════════════════════════"

# ── System packages ────────────────────────────────────────────
echo "› Installing system packages..."
apt-get update -y
apt-get install -y curl git ufw fail2ban

# ── Docker (official installer — bundles the compose plugin) ────
# Ubuntu's docker-compose-plugin isn't always in the default repos, so use
# Docker's convenience script. Idempotent: skipped if docker is already present.
if ! command -v docker >/dev/null 2>&1; then
  echo "› Installing Docker Engine + Compose plugin..."
  curl -fsSL https://get.docker.com | sh
fi
docker compose version

# ── Firewall ──────────────────────────────────────────────────
echo "› Configuring firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# ── Fail2Ban ──────────────────────────────────────────────────
systemctl enable fail2ban --now

# ── Docker ────────────────────────────────────────────────────
systemctl enable docker --now
mkdir -p "$APP_DIR" "$BACKUP_DIR"

# ── Clone / update repo ────────────────────────────────────────
if [ -d "$APP_DIR/.git" ]; then
  echo "› Pulling latest changes..."
  cd "$APP_DIR" && git pull origin master
else
  echo "› Cloning repository..."
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

# ── Environment ────────────────────────────────────────────────
if [ ! -f .env ]; then
  echo "› Creating .env from template..."
  cp .env.example .env
  echo "⚠️  IMPORTANT: Edit .env with your real credentials!"
  echo "   nano $APP_DIR/.env"
  echo ""
  echo "   Required changes:"
  echo "   - SECRET_KEY          (generate: openssl rand -hex 32)"
  echo "   - JWT_SECRET_KEY      (generate: openssl rand -hex 32)"
  echo "   - DATABASE_URL        (set MySQL password)"
  echo "   - MYSQL_ROOT_PASSWORD (set root password)"
  echo "   - MYSQL_PASSWORD      (same as in DATABASE_URL)"
  echo "   - REDIS_PASSWORD      (set Redis password)"
  echo "   - MAIL_USERNAME       (your Gmail address)"
  echo "   - MAIL_PASSWORD       (your Gmail app password)"
  echo "   - FIELD_ENCRYPTION_KEY (python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\")"
  echo "   - CF_TURNSTILE_SECRET  (from Cloudflare dashboard)"
  echo ""
  read -rp "Press Enter after editing .env, or Ctrl+C to abort..."
fi

# ── Build & start services ────────────────────────────────────
# The stack self-bootstraps: nginx mints a temporary self-signed cert so it can
# start, the certbot service then obtains the real Let's Encrypt cert and nginx
# reloads automatically; the app container runs `db-init` on startup. So a plain
# build + up brings everything online.
echo "› Building images and starting all services..."
docker compose up -d --build
echo "› Waiting for services to settle (TLS issuance can take ~30-60s)..."
sleep 45

# ── Admin user ────────────────────────────────────────────────
# DB tables are created automatically by the app container; only the admin
# account needs an interactive step (password is never stored in code/env).
echo "› Creating admin user..."
docker exec -it portfolio_app python manage.py create-admin

echo ""
echo "═══════════════════════════════════════"
echo "  ✓ Deployment complete!"
echo "  Site:    https://$DOMAIN"
echo "  Health:  https://$DOMAIN/health"
echo "  Admin:   https://$DOMAIN"
echo ""
echo "  Next steps:"
echo "  1. Visit https://$DOMAIN and verify the site loads"
echo "  2. Login to admin panel with your admin credentials"
echo "  3. Set up automated backups: crontab -e"
echo "     0 2 * * * docker exec portfolio_db mysqldump -u root -p\$MYSQL_ROOT_PASSWORD portfolio_db > $BACKUP_DIR/db-\$(date +\%Y\%m\%d).sql"
echo "═══════════════════════════════════════"
