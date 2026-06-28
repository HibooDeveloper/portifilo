// ============================================================
// translations.js — Bilingual AR/EN content for portfolio
// Abubaker Hobeldeen Suliman — Portfolio
// ============================================================

const TRANSLATIONS = {
  ar: {
    lang: 'ar', dir: 'rtl',
    logoHTML: '<img src="/static/images/logo.png" alt="hibbo.tech" style="width:24px;height:24px;object-fit:contain;vertical-align:middle;margin-inline-end:.4rem"><span id="logoText">حبو<span style="color:var(--blue)">.تك</span></span>',
    heroBadge: 'متاح للمشاريع الجديدة',
    heroHead: 'بناء حلول رقمية<br><span class="accent">ذكية وقابلة للتوسع</span><br>بالذكاء الاصطناعي',
    heroSub: 'أساعد الشركات الناشئة والمؤسسات الكبرى على تحويل أفكارها إلى منتجات رقمية قابلة للتوسع — من تطبيقات Flutter إلى واجهات خلفية مدعومة بالذكاء الاصطناعي.',
    btnProj: 'استعرض المشاريع ↓',
    btnContact: 'تواصل معي ←',
    s1: 'سنوات خبرة', s2: 'مشروع مُنجز', s3: 'رضا العملاء',
    fb2: '🤖 مدعوم بالذكاء الاصطناعي',
    aboutRole: '// مهندس برمجيات · Flutter · حلول الذكاء الاصطناعي',
    availText: 'متاح للمشاريع الجديدة · القاهرة، مصر 🌍',
    projCount: 'مشروع مبني', freeTxt: 'بدأ العمل الحر',
    aboutLabel: 'عني',
    aboutTitle: 'مهندس بالتدريب،<br>صانع بالشغف',
    aboutP1: 'أنا مهندس برمجيات من القاهرة، مصر، متخصص في تطوير تطبيقات Flutter المحمولة، وواجهات Python الخلفية، والحلول المدعومة بالذكاء الاصطناعي. بخلفية في هندسة الحاسوب وأكثر من 5 سنوات من الخبرة في العمل الحر، أساعد الشركات على تحويل أفكارها إلى منتجات رقمية جاهزة للإنتاج.',
    aboutP2: 'أعمل عبر المجموعة التقنية الكاملة — من تصميم واجهات Flutter السلسة إلى بناء REST APIs قوية بـ Flask، ودمج قدرات الذكاء الاصطناعي، وإدارة مشاريع التحول الرقمي للشركات في المنطقة العربية وخارجها.',
    skillsLabel: 'الخبرات', skillsTitle: 'المهارات والتقنيات',
    skillsSub: 'الأدوات والتقنيات التي أستخدمها لبناء منتجات رقمية احترافية.',
    svcLabel: 'ماذا أقدم', svcTitle: 'خدماتي',
    svcSub: 'حلول رقمية متكاملة — من تطبيقات الجوال والأنظمة الخلفية إلى الذكاء الاصطناعي والاستشارات الرقمية.',
    projLabel: 'أعمالي', projTitle: 'المشاريع المميزة',
    projSub: 'حلول واقعية مبنية بأحدث التقنيات — جوال، خلفيات، ويب، وذكاء اصطناعي.',
    projDemo: 'عرض مباشر ↗', projGit: 'GitHub ⌥', projCase: 'دراسة الحالة 📖',
    aiLabel: 'حلول الذكاء الاصطناعي',
    aiTitle: 'أتمتة ذكية<br>للأعمال الحديثة',
    aiSub: 'أصمم وأنشر أنظمة مدعومة بالذكاء الاصطناعي تُؤتمت سير العمل، وتُولّد المحتوى، وتُحوّل طريقة عمل الشركات.',
    userLbl: 'المستخدم', aiLbl: 'المساعد الذكي',
    chatUser: 'أتمتة إنشاء تقرير المبيعات الأسبوعي وإرساله بالبريد الإلكتروني كل يوم اثنين الساعة 8 صباحاً.',
    chatAI: '✅ تم الفهم. سأقوم بإعداد:<br><br>1. مهمة Celery مجدولة يوم الاثنين 08:00 (توقيت القاهرة)<br>2. جلب البيانات من جداول مبيعات MySQL<br>3. إنشاء تقرير PDF منسق<br>4. إرساله عبر Flask-Mail<br><br>وقت التنفيذ: <strong style="color:var(--cyan)">ساعتان</strong>. هل تريد Telegram أيضاً؟',
    testiLabel: 'آراء العملاء', testiTitle: 'ماذا يقول عملائي',
    blogLabel: 'مركز المعرفة', blogTitle: 'آخر المقالات', blogAll: 'عرض الكل →',
    contactLabel: 'تواصل معي', contactTitle: 'هل أنت مستعد لبناء شيء رائع؟',
    contactSub: 'سواء كنت تحتاج تطبيق Flutter، أو واجهة Python خلفية، أو أتمتة بالذكاء الاصطناعي، أو تحولاً رقمياً شاملاً — تحدث معي.',
    cEmail: 'البريد الإلكتروني', cWA: 'واتساب', cLoc: 'الموقع',
    cLocVal: 'القاهرة، مصر — عن بُعد في جميع أنحاء العالم',
    formTitle: 'أرسل رسالة',
    lName: 'الاسم الكامل', lEmail: 'البريد الإلكتروني',
    lPhone: 'الهاتف (اختياري)', lMsg: 'الرسالة',
    iName: 'اسمك الكامل', iEmail: 'your@email.com',
    iPhone: '+20 1XX XXX XXXX', iMsg: 'أخبرني عن مشروعك...',
    submitBtn: 'إرسال الرسالة ←', submitDone: '✓ تم إرسال رسالتك!',
    submitSending: 'جارٍ الإرسال…', submitError: '✕ تعذّر الإرسال، حاول مجدداً', submitRequired: 'يرجى ملء جميع الحقول المطلوبة',
    footerMain: '© 2025 <span>أبوبكر حب الدين</span> · مهندس برمجيات وخبير حلول الذكاء الاصطناعي · القاهرة، مصر',
    footerSub: 'Flutter · Python · Flask · AI · التحول الرقمي',
    readMore: 'اقرأ المزيد ←',
    blogBack: 'العودة إلى المقالات', blogLoading: 'جارٍ تحميل المقال…',
    blogNotFound: 'لم يتم العثور على هذا المقال.', minRead: 'دقائق قراءة', views: 'مشاهدة',

    roles: [
      'مطور Flutter',
      'مطور Python خلفي',
      'خبير حلول الذكاء الاصطناعي',
      'مستشار التحول الرقمي',
      'مهندس تطبيقات الجوال'
    ],

    skills: [
      { icon: '📱', name: 'Flutter & Dart', pct: 95 },
      { icon: '🐍', name: 'Python', pct: 92 },
      { icon: '🔥', name: 'Firebase', pct: 88 },
      { icon: '⚗️', name: 'Flask', pct: 90 },
      { icon: '🗄️', name: 'MySQL', pct: 85 },
      { icon: '🔌', name: 'REST APIs', pct: 93 },
      { icon: '🤖', name: 'أدوات الذكاء الاصطناعي', pct: 88 },
      { icon: '✍️', name: 'هندسة المطالبات', pct: 91 },
      { icon: '📢', name: 'التسويق الرقمي', pct: 80 },
      { icon: '⚡', name: 'تحسين الأداء', pct: 84 },
    ],

    services: [
      { icon: '📱', name: 'تطوير تطبيقات الجوال', desc: 'تطبيقات iOS و Android متعددة المنصات بـ Flutter و Dart — سلسة، سريعة، وجاهزة للإنتاج.', tags: ['Flutter', 'Dart', 'Firebase'] },
      { icon: '⚙️', name: 'تطوير الأنظمة الخلفية', desc: 'Python Flask APIs قوية مع مصادقة JWT و SQLAlchemy ORM و Redis و MySQL.', tags: ['Python', 'Flask', 'MySQL'] },
      { icon: '🔌', name: 'تطوير REST APIs', desc: 'واجهات برمجية نظيفة وموثقة وآمنة مصممة للتوسع وسهولة التكامل.', tags: ['OpenAPI', 'Swagger', 'JWT'] },
      { icon: '🤖', name: 'دمج الذكاء الاصطناعي', desc: 'تضمين قدرات الذكاء الاصطناعي في منتجاتك — روبوتات محادثة، توليد محتوى، وأتمتة ذكية.', tags: ['LLM', 'OpenAI', 'Automation'] },
      { icon: '🔄', name: 'حلول الأتمتة', desc: 'أتمتة شاملة لسير عمل الأعمال باستخدام Celery والمهام المجدولة وخطوط AI.', tags: ['Celery', 'Redis', 'AI'] },
      { icon: '🌐', name: 'إدارة المواقع', desc: 'إعداد شامل للمواقع وتحسينها وإدارتها المستمرة للأداء والموثوقية.', tags: ['Nginx', 'Cloudflare', 'CDN'] },
      { icon: '💡', name: 'الاستشارات التقنية', desc: 'مراجعات معمارية، اختيار التقنيات، تدقيق الكود، وخارطة الطريق الرقمية.', tags: ['Architecture', 'Audit', 'Strategy'] },
      { icon: '📣', name: 'الاستشارات التسويقية', desc: 'استراتيجية تسويق رقمي قائمة على البيانات وإدارة وسائل التواصل وتحسين الأداء.', tags: ['SEO', 'Analytics', 'Growth'] },
    ],

    pfFilters: [
      { val: 'all', label: 'كل المشاريع' },
      { val: 'mobile', label: 'تطبيقات الجوال' },
      { val: 'backend', label: 'الأنظمة الخلفية' },
      { val: 'ai', label: 'مشاريع AI' },
      { val: 'web', label: 'تطبيقات الويب' },
    ],

    projects: [
      { emoji: '📱', name: 'تطبيق تتبع الشحنات', desc: 'تطبيق جوال لتتبع الطرود في الوقت الفعلي مع إدارة السائقين وخرائط مباشرة وإشعارات فورية.', cat: 'mobile', tech: ['Flutter', 'Firebase', 'Google Maps', 'REST API'], badge: 'تطبيق جوال' },
      { emoji: '🏪', name: 'منصة التجارة الإلكترونية', desc: 'منصة تجارية متكاملة مع كتالوج المنتجات والسلة والدفع ولوحة تحكم المشرف.', cat: 'web', tech: ['Flask', 'MySQL', 'Stripe', 'React'], badge: 'تطبيق ويب' },
      { emoji: '🤖', name: 'بوت دعم العملاء AI', desc: 'روبوت محادثة ذكي مدرب على بيانات الأعمال ومدمج في واتساب والويب مع توجيه التصعيد.', cat: 'ai', tech: ['Python', 'LangChain', 'OpenAI', 'WhatsApp API'], badge: 'مشروع AI' },
      { emoji: '🏥', name: 'نظام إدارة عيادة', desc: 'سجلات المرضى وجدولة المواعيد ونظام الفواتير مع صلاحيات متعددة وتقارير تفصيلية.', cat: 'backend', tech: ['Python', 'Flask', 'MySQL', 'SQLAlchemy'], badge: 'نظام خلفي' },
      { emoji: '📊', name: 'لوحة تحليلات الأعمال', desc: 'لوحة ذكاء أعمال بمخططات مخصصة وتتبع مؤشرات الأداء وتقارير آلية.', cat: 'web', tech: ['Flask', 'Chart.js', 'MySQL', 'Celery'], badge: 'تطبيق ويب' },
      { emoji: '🧠', name: 'منشئ محتوى AI', desc: 'خط أنابيب توليد المحتوى التلقائي لوسائل التواصل والمدونات والبريد التسويقي مع جدولة.', cat: 'ai', tech: ['Python', 'GPT-4', 'Flask', 'Celery'], badge: 'مشروع AI' },
    ],

    aiCards: [
      { icon: '🤖', name: 'روبوتات المحادثة AI', desc: 'أنظمة محادثة ذكية لدعم العملاء وتوليد العملاء المحتملين' },
      { icon: '⚡', name: 'أتمتة سير العمل', desc: 'أتمتة شاملة للعمليات تلغي المهام اليدوية المتكررة' },
      { icon: '✍️', name: 'توليد المحتوى', desc: 'خطوط إنتاج محتوى بالذكاء الاصطناعي للتسويق والتواصل' },
      { icon: '🔍', name: 'هندسة المطالبات', desc: 'مطالبات دقيقة تستخرج أقصى قيمة من نماذج الذكاء الاصطناعي' },
      { icon: '📊', name: 'معالجة البيانات', desc: 'خطوط استخراج وتحسين وتحليل البيانات الذكية' },
      { icon: '🔄', name: 'تكامل APIs', desc: 'ربط خدمات الذكاء الاصطناعي بسلاسة في أنظمة الأعمال القائمة' },
    ],

    testimonials: [
      { text: 'سلّم أبوبكر تطبيق Flutter الخاص بنا قبل الموعد المحدد بجودة استثنائية. الواجهة سلسة، وقاعدة الكود نظيفة، والدعم بعد الإطلاق كان ممتازاً. أنصح به بشدة!', name: 'أحمد الرشيدي', role: 'الرئيس التنفيذي، TechStart MENA', avatar: 'أر', color: '#2563EB', stars: 5 },
      { text: 'كانت واجهة API الخلفية بحاجة إلى إعادة بناء كاملة. أعاد أبوبكر بناءها بـ Flask بهندسة سليمة وتوثيق دقيق وأداء أفضل بـ 3 أضعاف. محترف حقيقي.', name: 'سارة ميتشيل', role: 'المدير التقني، Launchpad Agency', avatar: 'SM', color: '#10B981', stars: 5 },
      { text: 'روبوت المحادثة الذي بناه أبوبكر لدعم العملاء قلل وقت الاستجابة بنسبة 70٪ ويتعامل مع 80٪ من الاستفسارات تلقائياً. عائد استثمار مذهل.', name: 'خالد يوسف', role: 'مدير العمليات، eShop Group', avatar: 'خي', color: '#06B6D4', stars: 5 },
    ],

    blogs: [
      { emoji: '📱', cat: 'Flutter', slug: 'offline-first-flutter-hive-sync', title: 'بناء تطبيقات Flutter تعمل بدون إنترنت مع استراتيجية Hive للمزامنة', excerpt: 'كيفية تصميم تطبيقات Flutter تعمل بسلاسة دون اتصال وتتزامن بذكاء عند العودة للإنترنت.', date: '١٠ يونيو ٢٠٢٥', read: '٧ دقائق', tags: ['Flutter', 'Hive', 'Offline'],
        body: `
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
        <p>بهذا النهج يبقى تطبيقك سريع الاستجابة في كل الظروف، ويمنح المستخدمين تجربة موثوقة حتى في أسوأ ظروف الشبكة.</p>` },
      { emoji: '🐍', cat: 'Python', slug: 'production-flask-api-architecture', title: 'Flask APIs للإنتاج: أنماط معمارية تتوسع فعلاً', excerpt: 'من مسارات Flask الأساسية إلى REST APIs جاهزة للمؤسسات مع Blueprints ومصادقة JWT.', date: '٢٨ مايو ٢٠٢٥', read: '١٠ دقائق', tags: ['Python', 'Flask', 'API'],
        body: `
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
        <blockquote>البنية النظيفة ليست رفاهية — إنها ما يجعل صيانة المشروع ممكنة بعد عام من إطلاقه.</blockquote>` },
      { emoji: '🤖', cat: 'AI والأتمتة', slug: 'prompt-engineering-business-automation', title: 'هندسة المطالبات لأتمتة الأعمال: دليل عملي', excerpt: 'تقنيات واقعية لصياغة مطالبات تُشغّل تدفقات أتمتة أعمال موثوقة ومتسقة.', date: '١٥ مايو ٢٠٢٥', read: '٨ دقائق', tags: ['AI', 'Prompts', 'Automation'],
        body: `
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
        <p>بهذه التقنيات تتحول النماذج اللغوية من أداة محادثة إلى محرك أتمتة حقيقي داخل أعمالك.</p>` },
    ],
  },

  // ─────────────────────────────────────────────────────────────────────
  en: {
    lang: 'en', dir: 'ltr',
    logoHTML: '<img src="/static/images/logo.png" alt="hibbo.tech" style="width:24px;height:24px;object-fit:contain;vertical-align:middle;margin-inline-end:.4rem"><span id="logoText">hibbo<span style="color:var(--blue)">.tech</span></span>',
    heroBadge: 'Available for projects',
    heroHead: 'Building Smart<br><span class="accent">Digital Solutions</span><br>with AI',
    heroSub: 'Helping startups and enterprises transform ideas into scalable digital products — from Flutter apps to AI-powered backends.',
    btnProj: 'View Projects ↓',
    btnContact: 'Contact Me →',
    s1: 'Years Experience', s2: 'Projects Delivered', s3: 'Client Satisfaction',
    fb2: '🤖 AI Integrated',
    aboutRole: '// Software Engineer · Flutter · AI Solutions',
    availText: 'Available for projects · Cairo, Egypt 🌍',
    projCount: 'Projects Built', freeTxt: 'Started Freelancing',
    aboutLabel: 'About Me',
    aboutTitle: 'Engineer by training,<br>builder by passion',
    aboutP1: "I'm a Software Engineer from Cairo, Egypt specializing in Flutter mobile development, Python backends, and AI-powered solutions. With a foundation in Computer Engineering and 5+ years of freelancing experience, I help businesses transform their ideas into production-ready digital products.",
    aboutP2: "I work across the full stack — from crafting smooth mobile UIs in Flutter/Dart to building robust REST APIs in Flask, integrating AI capabilities, and managing digital transformation projects for startups and enterprises worldwide.",
    skillsLabel: 'Expertise', skillsTitle: 'Skills & Technologies',
    skillsSub: 'Tools and technologies I use to build production-grade digital products.',
    svcLabel: 'What I Do', svcTitle: 'Services I Offer',
    svcSub: 'End-to-end digital solutions — from mobile apps and backends to AI systems and digital strategy.',
    projLabel: 'Portfolio', projTitle: 'Featured Projects',
    projSub: 'Real-world solutions built with modern technology — mobile, backend, web, and AI.',
    projDemo: 'Live Demo ↗', projGit: 'GitHub ⌥', projCase: 'Case Study 📖',
    aiLabel: 'AI Solutions',
    aiTitle: 'Intelligent Automation<br>for Modern Businesses',
    aiSub: 'I design and deploy AI-powered systems that automate workflows, generate content, and transform how businesses operate.',
    userLbl: 'USER', aiLbl: 'AI ASSISTANT',
    chatUser: 'Automate my weekly sales report generation and send it via email every Monday at 8 AM.',
    chatAI: "✅ Understood. I'll set up:<br><br>1. A scheduled Celery task for Monday 08:00 Cairo time<br>2. Pull data from your MySQL sales tables<br>3. Generate a formatted PDF report<br>4. Send via Flask-Mail with custom template<br><br>Estimated setup time: <strong style=\"color:var(--cyan)\">2 hours</strong>. Should I also add Telegram notifications?",
    testiLabel: 'Client Reviews', testiTitle: 'What Clients Say',
    blogLabel: 'Knowledge Hub', blogTitle: 'Latest Articles', blogAll: 'View All →',
    contactLabel: 'Get in Touch', contactTitle: 'Ready to build something great?',
    contactSub: "Whether you need a Flutter app, a Python backend, AI automation, or full digital transformation — let's talk.",
    cEmail: 'Email', cWA: 'WhatsApp', cLoc: 'Location',
    cLocVal: 'Cairo, Egypt — Remote worldwide',
    formTitle: 'Send a Message',
    lName: 'Full Name', lEmail: 'Email Address',
    lPhone: 'Phone (optional)', lMsg: 'Message',
    iName: 'Your full name', iEmail: 'your@email.com',
    iPhone: '+1 234 567 8900', iMsg: 'Tell me about your project...',
    submitBtn: 'Send Message →', submitDone: '✓ Message Sent!',
    submitSending: 'Sending…', submitError: '✕ Could not send, try again', submitRequired: 'Please fill all required fields',
    footerMain: '© 2025 <span>Abubaker Hobeldeen Suliman</span> · Software Engineer & AI Solutions Specialist · Cairo, Egypt',
    footerSub: 'Flutter · Python · Flask · AI · Digital Transformation',
    readMore: 'Read More →',
    blogBack: 'Back to articles', blogLoading: 'Loading article…',
    blogNotFound: 'This article could not be found.', minRead: 'min read', views: 'views',

    roles: [
      'Flutter Developer',
      'Python Backend Dev',
      'AI Solutions Specialist',
      'Digital Transformation Consultant',
      'Mobile App Engineer'
    ],

    skills: [
      { icon: '📱', name: 'Flutter & Dart', pct: 95 },
      { icon: '🐍', name: 'Python', pct: 92 },
      { icon: '🔥', name: 'Firebase', pct: 88 },
      { icon: '⚗️', name: 'Flask', pct: 90 },
      { icon: '🗄️', name: 'MySQL', pct: 85 },
      { icon: '🔌', name: 'REST APIs', pct: 93 },
      { icon: '🤖', name: 'AI Tools', pct: 88 },
      { icon: '✍️', name: 'Prompt Engineering', pct: 91 },
      { icon: '📢', name: 'Digital Marketing', pct: 80 },
      { icon: '⚡', name: 'Performance Opt.', pct: 84 },
    ],

    services: [
      { icon: '📱', name: 'Mobile App Development', desc: 'Cross-platform iOS & Android apps built with Flutter & Dart — smooth, fast, and production-ready.', tags: ['Flutter', 'Dart', 'Firebase'] },
      { icon: '⚙️', name: 'Backend Development', desc: 'Robust Python Flask APIs with JWT auth, SQLAlchemy ORM, Redis caching, and MySQL databases.', tags: ['Python', 'Flask', 'MySQL'] },
      { icon: '🔌', name: 'REST API Development', desc: 'Clean, documented, and secure RESTful APIs designed for scalability and ease of integration.', tags: ['OpenAPI', 'Swagger', 'JWT'] },
      { icon: '🤖', name: 'AI Integration', desc: 'Embed AI capabilities into your products — chatbots, content generation, and intelligent automation.', tags: ['LLM', 'OpenAI', 'Automation'] },
      { icon: '🔄', name: 'Automation Solutions', desc: 'End-to-end business workflow automation using Celery, cron jobs, and AI-powered pipelines.', tags: ['Celery', 'Redis', 'AI'] },
      { icon: '🌐', name: 'Website Management', desc: 'Full website setup, optimization, and ongoing management for performance and reliability.', tags: ['Nginx', 'Cloudflare', 'CDN'] },
      { icon: '💡', name: 'Technical Consulting', desc: 'Architecture reviews, technology selection, code audits, and digital roadmapping.', tags: ['Architecture', 'Audit', 'Strategy'] },
      { icon: '📣', name: 'Digital Marketing Consulting', desc: 'Data-driven digital marketing strategy, social media management, and performance optimization.', tags: ['SEO', 'Analytics', 'Growth'] },
    ],

    pfFilters: [
      { val: 'all', label: 'All Projects' },
      { val: 'mobile', label: 'Mobile Apps' },
      { val: 'backend', label: 'Backend' },
      { val: 'ai', label: 'AI Projects' },
      { val: 'web', label: 'Web Apps' },
    ],

    projects: [
      { emoji: '📱', name: 'Delivery Tracking App', desc: 'Real-time parcel tracking mobile app with driver management, live map integration, and push notifications.', cat: 'mobile', tech: ['Flutter', 'Firebase', 'Google Maps', 'REST API'], badge: 'Mobile App' },
      { emoji: '🏪', name: 'E-Commerce Platform', desc: 'Full-stack marketplace with product catalog, cart, payment integration, and admin dashboard.', cat: 'web', tech: ['Flask', 'MySQL', 'Stripe', 'React'], badge: 'Web App' },
      { emoji: '🤖', name: 'AI Customer Support Bot', desc: 'Intelligent chatbot trained on business data, integrated into WhatsApp and web with escalation routing.', cat: 'ai', tech: ['Python', 'LangChain', 'OpenAI', 'WhatsApp API'], badge: 'AI Project' },
      { emoji: '🏥', name: 'Clinic Management System', desc: 'Patient records, appointment scheduling, and billing system with role-based access and reporting.', cat: 'backend', tech: ['Python', 'Flask', 'MySQL', 'SQLAlchemy'], badge: 'Backend' },
      { emoji: '📊', name: 'Analytics Dashboard', desc: 'Real-time business intelligence dashboard with custom charts, KPI tracking, and automated reports.', cat: 'web', tech: ['Flask', 'Chart.js', 'MySQL', 'Celery'], badge: 'Web App' },
      { emoji: '🧠', name: 'AI Content Generator', desc: 'Automated content generation pipeline for social media, blogs, and email marketing with scheduling.', cat: 'ai', tech: ['Python', 'GPT-4', 'Flask', 'Celery'], badge: 'AI Project' },
    ],

    aiCards: [
      { icon: '🤖', name: 'AI Chatbots', desc: 'Intelligent conversational systems for customer support and lead generation' },
      { icon: '⚡', name: 'Workflow Automation', desc: 'End-to-end process automation eliminating manual, repetitive tasks' },
      { icon: '✍️', name: 'Content Generation', desc: 'AI-powered content pipelines for marketing and business communication' },
      { icon: '🔍', name: 'Prompt Engineering', desc: 'Precision-tuned prompts that extract maximum value from AI models' },
      { icon: '📊', name: 'Data Processing', desc: 'Intelligent data extraction, enrichment, and analysis pipelines' },
      { icon: '🔄', name: 'API Integration', desc: 'Seamlessly connecting AI services into existing business systems' },
    ],

    testimonials: [
      { text: "Abubaker delivered our Flutter app ahead of schedule with exceptional quality. The UI is smooth, the codebase is clean, and post-launch support has been outstanding. Highly recommend!", name: 'Ahmed Al-Rashidi', role: 'CEO, TechStart MENA', avatar: 'AR', color: '#2563EB', stars: 5 },
      { text: "Our backend API needed a complete overhaul. Abubaker rebuilt it in Flask with proper architecture, solid documentation, and 3x better performance. A true professional.", name: 'Sarah Mitchell', role: 'CTO, Launchpad Agency', avatar: 'SM', color: '#10B981', stars: 5 },
      { text: "The AI chatbot Abubaker built for our customer support has reduced our response time by 70% and handles 80% of inquiries automatically. Incredible ROI.", name: 'Khalid Youssef', role: 'Operations Director, eShop Group', avatar: 'KY', color: '#06B6D4', stars: 5 },
    ],

    blogs: [
      { emoji: '📱', cat: 'Flutter', slug: 'offline-first-flutter-hive-sync', title: 'Building Offline-First Flutter Apps with Hive & Sync Strategy', excerpt: 'How to design Flutter apps that work seamlessly offline and sync gracefully when connectivity returns.', date: 'Jun 10, 2025', read: '7 min', tags: ['Flutter', 'Hive', 'Offline'],
        body: `
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
        <p>With this approach your app stays responsive in every condition, giving users a reliable experience even on the worst networks.</p>` },
      { emoji: '🐍', cat: 'Python', slug: 'production-flask-api-architecture', title: 'Production Flask APIs: Architecture Patterns That Actually Scale', excerpt: 'From basic Flask routes to enterprise-ready REST APIs with blueprints, JWT auth, and proper error handling.', date: 'May 28, 2025', read: '10 min', tags: ['Python', 'Flask', 'API'],
        body: `
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
        <blockquote>Clean architecture isn't a luxury — it's what makes a project maintainable a year after launch.</blockquote>` },
      { emoji: '🤖', cat: 'AI & Automation', slug: 'prompt-engineering-business-automation', title: 'Prompt Engineering for Business Automation: A Practical Guide', excerpt: 'Real-world techniques for crafting prompts that power reliable, consistent business automation workflows.', date: 'May 15, 2025', read: '8 min', tags: ['AI', 'Prompts', 'Automation'],
        body: `
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
        <p>With these techniques, language models shift from a chat toy into a genuine automation engine inside your business.</p>` },
    ],
  }
};
