# Session 2026-06-10d — Quota Ledger + Suite Sealing

## 🎯 السياق
الجلسة السابقة علّقت نص ساعة (bash واقف) لأن الـ test suite كانت بتعمل
real LLM calls بدون حدود → الـ snapshot ماتسجلش → **الـ workspace ضاع
بالكامل**. الإنقاذ تم من GitHub (v2.6.0 كانت مرفوعة). `.env` اتعاد بناؤه.

## 🛡️ القاعدة الجديدة (المطلوبة من فارس)
> "خلي في البيئة بتاعتك يفشل تلقائي لما يعدي وقت معين"

كل شيء الآن مزدوج الحماية:
1. كل أمر bash: `timeout N` داخلي + tool timeout خارجي
2. `llm_pool`: HTTP timeout 30s + MAX_ATTEMPTS 4 + budget 200/run
3. pytest.ini: 90s/test + 1200s/session
4. **الجديد — Quota Ledger**: حصص يومية على الديسك تعيش عبر الجلسات

## ✅ المنجز

### 1. 📒 QuotaLedger (`ai_earth/core/quota_ledger.py`)
```yaml
الملف: data/quota_ledger.json (atomic writes + fcntl lock + prune 30 يوم)
stdlib فقط — صفر dependencies، يستحيل يكسر llm_pool
حصص يومية (env-overridable):
  github: 120/يوم | openrouter: 500 | google: 150 | serper: 60
التكامل في call_llm:
  - pre-flight: مزوّد خلصت حصته اليومية → skip فوري (صفر HTTP، صفر انتظار)
  - post-flight: كل محاولة تتسجل (حتى الفاشلة — الريموت عدّها برضه)
web_search: نفس الحماية لـ Serper (كريدتس one-time)
fail-open: أي خطأ في الليدجر نفسه لا يمنع النداءات أبداً
```

### 2. 🕵️ الـ Ledger كشف تسريبات فوراً (قيمة يوم أول!)
الـ structural suite كانت بتسرّب **14 LLM attempt** خفية:
- `benchmark.py` health → real chat في كل `run_all()` (×6)
- `tests/test_api.py::test_chat` بدون `@llm` (×1)
- `tests/lego/test_agent_judge.py` evaluation حية بدون marker (×3)
- `tests/lego/test_storm.py` perspectives+questions حية (×2)
- `tests/lego/test_self_discover.py` selection حية (×1)

**كل التسريبات اتقفلت**:
- `BenchmarkSuite.run_all(llm=bool)` + `_bench_health(llm=False)` = فحص هيكلي
  (router built + keys available + quota left) بدون HTTP
- التستات الحية اتعلّمت `@pytest.mark.llm` (بدون أي mock — فلسفة ثابتة)

### 3. 🌐 API endpoints جديدة
- `GET /quota` — استهلاك اليوم لكل مزوّد ضد الحصص
- `GET /quota/history?days=N` — آخر N أيام
- `GET /vault` — إحصائيات الفولت
- `GET /vault/{namespace}` — استرجاع entries (مع 404 سليم)

### 4. 🩺 key_doctor
قسم جديد "QUOTA LEDGER" يعرض حصص اليوم + lifetime.

## 📊 النتائج (المُتحقق منها بالليدجر كحكم)
```yaml
قبل: 522 passed / 50s / 14 تسريب LLM في الهيكلية
بعد: 545 passed / 14s / صفر تسريب (± 28 تست ليدجر جديد)
LLM smoke: 2 live tests passed (agent_judge + benchmark health)
تكلفة اليوم كله: $0.0036 (56 محاولة مسجلة)
اكتشاف جانبي: OpenRouter free models شغالة رغم الرصيد السالب (33 ok)
```

## 🔑 حالة المفاتيح (key doctor)
- OpenRouter: 11 مفتاح رصيد سالب — لكن :free models بتشتغل أحياناً
- GitHub Models: ✅ الحصان الشغّال (120/يوم في الليدجر)
- Google: 9 مفاتيح كوتة خلصانة (بترجع يومياً)
- Serper: شغال (حصة 60/يوم في الليدجر)

## Next candidates
- ربط ResearchDiscovery بالـ Self-Evolve loop (يتعلم من الأوراق)
- صفحة UI للـ quota + vault
- Google keys لما الكوتة ترجع → live gemini smoke
- تشديد xfail markers للـ 53 xpassed
