# 🚀 Abubaker Hobeldeen — Portfolio Platform

**Software Engineer | Flutter | Python | AI Solutions | Cairo, Egypt**

A production-ready bilingual (Arabic/English) portfolio platform with a full Flask REST API backend.

---

## ✨ Features

| Category | Details |
|----------|---------|
| **Frontend** | Bilingual AR/EN, RTL/LTR, particle canvas hero, scroll animations |
| **Backend**  | Flask, SQLAlchemy, JWT auth, 2FA TOTP, rate limiting |
| **Database** | MySQL 8 with full ORM models |
| **Security** | Cloudflare WAF, Turnstile, Fail2Ban, bcrypt, encrypted fields |
| **DevOps**   | Docker, Nginx, GitHub Actions CI/CD, Let's Encrypt SSL |
| **Testing**  | Pytest, coverage, Bandit, Safety, Trivy |

---

## 🛠️ Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio
cp .env.example .env
# Edit .env with your credentials

# 2. Run with Docker
docker compose up -d

# 3. Initialize database + create admin
docker exec portfolio_app flask db upgrade
docker exec portfolio_app python manage.py create-admin

# 4. Visit
open http://localhost
```

## 📁 Project Structure

```
portfolio/
├── app/
│   ├── api/           # REST API blueprints
│   │   ├── auth.py    # JWT + 2FA + refresh tokens
│   │   ├── projects.py
│   │   ├── blogs.py
│   │   ├── services.py
│   │   ├── testimonials.py
│   │   ├── messages.py
│   │   ├── analytics.py
│   │   ├── media.py
│   │   └── users.py
│   ├── models/        # SQLAlchemy models
│   ├── services/      # Mail, notifications
│   ├── utils/         # Validators, RBAC, audit, Turnstile
│   ├── templates/     # Jinja2 / HTML
│   └── static/
│       └── js/
│           ├── translations.js   # AR/EN content
│           └── main.js           # Animations + render engine
├── config/
│   └── settings.py    # Dev / Staging / Production configs
├── tests/
│   ├── conftest.py
│   └── unit/
├── nginx/
│   ├── nginx.conf
│   └── portfolio.conf
├── scripts/
│   ├── deploy.sh
│   └── init.sql
├── .github/workflows/
│   └── deploy.yml     # CI/CD pipeline
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── wsgi.py
└── manage.py
```

## 🔐 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Register user | — |
| POST | `/api/auth/login` | Login + 2FA | — |
| POST | `/api/auth/refresh` | Refresh token | JWT Refresh |
| POST | `/api/auth/logout` | Revoke token | JWT Refresh |
| GET  | `/api/auth/me` | Current user | JWT |
| POST | `/api/auth/2fa/setup` | Setup TOTP | JWT |
| POST | `/api/auth/2fa/verify` | Verify + enable 2FA | JWT |
| GET  | `/api/projects/` | List projects | — |
| GET  | `/api/projects/<slug>` | Project detail | — |
| POST | `/api/projects/` | Create project | Admin |
| PUT  | `/api/projects/<id>` | Update project | Admin/Editor |
| DELETE | `/api/projects/<id>` | Delete project | Super Admin |
| GET  | `/api/blogs/` | List posts | — |
| POST | `/api/blogs/` | Create post | Admin/Editor |
| GET  | `/api/messages/` | List messages | Admin |
| POST | `/api/messages/` | Submit contact | — |
| GET  | `/api/analytics/dashboard` | Analytics | Admin |
| POST | `/api/analytics/track` | Track event | — |
| GET  | `/api/media/` | List media | Admin |
| POST | `/api/media/upload` | Upload file | Admin |

## 🧪 Testing

```bash
pytest tests/ -v --cov=app
bandit -r app/
safety check
```

## 🚀 Production Deployment (Hostinger VPS)

```bash
# Run deployment script on fresh Ubuntu 24.04 VPS
curl -fsSL https://raw.githubusercontent.com/YOUR/portfolio/main/scripts/deploy.sh | bash
```

---

Built with ❤️ by **Abubaker Hobeldeen Suliman** — Cairo, Egypt
