# التقييم الذاتي

بفضل الورقة البحثية 2507.21046v3

## التصميم

لجعل وكيل الترجمة الخاص بنا يُقيّم ذاته، يمكننا تجربة الكشف التلقائي عن الأسماء الصحيحة.

طلب السحب (PR) لهذا المستودع في [الرابط](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

الفكرة الأساسية هي أن المطالبة تحتوي على جزء ديناميكي مثل الأسماء الصحيحة، ماذا لو طلبنا من LLM الكشف تلقائيًا عن أسماء صحيحة جديدة ودمجناها معًا في الجولة/الجزء التالي من المهام؟

### الخطوة الأولى: إضافة متغير لالتقاط الأسماء الصحيحة من LLM

تم الاختبار باستخدام [diffuser](https://github.com/huggingface/diffusers/pull/12179)

من السجل، نرى الأسماء الصحيحة المكتشفة كـ
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`

التي يمكننا بدء الخطوة الثانية بها كدمج الأسماء الصحيحة كـ reserved_word.

### الخطوة الثانية: دمج الأسماء الصحيحة و reserved word

ها هي عينة تنفيذ الدالة لدمج الأسماء الصحيحة (كاستجابة من LLM) و reserved word

```python
def MergePN(str1, str2):
    # تقسيم وإزالة التكرار مع الحفاظ على الترتيب
    merged = list(OrderedDict.fromkeys(
        [item.strip() for item in str1.split(",")] + 
        [item.strip() for item in str2.split(",")]
    ))

    result = ", ".join(merged)
    return result
```

### النتيجة

![](./img/selfevaluate.png)
![](./img/selfevaluate2.png)