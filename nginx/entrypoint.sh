#!/bin/sh
# nginx entrypoint — lets nginx start before Let's Encrypt has issued a cert.
#
# 1. If no certificate exists yet, mint a temporary self-signed one so nginx's
#    SSL server block can load (otherwise nginx refuses to start).
# 2. Run a background watcher that reloads nginx within ~60s of the cert file
#    changing — i.e. when the certbot container swaps the self-signed cert for
#    the real one, or when it renews. This is what makes auto-renewal effective.
set -e

DOMAIN="${DOMAIN:-hibbo.tech}"
CERT_DIR="/etc/letsencrypt/live/$DOMAIN"
CERT="$CERT_DIR/fullchain.pem"

if [ ! -f "$CERT" ]; then
  echo "[nginx] No certificate found — generating a temporary self-signed cert for $DOMAIN"
  mkdir -p "$CERT_DIR"
  openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
    -keyout "$CERT_DIR/privkey.pem" \
    -out    "$CERT" \
    -subj   "/CN=$DOMAIN" 2>/dev/null
fi

# Background: reload nginx when the certificate changes.
(
  last=""
  while :; do
    sleep 60
    cur=$(sha1sum "$CERT" 2>/dev/null | awk '{print $1}')
    if [ -n "$cur" ] && [ "$cur" != "$last" ]; then
      if [ -n "$last" ]; then
        echo "[nginx] certificate changed — reloading"
        nginx -s reload 2>/dev/null || true
      fi
      last="$cur"
    fi
  done
) &

exec nginx -g 'daemon off;'
