"""scripts/seed_content.py

Import the original static homepage content (the arrays that used to live in
app/static/js/translations.js) into the database so it can be managed from the
admin panel.

Idempotent — safe to run repeatedly. Skips any record that already exists:
  • services      by title_en
  • projects      by slug (derived from title_en)
  • testimonials  by client_name
  • blog posts    by slug

Run inside the app container:
    docker exec portfolio_app python scripts/seed_content.py
"""
import json
import os
import re
import sys
from datetime import datetime

# Allow running the file directly (`python scripts/seed_content.py`): make sure
# the project root is on sys.path so the `app` package is importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Service, Project, Testimonial, BlogPost, Skill, AICard


def slugify(text):
    text = (text or '').lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return re.sub(r'-+', '-', text).strip('-')


# ── Services ───────────────────────────────────────────────────────────
SERVICES = [
    {'icon': '📱', 'title_ar': 'تطوير تطبيقات الجوال', 'title_en': 'Mobile App Development',
     'desc_ar': 'تطبيقات iOS و Android متعددة المنصات بـ Flutter و Dart — سلسة، سريعة، وجاهزة للإنتاج.',
     'desc_en': 'Cross-platform iOS & Android apps built with Flutter & Dart — smooth, fast, and production-ready.',
     'tags': ['Flutter', 'Dart', 'Firebase']},
    {'icon': '⚙️', 'title_ar': 'تطوير الأنظمة الخلفية', 'title_en': 'Backend Development',
     'desc_ar': 'Python Flask APIs قوية مع مصادقة JWT و SQLAlchemy ORM و Redis و MySQL.',
     'desc_en': 'Robust Python Flask APIs with JWT auth, SQLAlchemy ORM, Redis caching, and MySQL databases.',
     'tags': ['Python', 'Flask', 'MySQL']},
    {'icon': '🔌', 'title_ar': 'تطوير REST APIs', 'title_en': 'REST API Development',
     'desc_ar': 'واجهات برمجية نظيفة وموثقة وآمنة مصممة للتوسع وسهولة التكامل.',
     'desc_en': 'Clean, documented, and secure RESTful APIs designed for scalability and ease of integration.',
     'tags': ['OpenAPI', 'Swagger', 'JWT']},
    {'icon': '🤖', 'title_ar': 'دمج الذكاء الاصطناعي', 'title_en': 'AI Integration',
     'desc_ar': 'تضمين قدرات الذكاء الاصطناعي في منتجاتك — روبوتات محادثة، توليد محتوى، وأتمتة ذكية.',
     'desc_en': 'Embed AI capabilities into your products — chatbots, content generation, and intelligent automation.',
     'tags': ['LLM', 'OpenAI', 'Automation']},
    {'icon': '🔄', 'title_ar': 'حلول الأتمتة', 'title_en': 'Automation Solutions',
     'desc_ar': 'أتمتة شاملة لسير عمل الأعمال باستخدام Celery والمهام المجدولة وخطوط AI.',
     'desc_en': 'End-to-end business workflow automation using Celery, cron jobs, and AI-powered pipelines.',
     'tags': ['Celery', 'Redis', 'AI']},
    {'icon': '🌐', 'title_ar': 'إدارة المواقع', 'title_en': 'Website Management',
     'desc_ar': 'إعداد شامل للمواقع وتحسينها وإدارتها المستمرة للأداء والموثوقية.',
     'desc_en': 'Full website setup, optimization, and ongoing management for performance and reliability.',
     'tags': ['Nginx', 'Cloudflare', 'CDN']},
    {'icon': '💡', 'title_ar': 'الاستشارات التقنية', 'title_en': 'Technical Consulting',
     'desc_ar': 'مراجعات معمارية، اختيار التقنيات، تدقيق الكود، وخارطة الطريق الرقمية.',
     'desc_en': 'Architecture reviews, technology selection, code audits, and digital roadmapping.',
     'tags': ['Architecture', 'Audit', 'Strategy']},
    {'icon': '📣', 'title_ar': 'الاستشارات التسويقية', 'title_en': 'Digital Marketing Consulting',
     'desc_ar': 'استراتيجية تسويق رقمي قائمة على البيانات وإدارة وسائل التواصل وتحسين الأداء.',
     'desc_en': 'Data-driven digital marketing strategy, social media management, and performance optimization.',
     'tags': ['SEO', 'Analytics', 'Growth']},
]

# ── Projects ───────────────────────────────────────────────────────────
PROJECTS = [
    {'title_ar': 'تطبيق تتبع الشحنات', 'title_en': 'Delivery Tracking App',
     'desc_ar': 'تطبيق جوال لتتبع الطرود في الوقت الفعلي مع إدارة السائقين وخرائط مباشرة وإشعارات فورية.',
     'desc_en': 'Real-time parcel tracking mobile app with driver management, live map integration, and push notifications.',
     'cat': 'mobile', 'tech': ['Flutter', 'Firebase', 'Google Maps', 'REST API']},
    {'title_ar': 'منصة التجارة الإلكترونية', 'title_en': 'E-Commerce Platform',
     'desc_ar': 'منصة تجارية متكاملة مع كتالوج المنتجات والسلة والدفع ولوحة تحكم المشرف.',
     'desc_en': 'Full-stack marketplace with product catalog, cart, payment integration, and admin dashboard.',
     'cat': 'web', 'tech': ['Flask', 'MySQL', 'Stripe', 'React']},
    {'title_ar': 'بوت دعم العملاء AI', 'title_en': 'AI Customer Support Bot',
     'desc_ar': 'روبوت محادثة ذكي مدرب على بيانات الأعمال ومدمج في واتساب والويب مع توجيه التصعيد.',
     'desc_en': 'Intelligent chatbot trained on business data, integrated into WhatsApp and web with escalation routing.',
     'cat': 'ai', 'tech': ['Python', 'LangChain', 'OpenAI', 'WhatsApp API']},
    {'title_ar': 'نظام إدارة عيادة', 'title_en': 'Clinic Management System',
     'desc_ar': 'سجلات المرضى وجدولة المواعيد ونظام الفواتير مع صلاحيات متعددة وتقارير تفصيلية.',
     'desc_en': 'Patient records, appointment scheduling, and billing system with role-based access and reporting.',
     'cat': 'backend', 'tech': ['Python', 'Flask', 'MySQL', 'SQLAlchemy']},
    {'title_ar': 'لوحة تحليلات الأعمال', 'title_en': 'Analytics Dashboard',
     'desc_ar': 'لوحة ذكاء أعمال بمخططات مخصصة وتتبع مؤشرات الأداء وتقارير آلية.',
     'desc_en': 'Real-time business intelligence dashboard with custom charts, KPI tracking, and automated reports.',
     'cat': 'web', 'tech': ['Flask', 'Chart.js', 'MySQL', 'Celery']},
    {'title_ar': 'منشئ محتوى AI', 'title_en': 'AI Content Generator',
     'desc_ar': 'خط أنابيب توليد المحتوى التلقائي لوسائل التواصل والمدونات والبريد التسويقي مع جدولة.',
     'desc_en': 'Automated content generation pipeline for social media, blogs, and email marketing with scheduling.',
     'cat': 'ai', 'tech': ['Python', 'GPT-4', 'Flask', 'Celery']},
]

# ── Skills ─────────────────────────────────────────────────────────────
SKILLS = [
    {'icon': '📱', 'name_ar': 'Flutter & Dart', 'name_en': 'Flutter & Dart', 'pct': 95},
    {'icon': '🐍', 'name_ar': 'Python', 'name_en': 'Python', 'pct': 92},
    {'icon': '🔥', 'name_ar': 'Firebase', 'name_en': 'Firebase', 'pct': 88},
    {'icon': '⚗️', 'name_ar': 'Flask', 'name_en': 'Flask', 'pct': 90},
    {'icon': '🗄️', 'name_ar': 'MySQL', 'name_en': 'MySQL', 'pct': 85},
    {'icon': '🔌', 'name_ar': 'REST APIs', 'name_en': 'REST APIs', 'pct': 93},
    {'icon': '🤖', 'name_ar': 'أدوات الذكاء الاصطناعي', 'name_en': 'AI Tools', 'pct': 88},
    {'icon': '✍️', 'name_ar': 'هندسة المطالبات', 'name_en': 'Prompt Engineering', 'pct': 91},
    {'icon': '📢', 'name_ar': 'التسويق الرقمي', 'name_en': 'Digital Marketing', 'pct': 80},
    {'icon': '⚡', 'name_ar': 'تحسين الأداء', 'name_en': 'Performance Opt.', 'pct': 84},
]

# ── AI Cards ───────────────────────────────────────────────────────────
AI_CARDS = [
    {'icon': '🤖', 'title_ar': 'روبوتات المحادثة AI', 'title_en': 'AI Chatbots',
     'desc_ar': 'أنظمة محادثة ذكية لدعم العملاء وتوليد العملاء المحتملين',
     'desc_en': 'Intelligent conversational systems for customer support and lead generation'},
    {'icon': '⚡', 'title_ar': 'أتمتة سير العمل', 'title_en': 'Workflow Automation',
     'desc_ar': 'أتمتة شاملة للعمليات تلغي المهام اليدوية المتكررة',
     'desc_en': 'End-to-end process automation eliminating manual, repetitive tasks'},
    {'icon': '✍️', 'title_ar': 'توليد المحتوى', 'title_en': 'Content Generation',
     'desc_ar': 'خطوط إنتاج محتوى بالذكاء الاصطناعي للتسويق والتواصل',
     'desc_en': 'AI-powered content pipelines for marketing and business communication'},
    {'icon': '🔍', 'title_ar': 'هندسة المطالبات', 'title_en': 'Prompt Engineering',
     'desc_ar': 'مطالبات دقيقة تستخرج أقصى قيمة من نماذج الذكاء الاصطناعي',
     'desc_en': 'Precision-tuned prompts that extract maximum value from AI models'},
    {'icon': '📊', 'title_ar': 'معالجة البيانات', 'title_en': 'Data Processing',
     'desc_ar': 'خطوط استخراج وتحسين وتحليل البيانات الذكية',
     'desc_en': 'Intelligent data extraction, enrichment, and analysis pipelines'},
    {'icon': '🔄', 'title_ar': 'تكامل APIs', 'title_en': 'API Integration',
     'desc_ar': 'ربط خدمات الذكاء الاصطناعي بسلاسة في أنظمة الأعمال القائمة',
     'desc_en': 'Seamlessly connecting AI services into existing business systems'},
]

# ── Testimonials ───────────────────────────────────────────────────────
TESTIMONIALS = [
    {'name': 'Ahmed Al-Rashidi', 'role_ar': 'الرئيس التنفيذي، TechStart MENA', 'role_en': 'CEO, TechStart MENA',
     'text_ar': 'سلّم أبوبكر تطبيق Flutter الخاص بنا قبل الموعد المحدد بجودة استثنائية. الواجهة سلسة، وقاعدة الكود نظيفة، والدعم بعد الإطلاق كان ممتازاً. أنصح به بشدة!',
     'text_en': 'Abubaker delivered our Flutter app ahead of schedule with exceptional quality. The UI is smooth, the codebase is clean, and post-launch support has been outstanding. Highly recommend!',
     'stars': 5},
    {'name': 'Sarah Mitchell', 'role_ar': 'المدير التقني، Launchpad Agency', 'role_en': 'CTO, Launchpad Agency',
     'text_ar': 'كانت واجهة API الخلفية بحاجة إلى إعادة بناء كاملة. أعاد أبوبكر بناءها بـ Flask بهندسة سليمة وتوثيق دقيق وأداء أفضل بـ 3 أضعاف. محترف حقيقي.',
     'text_en': 'Our backend API needed a complete overhaul. Abubaker rebuilt it in Flask with proper architecture, solid documentation, and 3x better performance. A true professional.',
     'stars': 5},
    {'name': 'Khalid Youssef', 'role_ar': 'مدير العمليات، eShop Group', 'role_en': 'Operations Director, eShop Group',
     'text_ar': 'روبوت المحادثة الذي بناه أبوبكر لدعم العملاء قلل وقت الاستجابة بنسبة 70٪ ويتعامل مع 80٪ من الاستفسارات تلقائياً. عائد استثمار مذهل.',
     'text_en': 'The AI chatbot Abubaker built for our customer support has reduced our response time by 70% and handles 80% of inquiries automatically. Incredible ROI.',
     'stars': 5},
]

# ── Blog posts ─────────────────────────────────────────────────────────
BLOG_BODY_AR_1 = '''
        <p>عند بناء تطبيقات الجوال، غالباً ما يكون الاتصال بالإنترنت غير مضمون. النهج <strong>Offline-First</strong> يجعل التطبيق يعمل بالكامل من قاعدة بيانات محلية، ثم يتزامن مع الخادم في الخلفية عند توفر الشبكة.</p>
        <h2>لماذا Hive؟</h2>
        <p>‏Hive قاعدة بيانات NoSQL خفيفة ومكتوبة بلغة Dart الخالصة — سريعة جداً ولا تعتمد على إضافات أصلية، مما يجعلها مثالية لتخزين البيانات محلياً.</p>
        <ul>
          <li>قراءة وكتابة فائقة السرعة</li>
          <li>دعم التشفير المدمج</li>
          <li>تكامل سلس مع نماذج البيانات عبر <code>TypeAdapters</code></li>
        </ul>
        <h2>استراتيجية المزامنة</h2>
        <p>نخزّن كل تغيير محلياً مع علامة <code>isSynced = false</code>، ثم نرفع التغييرات غير المتزامنة عند عودة الاتصال:</p>
        <pre><code>final box = await Hive.openBox('tasks');
await box.put(task.id, task..isSynced = false);

connectivity.onConnectivityChanged.listen((status) {
  if (status != ConnectivityResult.none) syncPending();
});</code></pre>
        <blockquote>القاعدة الذهبية: لا يجب أن ينتظر المستخدم الشبكة أبداً — الواجهة تتفاعل فوراً مع البيانات المحلية.</blockquote>
        <h2>شرح بالفيديو</h2>
        <p>https://youtu.be/lHhRhPV--G0</p>
        <p>بهذا النهج يبقى تطبيقك سريع الاستجابة في كل الظروف، ويمنح المستخدمين تجربة موثوقة حتى في أسوأ ظروف الشبكة.</p>'''

BLOG_BODY_EN_1 = '''
        <p>When building mobile apps, connectivity is never guaranteed. An <strong>offline-first</strong> approach makes the app run entirely from a local database, then sync with the server in the background once the network is available.</p>
        <h2>Why Hive?</h2>
        <p>Hive is a lightweight NoSQL database written in pure Dart — extremely fast and with no native dependencies, making it ideal for local storage.</p>
        <ul>
          <li>Blazing-fast reads and writes</li>
          <li>Built-in encryption support</li>
          <li>Clean integration with your models via <code>TypeAdapters</code></li>
        </ul>
        <h2>The Sync Strategy</h2>
        <p>Store every change locally with an <code>isSynced = false</code> flag, then push unsynced records when connectivity returns:</p>
        <pre><code>final box = await Hive.openBox('tasks');
await box.put(task.id, task..isSynced = false);

connectivity.onConnectivityChanged.listen((status) {
  if (status != ConnectivityResult.none) syncPending();
});</code></pre>
        <blockquote>The golden rule: the user should never wait on the network — the UI reacts instantly to local data.</blockquote>
        <h2>Watch the walkthrough</h2>
        <p>https://youtu.be/lHhRhPV--G0</p>
        <p>With this approach your app stays responsive in every condition, giving users a reliable experience even on the worst networks.</p>'''

BLOG_BODY_AR_2 = '''
        <p>الانتقال من نموذج Flask بسيط إلى واجهة API جاهزة للإنتاج يتطلب بنية واضحة. المفتاح هو <strong>مصنع التطبيق (Application Factory)</strong> مع <strong>Blueprints</strong> لتقسيم المسؤوليات.</p>
        <h2>مصنع التطبيق</h2>
        <pre><code>def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    db.init_app(app)
    app.register_blueprint(blogs_bp, url_prefix='/api/blogs')
    return app</code></pre>
        <h2>طبقات منفصلة</h2>
        <ul>
          <li><strong>المسارات (Routes):</strong> تستقبل الطلب وتعيد الاستجابة فقط</li>
          <li><strong>الخدمات (Services):</strong> منطق الأعمال</li>
          <li><strong>النماذج (Models):</strong> طبقة قاعدة البيانات عبر SQLAlchemy</li>
        </ul>
        <h2>الأمان والأداء</h2>
        <p>أضف مصادقة JWT، وتحديد المعدل عبر Flask-Limiter، وتخزيناً مؤقتاً بـ Redis — وستحصل على واجهة API تتحمّل أحمال الإنتاج الحقيقية.</p>
        <blockquote>البنية النظيفة ليست رفاهية — إنها ما يجعل صيانة المشروع ممكنة بعد عام من إطلاقه.</blockquote>'''

BLOG_BODY_EN_2 = '''
        <p>Going from a toy Flask script to a production-ready API requires clear structure. The key is the <strong>application factory</strong> pattern combined with <strong>blueprints</strong> to separate concerns.</p>
        <h2>The Application Factory</h2>
        <pre><code>def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_map[config_name])
    db.init_app(app)
    app.register_blueprint(blogs_bp, url_prefix='/api/blogs')
    return app</code></pre>
        <h2>Separated Layers</h2>
        <ul>
          <li><strong>Routes:</strong> only receive the request and return a response</li>
          <li><strong>Services:</strong> business logic</li>
          <li><strong>Models:</strong> the database layer via SQLAlchemy</li>
        </ul>
        <h2>Security & Performance</h2>
        <p>Add JWT auth, rate limiting via Flask-Limiter, and Redis caching — and you get an API that survives real production load.</p>
        <blockquote>Clean architecture isn't a luxury — it's what makes a project maintainable a year after launch.</blockquote>'''

BLOG_BODY_AR_3 = '''
        <p>المطالبة الجيدة هي الفرق بين أتمتة موثوقة وأخرى عشوائية. في سياق الأعمال، نحتاج مخرجات <strong>متسقة وقابلة للتحليل</strong>.</p>
        <h2>المبادئ الأساسية</h2>
        <ul>
          <li>حدّد الدور والسياق بوضوح</li>
          <li>اطلب صيغة مخرجات محددة (JSON مثلاً)</li>
          <li>أعطِ أمثلة (few-shot) لتثبيت السلوك</li>
        </ul>
        <h2>مثال عملي</h2>
        <pre><code>صنّف رسالة العميل التالية وأعد JSON فقط:
{ "category": "...", "priority": "high|medium|low" }</code></pre>
        <blockquote>عندما تطلب صيغة منظمة، يصبح بإمكانك ربط مخرجات الذكاء الاصطناعي مباشرة بأنظمتك دون تدخل بشري.</blockquote>
        <p>بهذه التقنيات تتحول النماذج اللغوية من أداة محادثة إلى محرك أتمتة حقيقي داخل أعمالك.</p>'''

BLOG_BODY_EN_3 = '''
        <p>A good prompt is the difference between reliable automation and random output. In a business context, we need <strong>consistent, parseable</strong> results.</p>
        <h2>Core Principles</h2>
        <ul>
          <li>Define the role and context clearly</li>
          <li>Request a specific output format (e.g. JSON)</li>
          <li>Provide few-shot examples to anchor behavior</li>
        </ul>
        <h2>A Practical Example</h2>
        <pre><code>Classify the following customer message and return JSON only:
{ "category": "...", "priority": "high|medium|low" }</code></pre>
        <blockquote>When you request structured output, you can wire AI responses directly into your systems with zero human intervention.</blockquote>
        <p>With these techniques, language models shift from a chat toy into a genuine automation engine inside your business.</p>'''

BLOGS = [
    {'slug': 'offline-first-flutter-hive-sync', 'cat': 'Flutter', 'read': 7,
     'published_at': datetime(2025, 6, 10),
     'title_ar': 'بناء تطبيقات Flutter تعمل بدون إنترنت مع استراتيجية Hive للمزامنة',
     'title_en': 'Building Offline-First Flutter Apps with Hive & Sync Strategy',
     'excerpt_ar': 'كيفية تصميم تطبيقات Flutter تعمل بسلاسة دون اتصال وتتزامن بذكاء عند العودة للإنترنت.',
     'excerpt_en': 'How to design Flutter apps that work seamlessly offline and sync gracefully when connectivity returns.',
     'tags': ['Flutter', 'Hive', 'Offline'],
     'content_ar': BLOG_BODY_AR_1, 'content_en': BLOG_BODY_EN_1},
    {'slug': 'production-flask-api-architecture', 'cat': 'Python', 'read': 10,
     'published_at': datetime(2025, 5, 28),
     'title_ar': 'Flask APIs للإنتاج: أنماط معمارية تتوسع فعلاً',
     'title_en': 'Production Flask APIs: Architecture Patterns That Actually Scale',
     'excerpt_ar': 'من مسارات Flask الأساسية إلى REST APIs جاهزة للمؤسسات مع Blueprints ومصادقة JWT.',
     'excerpt_en': 'From basic Flask routes to enterprise-ready REST APIs with blueprints, JWT auth, and proper error handling.',
     'tags': ['Python', 'Flask', 'API'],
     'content_ar': BLOG_BODY_AR_2, 'content_en': BLOG_BODY_EN_2},
    {'slug': 'prompt-engineering-business-automation', 'cat': 'AI & Automation', 'read': 8,
     'published_at': datetime(2025, 5, 15),
     'title_ar': 'هندسة المطالبات لأتمتة الأعمال: دليل عملي',
     'title_en': 'Prompt Engineering for Business Automation: A Practical Guide',
     'excerpt_ar': 'تقنيات واقعية لصياغة مطالبات تُشغّل تدفقات أتمتة أعمال موثوقة ومتسقة.',
     'excerpt_en': 'Real-world techniques for crafting prompts that power reliable, consistent business automation workflows.',
     'tags': ['AI', 'Prompts', 'Automation'],
     'content_ar': BLOG_BODY_AR_3, 'content_en': BLOG_BODY_EN_3},
]


def run():
    app = create_app()
    with app.app_context():
        added = {'services': 0, 'projects': 0, 'testimonials': 0, 'blogs': 0,
                 'skills': 0, 'ai_cards': 0}

        for i, s in enumerate(SERVICES):
            if Service.query.filter_by(title_en=s['title_en']).first():
                continue
            db.session.add(Service(
                icon=s['icon'], title_ar=s['title_ar'], title_en=s['title_en'],
                desc_ar=s['desc_ar'], desc_en=s['desc_en'],
                tags=json.dumps(s['tags']), sort_order=i + 1, is_active=True))
            added['services'] += 1

        for i, p in enumerate(PROJECTS):
            slug = slugify(p['title_en'])
            if Project.query.filter_by(slug=slug).first():
                continue
            db.session.add(Project(
                slug=slug, title_ar=p['title_ar'], title_en=p['title_en'],
                desc_ar=p['desc_ar'], desc_en=p['desc_en'],
                category=p['cat'], status='published',
                tech_stack=json.dumps(p['tech']),
                is_featured=(i == 0), sort_order=i + 1))
            added['projects'] += 1

        for i, t in enumerate(TESTIMONIALS):
            if Testimonial.query.filter_by(client_name=t['name']).first():
                continue
            db.session.add(Testimonial(
                client_name=t['name'], client_role_ar=t['role_ar'],
                client_role_en=t['role_en'], text_ar=t['text_ar'],
                text_en=t['text_en'], rating=t['stars'],
                is_active=True, sort_order=i + 1))
            added['testimonials'] += 1

        for i, b in enumerate(BLOGS):
            if BlogPost.query.filter_by(slug=b['slug']).first():
                continue
            db.session.add(BlogPost(
                slug=b['slug'], title_ar=b['title_ar'], title_en=b['title_en'],
                excerpt_ar=b['excerpt_ar'], excerpt_en=b['excerpt_en'],
                content_ar=b['content_ar'], content_en=b['content_en'],
                category=b['cat'], tags=json.dumps(b['tags']),
                status='published', read_time_min=b['read'],
                is_featured=(i == 0), published_at=b['published_at']))
            added['blogs'] += 1

        for i, sk in enumerate(SKILLS):
            if Skill.query.filter_by(name_en=sk['name_en']).first():
                continue
            db.session.add(Skill(
                icon=sk['icon'], name_ar=sk['name_ar'], name_en=sk['name_en'],
                percent=sk['pct'], sort_order=i + 1, is_active=True))
            added['skills'] += 1

        for i, c in enumerate(AI_CARDS):
            if AICard.query.filter_by(title_en=c['title_en']).first():
                continue
            db.session.add(AICard(
                icon=c['icon'], title_ar=c['title_ar'], title_en=c['title_en'],
                desc_ar=c['desc_ar'], desc_en=c['desc_en'],
                sort_order=i + 1, is_active=True))
            added['ai_cards'] += 1

        db.session.commit()
        print('✓ Seed complete:', added)


if __name__ == '__main__':
    run()
