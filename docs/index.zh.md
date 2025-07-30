# 为什么我们要做这个

在KCD 2025北京大会和Community Over Code 2025中国峰会上经过讨论，我们最终决定开发一个代理来处理社区的国际化工作。就我个人而言，我无法同时并行处理[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025分会场的工作。

## 基于我的智能体开发原则进行尝试

#### 推论1：如果任务相对固定且有可靠解决方案，就不需要调用大模型来承担风险。

#### 推论2：任务不固定，逐个适配过于复杂。大模型具有一定通用性，我们需要善用这种通用性并将其委托给大模型。

#### 推论3：任务不固定但可以逐个适配，需根据实际情况判断。如果使用大模型，必须考虑大模型回答错误的情况并进行错误处理。

#### 推论4：任务固定但没有可靠解决方案。如果使用大模型尝试创造性解决方案，则需要人工干预。

# 作为AI智能体
## 工作原理
### 手动模式（开发者使用，请注意安全，因其不在沙箱中运行）
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
注意：您需要自行运行代码检查。

### 容器模式（在沙箱中运行）
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

### GitHub Action
建议您在项目设置中启用PR自动创建功能以实现自动回传PR。

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
          title: "通过GHA自动国际化"
          body: "本PR为您完成国际化处理"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```

#### 每次PR后
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

      - name: 获取变更的markdown文件（排除所有国际化变体）
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
          echo "变更的markdown文件（排除所有国际化变体）："
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
          title: "通过GHA自动国际化"
          body: "本PR为您完成国际化处理"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```

## 输入参数
| 参数项 |	说明 |
| --- | --- | 
| CONFIG_FILE	| 国际化配置文件路径 |
| base_url  | 大语言模型服务端点   |
| apikey	| 大语言模型API密钥 |
| model |	大语言模型名称（具体指定） |
| DOCS_FOLDER	| 文档目录路径（防止LLM遗漏路径） |
| RESERVED_WORD	| 保留字段 |
| FILE_LIST |	可选指定文件列表（如果有需要国际化的特定文件清单） |

## 适配社区/项目
- 本项目自身(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- kepler项目

## 不在范围内
- 代码检查