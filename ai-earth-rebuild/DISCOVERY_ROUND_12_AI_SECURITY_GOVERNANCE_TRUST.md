# Discovery Round 12 — AI Safety / Security / Governance / Trust

## الهدف

استكشاف محور الثقة والأمان والحوكمة في AI وخصوصًا agents:

- prompt injection
- tool misuse
- memory poisoning
- agent identity/privilege
- supply chain
- auditability
- runtime governance
- EU AI Act / NIST / ISO
- cost governance

هذا المحور مهم لأن أي مشروع AI يُستخدم في الإنتاج سيُسأل: هل هو آمن؟ قابل للتدقيق؟ محكوم؟

---

# Online Round — مصادر واتجاهات

## 1. OWASP Top 10 for Agentic Applications 2026

مصادر:

- https://dev.to/alessandro_pignati/the-owasp-top-10-for-ai-agents-your-2026-security-checklist-asi-top-10-cck
- https://www.paloaltonetworks.com/blog/cloud-security/owasp-agentic-ai-security/

المخاطر تشمل:

- Agent Goal Hijack
- Tool Misuse
- Identity & Privilege Abuse
- Agentic Supply Chain
- Unexpected Code Execution
- Memory & Context Poisoning
- Insecure Inter-Agent Communication
- Cascading Failures
- Human-Agent Trust Exploitation
- Rogue Agents

**الأثر:** agentic security أصبح framework رسمي، وليس مجرد قلق نظري.

---

## 2. AI Agent Security Checklist 2026

الرابط: https://iternal.ai/ai-agent-security-checklist

يربط OWASP Agentic AI بـ NIST وCISA وMITRE ATLAS، ويؤكد أن prompt injection لا يمكن منعه بالكامل؛ المطلوب هو blast-radius control.

**الأثر:** الأمن الحقيقي ليس فلترة prompt، بل least privilege + provenance + sandboxing + monitoring.

---

## 3. Prompt Injection Attacks in AI Agents

الرابط: https://atlan.com/know/prompt-injection-attacks-ai-agents/

يوضح أن prompt injection بنيوي لأن النموذج لا يفصل طبيعيًا بين data وinstruction. RAG يزيد الخطر لأن أي document قد يحمل تعليمات خبيثة.

**الأثر:** كل Evidence/RAG system يحتاج context governance.

---

## 4. Agentic AI Security Threats

الرابط: https://www.lasso.security/blog/agentic-ai-security-threats-2025

يركز على memory poisoning, tool misuse, privilege compromise كأعلى مخاطر agents.

**الأثر:** memory وtools هما أخطر من output text.

---

## 5. OWASP Agentic AI Roadmap / Enterprise Security

الرابط: https://repello.ai/blog/owasp-agentic-ai-top-10-enterprise-security-roadmap-for-2026

يوثق incidents مثل EchoLeak, ForcedLeak, Amazon Q supply-chain attack, ChatGPT Operator injection.

**الأثر:** الهجمات ليست افتراضية؛ production systems تعرضت.

---

## 6. GenAI Security / OWASP LLM Top 10

الرابط: https://www.vectra.ai/topics/genai-security

يغطي LLM risks:

- prompt injection
- sensitive information disclosure
- supply chain
- data/model poisoning
- improper output handling
- excessive agency
- vector/embedding weaknesses
- unbounded consumption

---

## 7. AI Governance Framework 2026

الرابط: https://www.elementum.ai/blog/ai-governance-framework

يشرح NIST AI RMF, EU AI Act, ISO 42001. يذكر أن معظم المؤسسات لا تملك governance ناضجة رغم انتشار AI.

**الأثر:** compliance/governance layer فرصة حقيقية.

---

## 8. AI Governance for Enterprise Agents

الرابط: https://www.ruh.ai/blogs/ai-governance-enterprise-ai-agents-2026-compliance-playbook

يركز على أن enterprise agents تحتاج:

- data lineage
- human-in-loop checkpoints
- risk labels
- audit logs

---

## 9. AI Agent Governance Policy and Compliance

الرابط: https://www.digitalapplied.com/blog/ai-agent-governance-policy-compliance-2026

يربط EU AI Act, NIST, ISO, SOC2, GDPR. مهم لأنه يربط runtime logs بالمتطلبات القانونية.

---

## 10. AI Governance Tools 2026

الرابط: https://www.cloudzero.com/blog/ai-governance-tools/

يذكر أن governance تشمل:

- compliance
- security
- cost governance
- shadow AI
- model lifecycle

**الأثر:** cost governance أصبح جزءًا من AI governance، وليس مجرد FinOps.

---

# Offline Audit

## ما الحقيقي؟

1. Agent security خطر إنتاجي فعلي.
2. Prompt injection لا يحل بفلتر واحد.
3. Memory poisoning وtool misuse أخطر من hallucination أحيانًا.
4. Governance ينتقل من policy docs إلى runtime controls.
5. EU AI Act/NIST/ISO تدفع الحاجة لـ audit logs وrisk management.
6. Cost governance جزء من الحوكمة.
7. RAG/context layers تحتاج provenance وallowlisting.

## ما الـ hype؟

1. “نحل prompt injection” مبالغة.
2. “guardrails تكفي” خطأ.
3. security vendors قد يبالغون في الخوف.
4. compliance tooling وحده لا يجعل النظام آمنًا.
5. monitoring بلا enforcement غير كافٍ.

---

# التحليل العميق

## 1. الثقة ليست eval فقط، بل control plane

Evaluation تقول هل خرجت إجابة جيدة.
Governance/Security تقول:

- هل كان مسموحًا للـ agent أن يفعل ذلك؟
- هل استخدم الأداة الصحيحة؟
- هل كشف بيانات؟
- هل نستطيع تفسير/إيقاف/rollback؟

هذا يضيف بعدًا جديدًا لفكرة Cheap Genius:

> لا يكفي أن route أرخص؛ يجب أن route آمن ومسموح.

## 2. RAG والذاكرة هما أخطر attack surfaces

لأنهما يزوّدان النموذج بـ “حقائق” وتعليمات من الخارج.

أي Evidence/Knowledge project يجب أن يتعامل مع:

- source trust
- content sanitization
- provenance
- memory write approval
- context isolation

## 3. Least Agency أهم من More Agency

بدل أن نعطي agent كل الأدوات، نستخدم:

- least privilege
- just-in-time permissions
- scoped credentials
- sandboxing
- approval gates

هذا يطابق فلسفتنا:

> أرخص/أقل تدخل كافٍ.

لكن هنا:

> أقل صلاحية كافية.

## 4. Governance فرصة منتجية لكنها enterprise-heavy

بيع governance كامل صعب.
لكن يمكن بناء أدوات صغيرة:

- AI action audit log
- tool permission analyzer
- memory write firewall
- RAG source trust scanner
- agent risk checklist

---

# Candidate Theses

## Thesis A — RAG/Memory Context Firewall

### المشكلة

RAG documents وagent memory قد تحتوي تعليمات خبيثة أو معلومات غير موثوقة.

### الأطروحة

> طبقة تفحص كل context قبل دخوله prompt/memory: source trust, injection risk, instruction/data separation, provenance.

### MVP

- input documents/chunks
- detect suspicious instructions
- label trusted/untrusted
- strip/quote unsafe content
- add provenance

### لماذا قوي؟

يتقاطع مع Evidence Engine وPersonal Memory وRAG.

---

## Thesis B — Agent Tool Permission Governor

### المشكلة

agents تستخدم tools بصلاحيات أوسع من اللازم.

### الأطروحة

> طبقة تحدد لكل tool/action: allowed? needs approval? sandbox? denied?

### MVP

- tool manifest
- action request
- policy check
- audit log

### يندمج مع

Agent Cost Governor / Runtime Layer.

---

## Thesis C — AI Action Audit Log

### المشكلة

لا توجد trace كافية تقول ماذا فعل الـ AI ولماذا.

### الأطروحة

> سجل موحد لكل AI action: prompt, context, tool, decision, permission, output, human approval.

### MVP

JSONL/SQLite + report.

### لماذا قوي؟

أساس governance وdebugging.

---

## Thesis D — Agent Risk Readiness Scanner

### المشكلة

الشركات تريد agents ولا تعرف المخاطر قبل النشر.

### الأطروحة

> scanner يقرأ agent design/config ويخرجه against OWASP Agentic Top 10.

### MVP

Input:

- tools list
- memory config
- data sources
- permissions
- workflow description

Output:

- risk report
- missing controls
- recommended mitigations

### سريع ومناسب.

---

## Thesis E — AI Governance Evidence Pack Generator

### المشكلة

الشركات تحتاج إثبات compliance: logs, policies, model cards, risk assessment.

### الأطروحة

> أداة تولد audit-ready evidence pack من traces/configs/evals.

### MVP

- ingest traces
- generate NIST/EU AI Act mapping summary
- risk/control matrix

### مخاطر

قانوني/امتثال يحتاج دقة.

---

# Scoring أولي

| Thesis | Intelligence | Cost Advantage | MVP Speed | Market Pain | Moat | Total |
|---|---:|---:|---:|---:|---:|---:|
| RAG/Memory Context Firewall | 5 | 4 | 4 | 5 | 5 | 23 |
| Agent Tool Permission Governor | 4 | 4 | 4 | 5 | 4 | 21 |
| AI Action Audit Log | 4 | 4 | 5 | 5 | 3 | 21 |
| Agent Risk Readiness Scanner | 4 | 4 | 5 | 4 | 3 | 20 |
| Governance Evidence Pack | 4 | 3 | 3 | 5 | 4 | 19 |

---

# أقوى Candidate من هذا المحور

# RAG/Memory Context Firewall

لأنه يربط محاور كثيرة:

- Evidence Engine
- RAG
- Personal Memory
- Agent Security
- Enterprise Governance

وهو wedge واضح:

> قبل أن يدخل أي content إلى context أو memory، افحص مصدره وخطره وصلاحيته.

---

# علاقة هذا بباقي المحاور

## مع Evidence Grounding

source trust وprovenance جزء من evidence.

## مع Personal Memory

memory write يجب أن يمر عبر firewall.

## مع Enterprise Workflows

tool/action permissions تحتاج governor.

## مع Cheap Genius Runtime

routing يجب أن يراعي ليس فقط cost، بل risk.

---

# الخلاصة العميقة

الأمان يضيف بعدًا خامسًا لكل سياساتنا:

ليس فقط:

```text
accuracy / cost / latency / confidence
```

بل:

```text
risk / permission / provenance / blast radius
```

أي route لا يجب أن يكون الأرخص فقط، بل:

> أرخص route مسموح وآمن وكافٍ.

---

# Candidate مضافة

نضيف إلى Top Candidates:

1. RAG/Memory Context Firewall
2. Agent Tool Permission Governor
3. AI Action Audit Log

ولا نقرر بعد.
