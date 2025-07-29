# i18n-agent-action

[![GitHub Super-Linter](https://github.com/actions/hello-world-docker-action/actions/workflows/linter.yml/badge.svg)](https://github.com/super-linter/super-linter)
![CI](https://github.com/actions/hello-world-docker-action/actions/workflows/ci.yml/badge.svg)


## UX todo
- [ ] self i18n works as living demo and test base with dryRun
- [ ] dryRun option
- [ ] report as how many docs, tokens been used

## Tech todo
- [ ] phase 1 into run model
- [ ] refactor LLM talk and client creation

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

### Manual
```bash
pip3 install...
export api_key={your_key}
## python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
## run repo itself
python3 main.py ./mkdocs.yml ./docs i18n-agent-action ./docs/index.md
```

### Container
```
docker run -it \
  -v /path_to_repo.../kepler-doc:/workspace \
  -e api_key="" \
  -e CONFIG_FILE="/workspace/mkdocs.yml" \
  -e DOCS_FOLDER="/workspace/docs" \
  -e RESERVED_WORD="kepler" \
  -e FILE_LIST="/workspace/docs/index.md" \
  ghcr.io/samyuan1990/i18n-agent-action:latest
```
### GHA


## Inputs
- Config file
- LLM service endpoint and API key
- Run model(to be specific)
- Specific file path(in case of LLM missing a path)
- Reserved word
- Optional Specific file if you have a file list

## Outputs
- Files.
- Trace Logs, in console

## Adption communtiy/project
- kepler

## Test Locally same as usage.manual
