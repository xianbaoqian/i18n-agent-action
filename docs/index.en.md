Here's the English translation while preserving the i18n-agent-action term and maintaining the markdown style:

```markdown
# Why we have this
This initiative was discussed at KCD 2025 Beijing and Community Over Code 2025 China, where we ultimately decided to create an agent to handle i18n tasks for the community.  
Personally, I couldn't simultaneously contribute to [https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175) and participate in Community Over Code 2025's sessions.

## Try with my own Principles of Agent Development

#### Inference 1: If the task is relatively fixed and has a reliable solution, there's no need to involve a large model and take unnecessary risks.

#### Inference 2: When tasks are not fixed and adapting them individually becomes too complex, leverage the generalizability of large models and delegate accordingly.

#### Inference 3: For non-fixed tasks that can be adapted case-by-case, assess the situation. If using a large model, account for potential errors and implement proper error handling.

#### Inference 4: For fixed tasks without reliable solutions, if attempting creative approaches with large models, ensure manual oversight is available.

# As it's an AI Agent
## How it works
### Manual (for devs, or proceed with caution as it doesn't run in a sandbox)
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
Remember to run linting separately.

### Container (sandboxed execution)
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
Enable PR automation in project settings for automatic PR generation.

#### 1st initialization
```
name: Manual i8n and PR Creation

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # Manual trigger enabled

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # Uses current branch or main
          fetch-depth: 0  # Full history for branch creation

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
          base: main  # Target branch
          draft: false
```
#### Post-PR automation
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

      - name: Get changed markdown files (excluding i18n variants)
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # Excludes all language variants

      - name: Print and use changed files
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo "Changed markdown files (excluding i18n variants):"
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
          base: main  # Target branch
          draft: false
```  

## Inputs
| Item | Description |
| --- | --- | 
| CONFIG_FILE | i18n configuration file |
| base_url | LLM service endpoint |
| apikey | LLM service API key |
| model | Specific LLM model |
| DOCS_FOLDER | Fallback path for LLM |
| RESERVED_WORD | Reserved identifier |
| FILE_LIST | Optional file list for i18n tasks |

## Adopted by communities/projects
- Self-reference (https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- Kepler

## Scope boundaries and workflow

> Avoiding wheel reinvention.
- Trigger mechanisms are out of scope
  - Left to manual full refreshes or diff actions
  - Model API and endpoint configuration
  > Users can choose any OpenAI-compatible LLM service?
  - Configuration entry points
  > Requires knowledge of default/target languages from config files.

--- In scope ---
- Phase one: Configuration parsing
> Sam @ July 2025: Avoid LLM project scanning due to token costs/errors. Document maintainers should provide i18n configs for 100% accuracy.

- Language scope determination:
  - Parse config files for language lists
  - Calculate: default language - existing languages (via file diff)

- Result storage conventions
> Sam @ July 2025: After translation scope is defined, we need naming rules from configs (or LLM-based pattern recognition).

-- Phase one outcome: Clear task scope with source files, translation targets, and languages.

-- Phase two: Translation loop
- LLM-assisted translation:
  - Glossary management for content mapping
  - Gap handling (or full refreshes)

> Sam @ July 2025: To be specified.

--- Out of scope ---
- PR creation delegated to existing PR Actions

> Leveraging existing solutions rather than rebuilding PR functionality.
```