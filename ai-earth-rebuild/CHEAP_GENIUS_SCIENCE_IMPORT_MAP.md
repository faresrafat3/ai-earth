# Cheap Genius — Science Import Map

## الفكرة

لا نبني العلم من الصفر. نأخذ من مجالات ناضجة:

- adaptive inference
- model routing
- cascades
- selective prediction
- uncertainty quantification
- value of information
- cost-sensitive decision theory
- ensemble theory
- frugal computing
- evidence retrieval

ثم نركبها في مشروع واحد:

> Cost-Aware Adaptive Inference Router

## الأطروحة الجديدة

بدل:

> AI Earth يجمع أبحاث الذكاء كقطع LEGO.

نقول:

> Cheap Genius يصرف الذكاء تدريجيًا: يبدأ بأرخص إشارة كافية، ويصعّد فقط إذا كانت قيمة المعلومة الإضافية أعلى من تكلفتها.

## المجالات المستوردة

| المجال | ما نستورد منه |
|---|---|
| Model Cascades | small → medium → large escalation |
| Dynamic Routing | اختيار الموديل/الاستراتيجية حسب السؤال |
| Sequential Decision Making | stop / continue / escalate |
| Value of Information | هل العينة أو الموديل الأغلى يستحق؟ |
| Selective Prediction | أجب فقط عند الثقة؛ وإلا صعّد |
| Ensemble Theory | متى التصويت يفيد ومتى يضخم الخطأ |
| Uncertainty Quantification | entropy, disagreement, confidence, calibration |
| Cost-Sensitive Learning | accuracy per dollar / latency per correct |
| Evidence Retrieval | search/scrape only when needed |

## معمارية MVP

1. cheap answer
2. k0=3 cheap probes
3. early stability / disagreement check
4. if stable: return
5. if unstable: escalate to one of:
   - SC@10
   - stronger model
   - cross-family verifier
   - search + scrape
   - human/manual review later

## لماذا هذا قوي؟

لأنه layer فوق كل النماذج، وليس موديل جديدًا.

ينفع مع:

- OpenRouter
- Gemini
- Mistral
- NVIDIA NIM
- SiliconFlow/Qwen/DeepSeek
- Serper/Firecrawl
- Cloudflare Gateway

## التجارب تصبح validation فقط

لا نستخدم التجارب لاختراع العلم، بل لاختبار policy محليًا:

- هل route يقلل cost؟
- هل يحافظ على accuracy؟
- هل يقلل latency؟
- هل يعرف متى يصعّد؟

## أول تجربة منتجية

EXP14 — Early Topology Routing Policy

مقارنة:

1. single sample always
2. always SC@10
3. adaptive route:
   - k0=3
   - if unanimous: stop
   - else complete to SC@10

المقياس:

- accuracy
- generations per correct
- token cost per correct
- latency per correct

## الاسم المقترح

AI Earth: Cheap Genius

أو ببساطة:

Cheap Genius Router

## الشعار

> Spend intelligence only when uncertainty earns it.

بالعربي:

> اصرف الذكاء الغالي فقط عندما يثبت الرخيص أنه غير كافٍ.
