#!/usr/bin/env bash
# scripts/init-letsencrypt.sh
# First-time Let's Encrypt bootstrap for the nginx + certbot docker-compose stack.
#
# Solves the chicken-and-egg problem: nginx's config references a certificate
# that does not exist on a fresh box (so nginx can't start), but certbot's
# --webroot challenge needs nginx already serving port 80.
#
# Flow:
#   1. Write a throwaway self-signed cert into the certbot_conf VOLUME so nginx
#      can boot and serve the ACME HTTP-01 challenge on port 80.
#   2. Start nginx (and its deps).
#   3. Delete the dummy cert and request the real one via --webroot.
#   4. Reload nginx so it serves the real certificate.
#
# Both nginx and certbot share the certbot_conf / certbot_www NAMED volumes in
# docker-compose.yml, so everything lands where nginx expects it.
set -euo pipefail

DOMAIN="${DOMAIN:-hibbo.tech}"
EMAIL="${EMAIL:-admin@hibbo.tech}"
# Set STAGING=1 to use Let's Encrypt's staging CA while testing (avoids rate limits).
STAGING="${STAGING:-0}"

COMPOSE="docker compose"
live_path="/etc/letsencrypt/live/$DOMAIN"

echo "═══════════════════════════════════════"
echo "  Let's Encrypt bootstrap"
echo "  Domain:  $DOMAIN  (+ www.$DOMAIN)"
echo "  Email:   $EMAIL"
echo "  Staging: $STAGING"
echo "═══════════════════════════════════════"

echo "› [1/4] Creating temporary self-signed certificate so nginx can start..."
$COMPOSE run --rm --entrypoint "\
  sh -c 'mkdir -p $live_path && \
  openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
    -keyout $live_path/privkey.pem \
    -out    $live_path/fullchain.pem \
    -subj   /CN=localhost'" certbot

echo "› [2/4] Starting nginx (serves the ACME challenge on port 80)..."
$COMPOSE up -d nginx

echo "› [3/4] Removing dummy cert and requesting the real certificate..."
$COMPOSE run --rm --entrypoint "\
  rm -rf /etc/letsencrypt/live/$DOMAIN \
         /etc/letsencrypt/archive/$DOMAIN \
         /etc/letsencrypt/renewal/$DOMAIN.conf" certbot

staging_arg=""
if [ "$STAGING" != "0" ]; then staging_arg="--staging"; fi

$COMPOSE run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    --email $EMAIL --agree-tos --no-eff-email \
    --rsa-key-size 4096 --force-renewal \
    -d $DOMAIN -d www.$DOMAIN" certbot

echo "› [4/4] Reloading nginx with the real certificate..."
$COMPOSE exec nginx nginx -s reload

echo ""
echo "✓ Certificate installed for $DOMAIN and www.$DOMAIN."
echo "  Auto-renewal runs via the 'certbot' service (renew loop every 12h);"
echo "  nginx reloads itself every 6h to pick up renewed certs."
