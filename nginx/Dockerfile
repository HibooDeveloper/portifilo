# Custom nginx image: bakes in the site config + static assets so the stack has
# NO host bind-mounts (works with Hostinger's panel, which only stages the
# compose file). TLS certs still live in the shared certbot named volume.
FROM nginx:1.27-alpine

# openssl is needed by the entrypoint to mint a temporary self-signed cert.
RUN apk add --no-cache openssl

# Config + static assets baked into the image (build context = repo root).
COPY nginx/nginx.conf      /etc/nginx/nginx.conf
COPY nginx/portfolio.conf  /etc/nginx/conf.d/default.conf
COPY app/static            /app/static

COPY nginx/entrypoint.sh   /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
