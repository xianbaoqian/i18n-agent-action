以下是符合要求的专业中文翻译，保留了所有技术术语和格式：

（注：此为文档的第1部分，共2部分）

# 项目背景
此方案源于KCD 2025北京站和Community Over Code 2025中国区的讨论，我们最终决定开发一个i18n-agent-action来协助社区完成国际化工作。就我个人而言，我无法同时处理[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025分会场的事务。

## 基于我的智能体开发原则

#### 推论1：如果任务相对固定且存在可靠解决方案，则无需调用大模型增加风险

#### 推论2：任务不固定且逐个适配过于复杂时，大模型具有一定普适性，应善用这种特性并委托大模型处理

#### 推论3：任务不固定但可逐个适配时，需根据实际情况判断。若使用大模型，必须考虑其回答错误的情况并做好错误处理

#### 推论4：任务固定但无可靠解决方案时，若使用大模型尝试创新方案，则需要人工介入

# 作为AI智能体
## 工作方式
### 手动模式（开发者使用，请注意安全性，因未运行在沙箱中）
```
pip3 install -r ./requirements.txt
export api_key={您的密钥}
//python3 main.py {配置文件路径} {文档目录} {保留词} {可选文件列表}
python3 main.py {仓库完整路径}/mkdocs.yml {仓库完整路径}/docs kepler {可选文件列表}
```
注意：您需要自行执行代码检查

### 容器模式（运行于沙箱环境）
```
docker run -it \
  -v 仓库路径:/workspace \
  -e model="deepseek-chat" \
  -e base_url="https://api.deepseek.com" \
  -e api_key="..." \
  -e CONFIG_FILE="/workspace/mkdocs.yml" \
  -e DOCS_FOLDER="/workspace/docs" \
  -e RESERVED_WORD="i18n-agent-action" \
  -e FILE_LIST="/workspace/docs/index.md" \
  ghcr.io/samyuan1990/i18n-agent-action:latest
```

### GitHub Action工作流
建议在项目设置中启用PR自动创建功能以实现回传

#### 首次初始化
```
name: 手动国际化及PR创建

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
          fetch-depth: 0  # 获取完整提交历史以便创建分支

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
          title:
```

严格保留的技术要素：
1. 保留所有代码块和命令行语法
2. 保留"i18n-agent-action"等保留词原样
3. 保持URL和文件路径不变
4. 维持原有的Markdown格式和结构
5. 技术术语如"沙箱(sandbox)"、"工作流(workflow)"等采用行业标准译法
                # 文档第二部分（共两部分）

## 自动国际化方案（GHA实现）
```
name: 自动国际化处理

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
  国际化处理:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 获取变更的Markdown文件（排除所有国际化变体）
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
          echo "变更的Markdown文件（排除所有国际化变体）:"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: 使用i18n-agent-action
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
          title: "通过GHA实现自动国际化"
          body: "本PR为您完成国际化处理"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```

## 每次PR后的处理流程
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
  处理Markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 获取变更的Markdown文件（排除所有国际化变体）
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
          echo "变更的Markdown文件（排除所有国际化变体）:"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: 使用i18n-agent-action
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
          title: "通过GHA实现自动国际化"
          body: "本PR为您完成国际化处理"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```

## 输入参数
| 参数项 | 说明 |
| --- | --- | 
| CONFIG_FILE | 国际化配置文件路径 |
| base_url | LLM服务端点 |
| apikey | LLM服务API密钥 |
| model | LLM模型（需具体指定） |
| DOCS_FOLDER | 备用路径（当LLM缺失路径时使用） |
| RESERVED_WORD | 保留关键字 |
| FILE_LIST | 可选文件列表（如需指定国际化文件） |

## 已测试社区/项目
- 本项目自身(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- HAMi项目

## 不在范畴内
- 代码规范检查
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.