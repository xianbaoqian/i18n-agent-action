# なぜこれがあるのか
KCD 2025 北京、Community Over Code 2025 中国で議論され、最終的にコミュニティのためのi18n作業を処理するエージェントを作成することに決めました。
私としては、[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175) と Community Over Code 2025のセッションで並行して作業することができません。

## 私自身のエージェント開発の原則で試す

#### 推論1: タスクが比較的固定されており、信頼できる解決策がある場合、大きなモデルを呼び出してリスクを取る必要はありません。

#### 推論2: タスクは固定されておらず、一つ一つ適応させるのは複雑すぎます。大きなモデルには一定の普遍性があり、この普遍性をうまく利用して大きなモデルに委ねる必要があります。

#### 推論3: タスクは固定されておらず、一つ一つ適応させることができますが、実際の状況によります。大きなモデルを使用する場合、大きなモデルが間違って回答する状況を考慮し、エラーを適切に処理する必要があります。

#### 推論4: タスクは固定されていますが、信頼できる解決策がありません。大きなモデルを使用して創造的な解決策を試みる場合、手動介入が必要です。

# AIエージェントとして
## どのように機能するか
### 手動（開発者用、またはサンドボックスで実行されていないため自身のセキュリティを考慮する必要があります）
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
そして、自分でリンターを実行する必要があります。

### コンテナ（サンドボックスで実行）
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
自動PRを作成するために、プロジェクト設定でPR作成を有効にすることをお勧めします。

#### 1回目の初期化
```
name: Manual i8n and PR Creation

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # 手動トリガーを許可

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # 現在のブランチまたはmainブランチを使用
          fetch-depth: 0  # ブランチ作成のためにすべての履歴を取得

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
          title:
GHAによる自動i18n
          body: "このPRはあなたのためにi18nを行います"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # ターゲットブランチ
          draft: false
```
#### 各PRの後
```
name: 変更されたMarkdownファイルの処理

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

      - name: 変更されたMarkdownファイルの取得（すべてのi18nバリアントを除く）
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # すべての言語バリアントに一致

      - name: 変更されたファイルの表示と使用
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo "変更されたMarkdownファイル（すべてのi18nバリアントを除く）:"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: このアクションを使用
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action
          FILE_LIST: ${{ steps.changed-files.outputs.all_changed_files }}

      - name: プルリクエストの作成
        uses: peter-evans/create-pull-request@v7
        with:
          title: "GHAによる自動i18n"
          body: "このPRはあなたのためにi18nを行います"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # ターゲットブランチ
          draft: false
```

## 入力
| 入力パラメータ | 必須 | デフォルト値 | 説明 |
|-----------------|----------|---------------|-------------|
| `apikey`        | はい      | -             | LLMサービスのAPIキー |
| `base_url`      | いいえ       | DeepSeek             | LLMサービスのエンドポイントURL |
| `model`         | いいえ       | DeepSeek v3            | LLMサービスのモデル名/識別子 |
| `RESERVED_WORD` | はい      | -             | 翻訳から除外する予約語/フレーズ |
| `DOCS_FOLDER`   | はい      | -             | ドキュメントフォルダへのパス |
| `CONFIG_FILE`   | はい      | -             | プロジェクトi18n設定の設定ファイル |
| `FILE_LIST`     | いいえ       | -             | 処理する特定のファイルリスト（オプション） |
| `workspace`     | はい      | -             | コードリポジトリのワークスペースへのパス |
| `target_language` | いいえ     | `'zh'`        | 翻訳のターゲット言語コード（例：中国語の場合は`'zh'`） |
| `max_files`     | いいえ       | `'20'`        | 処理するファイルの最大数 |
| `dryRun`        | いいえ       | false             | ドライランモードを有効にする（変更を加えずに実行をシミュレート） |

## テスト済みcom
muntiy/project
- それ自体(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- HAMi

## 対象外
- lint
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.