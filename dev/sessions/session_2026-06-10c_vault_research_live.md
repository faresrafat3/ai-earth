# 🧠 Session 2026-06-10c — Vault Memory + Live Research Discovery
# ══════════════════════════════════════════════════════════════════════
# التاريخ: 2026-06-10
# النسخة: v2.5.0 → v2.6.0
# الحدث المحوري: البيئة اتصفّرت بالكامل بسبب pytest معلّق نص ساعة
# ══════════════════════════════════════════════════════════════════════

---

## ⚠️ الكارثة والدرس

```yaml
ما حدث:
  - آخر أمر في السيشن السابقة (pytest كامل بدون timeout خارجي) علّق ~30 دقيقة
  - المستخدم لا يملك وسيلة لإيقاف أي عملية معلّقة
  - النتيجة: الـ sandbox اتصفّر بالكامل (حتى Python رجع 3.10 بدل 3.13)
  - كل ما لم يُدفع إلى GitHub كان سيضيع — الحمد لله آخر push كان شاملاً

القواعد الذهبية (إلزامية من الآن):
  1. كل أمر bash يتغلف بـ `timeout -k N SECONDS ...` — بلا استثناء
  2. pytest دائماً عبر pytest.ini (timeout=90/test, session_timeout=1200)
  3. commit + push بعد كل مكوّن مكتمل — الشغل لا يقعد ساعة بدون push
  4. الاسترجاع بعد التصفير = bash scripts/bootstrap.sh (كل خطوة bounded)
  5. .env خارج git — يُعاد إنشاؤه يدوياً بعد كل تصفير (القائمة مع المستخدم)
```

## 🔄 الاسترجاع (تم في ~6 دقائق)

```yaml
1. git clone من GitHub (v2.5.0 سليمة — 3.6s)
2. إعادة إنشاء .env (21 مفتاح: 11 OpenRouter + 1 GitHub + 9 Google + Serper)
3. pip install -r requirements.txt (142s bounded)
4. pytest -m "not llm" → 475 passed في 57s ✅
5. LLM smoke → real chat في 2.6s ✅
```

---

## 🧱 الجديد في v2.6.0

### 1. 🛡️ scripts/bootstrap.sh
```yaml
الغرض: استرجاع بيئة كاملة بأمر واحد بعد أي تصفير
الضمانات: كل خطوة لها timeout صارم — يستحيل أن يعلّق
الخطوات: env check → pip (1700s) → boot check (60s) → fast suite (950s)
```

### 2. 🧠 MemoryVault (ai_earth/memory/vault.py — 269 سطر)
```yaml
الفكرة: ذاكرة دائمة "تنجو من تصفير البيئة" لأنها JSON داخل الريبو نفسه
المسار: data/vault/<namespace>.json — يتدفع مع git push
الضمانات:
  - كتابة ذرّية (tmp + os.replace) — قتل العملية لا يفسد الملف
  - bounded (500 entry/namespace كحد أقصى — الريبو لا ينتفخ)
  - ملف تالف → .bak + بداية نظيفة (لا crash أبداً)
  - thread-safe
API: remember/recall/latest/search/forget/clear/namespaces/stats/export_markdown
Integration:
  - SelfEvolveCore(vault=v) → learnings تُحفظ تلقائياً وتُسترجع عند الإقلاع
  - vault معطوب لا يكسر الـ evolution أبداً (non-fatal دائماً)
الاختبارات: 30 (كلها هيكلية، tmp_path — لا تلوث الـ vault الحقيقي)
```

### 3. 🔭 ResearchDiscovery Live (rewrite كامل — 288 سطر)
```yaml
الفكرة: خط تجميع الذكاء الحي — قلب رسالة المنصة
Pipeline: Serper search → crawl → LLM summarize (budgeted) → vault persist
إصلاحات جوهرية:
  - BUG: router.crawl() لم تكن موجودة → أضيفت لـ ModelRouter
  - فلسفة: crawl_url كانت ترجع "Simulated content" عند الفشل → الآن ""
    (صدق كامل — ممنوع أي محتوى مزيف في المنصة)
الأوضاع (بدون أي mock):
  - llm=True  → ملخصات LLM حقيقية (mode="llm")
  - llm=False → mode="structural" بعلامة صريحة (صفر calls)
  - نفاد الميزانية → mode="budget_exhausted" بعلامة صريحة
  - فشل crawl → mode="crawl_failed" بصدق
الميزانية: max_llm_calls (افتراضي 4) — سقف صارم لا يُتجاوز
الاختبارات: 16 هيكلية (fake IO محقون) + 2 live (@llm)
```

### 4. 🔬 إثبات حي (في الريبو فعلاً)
```yaml
أول عملية تجميع ذكاء حقيقية دخلت data/vault/discoveries.json:
  - arXiv 2508.07407 — A Comprehensive Survey of Self-Evolving AI Agents
  - arXiv 2507.21046 — A Survey of Self-Evolving Agents
التكلفة: $0.000693 | الوقت: 13.1s | llm_calls: 2/2 (البجت انضبط)
ملاحظة تشغيلية: مفتاح openrouter_1 (ahmed) رجّع 402 (رصيد خلص)
→ الـ pool عمل rotation تلقائي للمفتاح التالي بدون أي توقف ✅
```

---

## 📈 الحالة بعد الجلسة

```yaml
الإصدار: 2.6.0
الاختبارات: 475+48 هيكلية خضراء + 21 @llm (منهم 2 جديدة)
مفاتيح حية: 20/21 (openrouter_1 خلص رصيده — تمت ملاحظته)
Next candidates:
  - /research + /vault endpoints في api.py + صفحة UI
  - ربط ResearchDiscovery بالـ Self-Evolve loop (يتعلم من الأوراق الجديدة)
  - live-LLM benchmark category صغيرة
  - تشديد xfail markers للـ 53 xpassed
```

_هذا الملف يوثق Session 2026-06-10c_
