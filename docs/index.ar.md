# لماذا لدينا هذا
بعد المناقشة في KCD 2025 بكين وCommunity Over Code 2025 الصين، قررنا في النهاية إنشاء وكيل للتعامل مع أعمال i18n للمجتمع.
بالنسبة لي، لا يمكنني العمل في نفس الوقت على [https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175) وفي اجتماعات Community Over Code 2025.

## تجربة مبادئ تطوير الوكيل الخاصة بي

#### الاستنتاج 1: إذا كانت المهمة ثابتة نسبيًا ولديها حل موثوق، فلا داعي لاستدعاء نموذج كبير للمخاطرة.

#### الاستنتاج 2: المهمة غير ثابتة، والتكيف مع كل حالة على حدة معقد جدًا. النموذج الكبير لديه قدر معين من العمومية، نحن بحاجة إلى الاستفادة الجيدة من هذه العمومية وتفويضها للنموذج الكبير.

#### الاستنتاج 3: المهمة غير ثابتة، يمكن التكيف مع كل حالة على حدة وفقًا للواقع. إذا تم استخدام نموذج كبير، يجب النظر في حالة الخطأ في إجابة النموذج الكبير ومعالجة الخطأ وفقًا لذلك.

#### الاستنتاج 4: المهمة ثابتة ولكن لا يوجد حل موثوق. إذا تم استخدام نموذج كبير لمحاولة حل إبداعي، هناك حاجة إلى تدخل بشري.

# لأنه وكيل ذكاء اصطناعي
## كيف يعمل
### يدويًا (مناسب للتطوير، أو يجب عليك تحمل مسؤولية السلامة بنفسك، لأنه لا يعمل في بيئة معزولة)
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
ويجب عليك تشغيل linting بنفسك.

### حاوية (تعمل في بيئة معزولة)
```
docker run -it \
  -v path_to_your_repo:/workspace \
  -e model="deepseek-chat" \
  -e base_url="https://api.deepseek.com" \
  -e api_key="..." \
  -e CONFIG_FILE="/workspace/mkdocs.yml" \
  -e DOCS_FOLDER="/workspace/docs" \
  -e RESERVED_WORD="i18n-agent-action" \
  -e FILE_LIST="/workspace/docs/index.md" \
  ghcr.io/samyuan1990/i18n-agent-action:latest
```
### GHA
أوصي بتمكين إنشاء PR في إعدادات المشروع لإنشاء PR تلقائيًا.

#### التهيئة الأولى
```
name: i8n يدوي وإنشاء PR

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # يسمح بالتشغيل اليدوي

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: تحقق من الكود
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # استخدم الفرع الحالي أو الفرع الرئيسي
          fetch-depth: 0  # احصل على كل التاريخ لإنشاء فرع

      - name: استخدم هذا الإجراء
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action

      - name: إنشاء طلب سحب
        uses: peter-evans/create-pull-request@v7
        with:
          title:
استخدام GHA لأتمتة i18n
          body: "هذا PR يكمل i18n لك"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # الفرع الهدف
          draft: false
```
#### بعد كل PR
```
name: معالجة ملفات Markdown المتغيرة

permissions:
  contents: write
  pull-requests: write

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**/*.md'

jobs:
  process-markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: الحصول على ملفات markdown المتغيرة (باستثناء جميع متغيرات i18n)
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # تطابق جميع متغيرات اللغة

      - name: طباعة واستخدام الملفات المتغيرة
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo
ملفات markdown التي تم تغييرها (لا تشمل جميع المتغيرات i18n):
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: استخدام هذا الإجراء
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action
          FILE_LIST: ${{ steps.changed-files.outputs.all_changed_files }}

      - name: إنشاء طلب سحب
        uses: peter-evans/create-pull-request@v7
        with:
          title: "استخدام GHA للتلقائية الدولية"
          body: "هذا PR يكمل عملية الدولية لك"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # الفرع الهدف
          draft: false

## الإدخال
| معامل الإدخال | مطلوب | القيمة الافتراضية | الوصف |
|-----------------|----------|---------------|-------------|
| `apikey`        | نعم      | -             | مفتاح API لخدمة LLM |
| `base_url`      | لا       | DeepSeek             | عنوان URL لنقطة نهاية خدمة LLM |
| `model`         | لا       | DeepSeek v3            | اسم/معرف نموذج خدمة LLM |
| `RESERVED_WORD` | نعم      | -             | المصطلح/العبارة المحجوزة المستثناة من الترجمة |
| `DOCS_FOLDER`   | نعم      | -             | مسار مجلد المستندات الخاص بك |
| `CONFIG_FILE`   | نعم      | -             | ملف التكوين لإعدادات الدولية للمشروع |
| `FILE_LIST`     | لا       | -             | قائمة ملفات محددة للمعالجة (اختياري) |
| `workspace`     | نعم      | -             | مسار مساحة العمل لمستودع الكود الخاص بك |
| `target_language` | لا     | `'zh'`        | كود اللغة الهدف للترجمة (مثال، `'zh'` للصينية) |
| `max_files`     | لا       | `'20'`        | الحد الأقصى لعدد الملفات للمعالجة |
| `dryRun`        | لا       | false             | تمكين وضع dry-run (تنفيذ محاكاة دون إجراء أي تغييرات) |

## اختبار مكتمل
muntiy/المشروع
- نفسه(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- HAMi

## خارج النطاق
- lint
 إخلاء مسؤولية: هذا المحتوى مدعوم بـ i18n-agent-action مع خدمة LLM https://api.deepseek.com مع نموذج deepseek-chat، لسبب ما، (على سبيل المثال، نحن لسنا متحدثين أصليين) نستخدم LLM لتوفير هذه الترجمة لك. إذا وجدت أي تصحيحات، يرجى تقديم مشكلة أو رفع PR مرة أخرى إلى github، والعودة إلى اللغة الافتراضية.
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.