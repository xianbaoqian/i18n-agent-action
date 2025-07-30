# Why we have this
It was discussed on KCD 2025 BeiJing, Community Over Code 2025 China and we finally dicede to make an agent to handle i18n works for community.
As for me, I can't parallel in [https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175) and Community Over Code 2025's session.

## Try with my own Principles of Agent Development

#### Inference 1: If the task is relatively fixed and there is a reliable solution, there is no need to call on a large model to take risks.

#### Inference 2: The tasks are not fixed, and adapting them one by one is too complex. The big model has a certain universality, and we need to make good use of this universality and entrust it to the big model.

#### Inference 3: The task is not fixed and can be adapted one by one, depending on the actual situation. If using a large model, it is necessary to consider the situation where the large model answers incorrectly and handle the errors accordingly.

#### Inference 4: The task is fixed and there is no reliable solution. If using a large model to attempt creative solutions, manual intervention is required.

# As it's an AI Agent
## How it works
### Manual(for dev, or you should take your own security as it not running in sandbox)
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
and you shoud run linting by yourself.

### Container(running in sandbox)
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
I suggest you enable PR creation in project settng to make auto PR back.

#### 1st init
```
name: Manual i8n and PR Creation

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # 允许手动触发

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # 使用当前分支或main分支
          fetch-depth: 0  # 获取所有历史记录以便创建分支

      - name: Use this Action
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: "auto i18n with GHA"
          body: "This PR do i18n for you"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```
#### after each PR
```
name: Process Changed Markdown Files

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

      - name: Get changed markdown files (excluding all i18n variants)
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # 匹配所有语言变体

      - name: Print and use changed files
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo "Changed markdown files (excluding all i18n variants):"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: Use this Action
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action
          FILE_LIST: ${{ steps.changed-files.outputs.all_changed_files }}

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: "auto i18n with GHA"
          body: "This PR do i18n for you"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # 目标分支
          draft: false
```  

## Inputs
| Item |	Description |
| --- | --- | 
| CONFIG_FILE	| Configuration file to your i18n setting |
| base_url  | LLM service endpoint   |
| apikey	| LLM service API key |
| model |	LLM model (to be specific) |
| DOCS_FOLDER	| In case of LLM missing a path |
| RESERVED_WORD	| Reserved word |
| FILE_LIST |	Optional specific file (if you have a file list for i18n task) |

## Adption communtiy/project
- itself(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- kepler

## Not in scope
- lint