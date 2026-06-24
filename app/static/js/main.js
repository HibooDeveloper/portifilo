// ============================================================
// main.js — Portfolio interactivity & bilingual engine
// Abubaker Hobeldeen Suliman — Portfolio
// ============================================================

'use strict';

// ─── State ───────────────────────────────────────────────────
let currentLang = 'ar';
let currentFilter = 'all';
let typingTimer = null;
let typingRI = 0, typingCI = 0, typingDel = false;

// ─── Mobile Menu Toggle ──────────────────────────────────────
function toggleMenu() {
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');
  const open = hamburger.classList.toggle('open');
  navLinks.classList.toggle('open', open);
  hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
}

// Close menu when a nav link is clicked
document.addEventListener('click', function(e) {
  if (e.target.closest('#navLinks a')) {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    if (hamburger && navLinks) {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  }
});

// ─── Particle Canvas ─────────────────────────────────────────
(function initCanvas() {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;
  // Respect users who prefer reduced motion — skip the animation entirely.
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const ctx = canvas.getContext('2d');
  let W, H, particles = [];
  let rafId = null, running = false;
  const mouse = { x: -9999, y: -9999 };
  // Fewer particles on small screens to save battery/CPU.
  const PARTICLE_COUNT = window.innerWidth < 600 ? 35 : 75;

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.vx = (Math.random() - 0.5) * 0.28;
      this.vy = (Math.random() - 0.5) * 0.28;
      this.r = Math.random() * 1.4 + 0.4;
      this.a = Math.random() * 0.55 + 0.08;
    }
    update() {
      this.x += this.vx; this.y += this.vy;
      if (this.x < 0 || this.x > W) this.vx *= -1;
      if (this.y < 0 || this.y > H) this.vy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(37,99,235,${this.a})`;
      ctx.fill();
    }
  }

  function initParticles() {
    particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());
  }

  function drawConnections() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const d = Math.sqrt(dx * dx + dy * dy);
        if (d < 115) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(37,99,235,${0.14 * (1 - d / 115)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
      const dx = particles[i].x - mouse.x;
      const dy = particles[i].y - mouse.y;
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < 95) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.strokeStyle = `rgba(6,182,212,${0.28 * (1 - d / 95)})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }

  function animate() {
    rafId = requestAnimationFrame(animate);
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => { p.update(); p.draw(); });
    drawConnections();
  }

  function start() {
    if (running) return;
    running = true;
    animate();
  }
  function stop() {
    running = false;
    if (rafId) cancelAnimationFrame(rafId);
    rafId = null;
  }

  canvas.addEventListener('mousemove', e => {
    const r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left;
    mouse.y = e.clientY - r.top;
  });

  resize();
  initParticles();
  start();
  window.addEventListener('resize', () => { resize(); initParticles(); });

  // Pause the loop whenever the hero scrolls out of view or the tab is hidden.
  const hero = document.getElementById('hero');
  if (hero && 'IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      entries[0].isIntersecting ? start() : stop();
    }, { threshold: 0 }).observe(hero);
  }
  document.addEventListener('visibilitychange', () => {
    document.hidden ? stop() : start();
  });
})();

// ─── Typing Effect ────────────────────────────────────────────
function typeEffect() {
  const roles = TRANSLATIONS[currentLang].roles;
  const cur = roles[typingRI];
  const el = document.getElementById('typed-role');
  if (!el) return;

  if (!typingDel) {
    el.textContent = cur.slice(0, typingCI + 1);
    typingCI++;
    if (typingCI === cur.length) {
      typingDel = true;
      typingTimer = setTimeout(typeEffect, 1900);
      return;
    }
  } else {
    el.textContent = cur.slice(0, typingCI - 1);
    typingCI--;
    if (typingCI === 0) {
      typingDel = false;
      typingRI = (typingRI + 1) % roles.length;
    }
  }
  typingTimer = setTimeout(typeEffect, typingDel ? 55 : 85);
}

// ─── Scroll Reveal ────────────────────────────────────────────
let revealObserver = null;
function observe() {
  if (revealObserver) revealObserver.disconnect();
  const els = document.querySelectorAll('.reveal:not(.visible)');
  revealObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        revealObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.1 });
  els.forEach(el => revealObserver.observe(el));
}

// ─── Skill Bars ───────────────────────────────────────────────
let skillObserver = null;
function initSkillBars() {
  const sg = document.getElementById('skillsGrid');
  if (!sg) return;
  if (skillObserver) skillObserver.disconnect();
  skillObserver = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.skill-bar').forEach(bar => {
          bar.style.width = bar.dataset.pct + '%';
        });
        skillObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.25 });
  skillObserver.observe(sg);
}

// ─── Render Functions ─────────────────────────────────────────
function renderTimeline(t) {
  const el = document.getElementById('timeline');
  if (!el) return;
  el.innerHTML = t.timeline.map(item => `
    <div class="tl-item">
      <div class="tl-dot" ${item.accent ? 'style="background:var(--cyan)"' : ''}></div>
      <div>
        <div class="tl-year">${item.year}</div>
        <div class="tl-desc">${item.desc}</div>
        <div class="tl-sub">${item.sub}</div>
      </div>
    </div>`).join('');
}

function renderSkills(t) {
  const el = document.getElementById('skillsGrid');
  if (!el) return;
  el.innerHTML = t.skills.map((s, i) => `
    <div class="skill-card reveal" style="transition-delay:${i * 0.06}s">
      <div class="skill-icon">${s.icon}</div>
      <div class="skill-name">${s.name}</div>
      <div class="skill-bar-wrap">
        <div class="skill-bar" data-pct="${s.pct}" style="width:0%"></div>
      </div>
      <div class="skill-pct">${s.pct}%</div>
    </div>`).join('');
}

function renderServices(t) {
  const el = document.getElementById('servicesGrid');
  if (!el) return;
  el.innerHTML = t.services.map((s, i) => `
    <div class="svc-card reveal" style="transition-delay:${i * 0.07}s">
      <div class="svc-icon">${s.icon}</div>
      <div class="svc-name">${s.name}</div>
      <div class="svc-desc">${s.desc}</div>
      <div class="svc-tags">${s.tags.map(tag => `<span class="s-tag">${tag}</span>`).join('')}</div>
    </div>`).join('');
}

function renderProjects(filter) {
  currentFilter = filter;
  const t = TRANSLATIONS[currentLang];

  // Filters
  const pfWrap = document.getElementById('pfWrap');
  if (pfWrap) {
    pfWrap.innerHTML = t.pfFilters.map(f => `
      <button class="pf-btn ${f.val === filter ? 'active' : ''}"
        onclick="filterProjects('${f.val}',this)">${f.label}</button>`).join('');
  }

  // Cards
  const pg = document.getElementById('projectsGrid');
  if (!pg) return;
  const filtered = filter === 'all' ? t.projects : t.projects.filter(p => p.cat === filter);
  pg.innerHTML = filtered.map((p, i) => `
    <div class="proj-card reveal" style="transition-delay:${i * 0.08}s">
      <div class="proj-thumb">
        ${p.emoji}
        <div class="proj-badge">${p.badge}</div>
      </div>
      <div class="proj-body">
        <div class="proj-name">${p.name}</div>
        <div class="proj-desc">${p.desc}</div>
        <div class="proj-techs">${p.tech.map(tc => `<span class="tech-pill">${tc}</span>`).join('')}</div>
        <div class="proj-links">
          <a class="proj-link" href="#">${t.projDemo}</a>
          <a class="proj-link" href="#">${t.projGit}</a>
          <a class="proj-link" href="#">${t.projCase}</a>
        </div>
      </div>
    </div>`).join('');
  observe();
}

function filterProjects(val, btn) {
  document.querySelectorAll('.pf-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderProjects(val);
}

function renderAICards(t) {
  const el = document.getElementById('aiCards');
  if (!el) return;
  el.innerHTML = t.aiCards.map(c => `
    <div class="ai-card">
      <div class="ai-card-icon">${c.icon}</div>
      <div class="ai-card-name">${c.name}</div>
      <div class="ai-card-desc">${c.desc}</div>
    </div>`).join('');
}

function renderTestimonials(t) {
  const el = document.getElementById('testiGrid');
  if (!el) return;
  el.innerHTML = t.testimonials.map((item, i) => `
    <div class="testi-card reveal" style="transition-delay:${i * 0.1}s">
      <div class="testi-quote">"</div>
      <div class="testi-text">${item.text}</div>
      <div class="testi-author">
        <div class="testi-avatar" style="background:${item.color}">${item.avatar}</div>
        <div>
          <div class="testi-name">${item.name}</div>
          <div class="testi-role">${item.role}</div>
          <div class="stars">${'★'.repeat(item.stars)}</div>
        </div>
      </div>
    </div>`).join('');
}

function renderBlog(t) {
  const el = document.getElementById('blogGrid');
  if (!el) return;
  el.innerHTML = t.blogs.map((b, i) => `
    <div class="blog-card reveal" style="transition-delay:${i * 0.1}s">
      <div class="blog-thumb" style="background:linear-gradient(135deg,#EFF6FF,#DBEAFE)">${b.emoji}</div>
      <div class="blog-body">
        <div class="blog-cat">${b.cat}</div>
        <div class="blog-title">${b.title}</div>
        <div class="blog-excerpt">${b.excerpt}</div>
        <div class="blog-meta">
          <span>${b.date} · ${b.read}</span>
          <a class="blog-read" href="#">${t.readMore}</a>
        </div>
      </div>
    </div>`).join('');
}

// ─── Language Switcher ────────────────────────────────────────
function setLang(lang) {
  currentLang = lang;
  const t = TRANSLATIONS[lang];
  const html = document.documentElement;
  const body = document.getElementById('mainBody');

  html.setAttribute('lang', lang);
  html.setAttribute('dir', t.dir);
  body.className = t.dir === 'rtl' ? 'rtl' : 'ltr';

  // Logo
  const logo = document.getElementById('logo');
  if (logo) logo.innerHTML = t.logoHTML;

  // Nav items
  document.querySelectorAll('[data-ar]').forEach(el => {
    el.textContent = lang === 'ar' ? el.dataset.ar : el.dataset.en;
  });

  // Hero
  setText('heroBadge', `<span class="badge-dot"></span>${t.heroBadge}`, true);
  setText('heroHead', t.heroHead, true);
  setText('heroSub', t.heroSub);
  setText('btnProj', t.btnProj);
  setText('btnContact', t.btnContact);
  setText('s1', t.s1); setText('s2', t.s2); setText('s3', t.s3);
  setText('fb2', t.fb2);

  // About
  setText('aboutRole', t.aboutRole);
  setText('availText', t.availText);
  setText('projCount', t.projCount);
  setText('freeTxt', t.freeTxt);
  setText('aboutLabel', t.aboutLabel);
  setText('aboutTitle', t.aboutTitle, true);
  setText('aboutP1', t.aboutP1);
  setText('aboutP2', t.aboutP2);
  renderTimeline(t);

  // Skills
  setText('skillsLabel', t.skillsLabel);
  setText('skillsTitle', t.skillsTitle);
  setText('skillsSub', t.skillsSub);
  renderSkills(t);

  // Services
  setText('svcLabel', t.svcLabel);
  setText('svcTitle', t.svcTitle);
  setText('svcSub', t.svcSub);
  renderServices(t);

  // Projects
  setText('projLabel', t.projLabel);
  setText('projTitle', t.projTitle);
  setText('projSub', t.projSub);
  renderProjects(currentFilter);

  // AI
  setText('aiLabel', t.aiLabel);
  setText('aiTitle', t.aiTitle, true);
  setText('aiSub', t.aiSub);
  setText('userLbl', t.userLbl);
  setText('aiLbl', t.aiLbl);
  setText('chatUser', t.chatUser);
  setText('chatAI', t.chatAI, true);
  renderAICards(t);

  // Testimonials
  setText('testiLabel', t.testiLabel);
  setText('testiTitle', t.testiTitle);
  renderTestimonials(t);

  // Blog
  setText('blogLabel', t.blogLabel);
  setText('blogTitle', t.blogTitle);
  setText('blogAll', t.blogAll);
  renderBlog(t);

  // Contact
  setText('contactLabel', t.contactLabel);
  setText('contactTitle', t.contactTitle);
  setText('contactSub', t.contactSub);
  setText('cEmail', t.cEmail); setText('cWA', t.cWA);
  setText('cLoc', t.cLoc); setText('cLocVal', t.cLocVal);
  setText('formTitle', t.formTitle);
  setText('lName', t.lName); setText('lEmail', t.lEmail);
  setText('lPhone', t.lPhone); setText('lMsg', t.lMsg);
  setPlaceholder('iName', t.iName); setPlaceholder('iEmail', t.iEmail);
  setPlaceholder('iPhone', t.iPhone); setPlaceholder('iMsg', t.iMsg);
  setText('submitBtn', t.submitBtn);

  // Footer
  setText('footerMain', t.footerMain, true);
  setText('footerSub', t.footerSub);

  // Lang button states
  const btnEn = document.getElementById('btnEn');
  const btnAr = document.getElementById('btnAr');
  btnEn.classList.toggle('active', lang === 'en');
  btnAr.classList.toggle('active', lang === 'ar');
  btnEn.setAttribute('aria-pressed', lang === 'en' ? 'true' : 'false');
  btnAr.setAttribute('aria-pressed', lang === 'ar' ? 'true' : 'false');

  // Restart typing
  if (typingTimer) clearTimeout(typingTimer);
  typingRI = 0; typingCI = 0; typingDel = false;
  const typedEl = document.getElementById('typed-role');
  if (typedEl) typedEl.textContent = '';
  typeEffect();

  observe();
  setTimeout(initSkillBars, 400);
}

// ─── Helpers ──────────────────────────────────────────────────
function setText(id, value, html = false) {
  const el = document.getElementById(id);
  if (!el) return;
  if (html) el.innerHTML = value;
  else el.textContent = value;
}

function setPlaceholder(id, value) {
  const el = document.getElementById(id);
  if (el) el.placeholder = value;
}

// ─── Contact Form ─────────────────────────────────────────────
async function handleSubmit() {
  const t = TRANSLATIONS[currentLang];
  const btn = document.getElementById('submitBtn');
  if (!btn || btn.disabled) return;

  const name = document.getElementById('iName')?.value.trim();
  const email = document.getElementById('iEmail')?.value.trim();
  const phone = document.getElementById('iPhone')?.value.trim();
  const msg = document.getElementById('iMsg')?.value.trim();
  if (!name || !email || !msg) {
    btn.textContent = t.submitRequired;
    btn.style.background = 'var(--blue)';
    setTimeout(() => { btn.textContent = t.submitBtn; btn.style.background = ''; }, 2500);
    return;
  }

  btn.textContent = t.submitSending;
  btn.disabled = true;

  try {
    const res = await fetch('/api/messages/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, phone, message: msg })
    });
    if (!res.ok) throw new Error('Request failed');

    btn.textContent = t.submitDone;
    btn.style.background = 'var(--green)';
    ['iName', 'iEmail', 'iPhone', 'iMsg'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
  } catch (err) {
    btn.textContent = t.submitError;
    btn.style.background = '#EF4444';
  }

  setTimeout(() => {
    btn.textContent = t.submitBtn;
    btn.style.background = '';
    btn.disabled = false;
  }, 3500);
}

// ─── Nav scroll effect ────────────────────────────────────────
window.addEventListener('scroll', () => {
  const nav = document.querySelector('nav');
  if (nav) nav.style.boxShadow = window.scrollY > 20 ? '0 2px 20px rgba(0,0,0,.06)' : '';
});

// ─── Init ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setLang('ar');
});
