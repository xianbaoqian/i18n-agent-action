# 为什么我们会有这个
在KCD 2025北京、Community Over Code 2025中国上讨论后，我们最终决定制作一个代理来处理社区的i18n工作。
对我来说，我无法同时在[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025的会议上并行工作。

## 尝试我自己的代理开发原则

#### 推论1：如果任务相对固定且有可靠的解决方案，就没有必要调用大模型来冒险。

#### 推论2：任务不固定，逐个适应太复杂。大模型有一定的通用性，我们需要好好利用这种通用性，并将其委托给大模型。

#### 推论3：任务不固定，可以根据实际情况逐个适应。如果使用大模型，需要考虑大模型回答错误的情况并相应处理错误。

#### 推论4：任务固定但没有可靠的解决方案。如果使用大模型尝试创造性解决方案，需要人工干预。

# 因为它是一个AI代理
## 它是如何工作的
### 手动（适用于开发，或者你应该自行承担安全责任，因为它不在沙箱中运行）
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
并且你应该自己运行linting。

### 容器（在沙箱中运行）
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
我建议你在项目设置中启用PR创建以自动PR返回。

#### 第一次初始化
```
name: 手动i8n和PR创建

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

      - name: 使用此Action
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
          title:
使用GHA自动进行国际化（i18n）
          body: "此PR为您完成国际化"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```
#### 每次PR之后
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

      - name: 获取变更的markdown文件（不包括所有i18n变体）
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # 匹配所有语言变体

      - name: 打印并使用变更的文件
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo
变更的markdown文件（不包括所有i18n变体）:
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: 使用此Action
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
          title: "使用GHA自动进行国际化"
          body: "此PR为您完成国际化"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false

## 输入
| 输入参数 | 是否必需 | 默认值 | 描述 |
|-----------------|----------|---------------|-------------|
| `apikey`        | 是      | -             | LLM服务的API密钥 |
| `base_url`      | 否       | DeepSeek             | LLM服务的端点URL |
| `model`         | 否       | DeepSeek v3            | LLM服务的模型名称/标识符 |
| `RESERVED_WORD` | 是      | -             | 从翻译中排除的保留术语/短语 |
| `DOCS_FOLDER`   | 是      | -             | 您的文档文件夹路径 |
| `CONFIG_FILE`   | 是      | -             | 项目国际化设置的配置文件 |
| `FILE_LIST`     | 否       | -             | 要处理的特定文件列表（可选） |
| `workspace`     | 是      | -             | 您的代码仓库工作空间路径 |
| `target_language` | 否     | `'zh'`        | 翻译的目标语言代码（例如，`'zh'`表示中文） |
| `max_files`     | 否       | `'20'`        | 处理的最大文件数量 |
| `dryRun`        | 否       | false             | 启用dry-run模式（模拟执行而不做任何更改） |

## 测试完成
muntiy/项目
- 自身(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- HAMi

## 不在范围内
- lint
 免责声明：此内容由i18n-agent-action与LLM服务https://api.deepseek.com使用模型deepseek-chat提供，出于某些原因（例如，我们不是母语者），我们使用LLM为您提供此翻译。如果您发现任何需要更正的地方，请提交问题或向github提出PR，并切换回默认语言。
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.