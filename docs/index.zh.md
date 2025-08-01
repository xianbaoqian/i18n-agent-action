# 为什么我们需要这个工具

在KCD 2025北京大会和Community Over Code 2025中国会议上经过讨论后，我们最终决定开发一个代理程序来处理社区的国际化和本地化(i18n)工作。  
就我个人而言，我无法同时处理[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025会议的相关工作。

# 这是一个AI代理程序
## 使用方法
### 手动模式(适用于开发人员，请注意安全风险，因为这不是在沙箱中运行)
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
完成后您需要自行运行代码检查。

### 容器模式(在沙箱中运行)
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
### GitHub Actions工作流
建议您在项目设置中启用PR自动创建功能。

#### 首次初始化
```
name: 手动i18n处理及PR创建

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # 允许手动触发

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # 使用当前分支或main分支
          fetch-depth: 0  # 获取所有历史记录以便创建分支

      - name: 使用本Action
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action

      - name: 创建Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: "自动i18n处理(GHA)"
          body: "此PR为您完成国际化处理"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```
#### 每次PR后的处理
```
name: 处理变更的Markdown文件

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

      - name: 获取变更的markdown文件(排除所有i18n变体)
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # 匹配所有语言变体

      - name: 打印并使用变更文件
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo "变更的markdown文件(排除所有i18n变体):"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: 使用本Action
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action
          FILE_LIST: ${{ steps.changed-files.outputs.all_changed_files }}

      - name: 创建Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: "自动i18n处理(GHA)"
          body: "此PR为您完成国际化处理"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```  

## 输入参数
| 输入参数 | 是否必填 | 默认值 | 描述 |
|-----------------|----------|---------------|-------------|
| `apikey` | 是 | - | LLM服务的API密钥 |
| `base_url` | 否 | DeepSeek | LLM服务的端点URL |
| `model` | 否 | DeepSeek v3 | LLM服务的模型名称/标识符 |
| `RESERVED_WORD` | 是 | - | 翻译时需要保留的术语/短语 |
| `DOCS_FOLDER` | 是 | - | 文档文件夹路径 |
| `CONFIG_FILE` | 是 | - | 项目i18n设置的配置文件 |
| `FILE_LIST` | 否 | - | 要处理的特定文件列表(可选) |
| `workspace` | 是 | - | 代码仓库工作区路径 |
| `target_language` | 否 | `'zh'` | 目标语言代码(如`'zh'`表示中文) |
| `max_files` | 否 | `'20'` | 最大处理文件数量 |
| `dryRun` | 否 | false | 启用试运行模式(模拟执行而不实际修改) |

## 已适配的社区/项目
- 本项目(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- kepler项目

## 不在范围的功能
- 代码检查(lint)
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.