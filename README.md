# i18n-agent-action

[![GitHub Super-Linter](https://github.com/actions/hello-world-docker-action/actions/workflows/linter.yml/badge.svg)](https://github.com/super-linter/super-linter)
![CI](https://github.com/actions/hello-world-docker-action/actions/workflows/ci.yml/badge.svg)
[![Deploy Docs](https://github.com/SamYuan1990/i18n-agent-action/actions/workflows/deploy.yml/badge.svg)](https://github.com/SamYuan1990/i18n-agent-action/actions/workflows/deploy.yml)
[![image](https://github.com/SamYuan1990/i18n-agent-action/actions/workflows/image.yml/badge.svg)](https://github.com/SamYuan1990/i18n-agent-action/actions/workflows/image.yml)

## UX todo
- [ ] report as how many docs, tokens been used

## In scope and not in scope, and how it works.

> Don't want to rebuild the wheel.
- Trigger is not in scope
	- leave to manual for full refresh or diff action
  - model api and model endpoint
  > people can select any LLM service with openAI API?
	- config entry point
  > We need to know the default language and what languages are the target, it's in the config file.

--- scope ---
- Phase one: from configuration file
> Sam at 2025 July: I don't want LLM to scan the project, as token cost or it may wrong. Just ask document maintainer to give the i18n configuration file, the manual point to configuration file will be 100% correct to i18n config.

- language scope, how to get language scope?
	- = consume config files to get language list.
	- = default language - existing language(a file diff)

- save result to the specific file
> Sam at 2025 July: after we have translation scope, we also need to have naming rules from configuration files.(or maybe ask LLM to notice that)

-- end of here: get a list for source file, translate target, language.
> Sam at 2025 July: as result of this phase, we need to have a clear scope for all the tasks.

-- Phase two, A for loop here to translate
- Translate ask LLM for help
	- how to get a glossary for content mapping?
	- Gaps?(or just refresh all)

> Sam at 2025 July: to be specific.

--- not in scope ---
- create PR leave to PR Action

> Don't want to rebuild the wheel. as there are PR actions already to open PR for change.

## Usage
to be specific, but considering with 12 factors agent, it supports local run in terminal, container or CI.

### Manual(for dev, or you should take your own security as it not running in sandbox)
```bash
pip3 install...
export api_key={your_key}
## python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
## run repo itself
python3 main.py ./mkdocs.yml ./docs i18n-agent-action ./docs/index.md
```

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

## Outputs
- Files.
- Trace Logs, in console

## Adption communtiy/project
- itself(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- kepler

## Test Locally same as usage.manual
