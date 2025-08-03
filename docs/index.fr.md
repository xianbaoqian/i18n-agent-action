# Pourquoi nous avons cela
Cela a été discuté lors du KCD 2025 Pékin, Community Over Code 2025 Chine et nous avons finalement décidé de créer un agent pour gérer les travaux i18n pour la communauté.
Pour moi, je ne peux pas paralléliser dans [https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175) et la session de Community Over Code 2025.

## Essayer avec mes propres Principes de Développement d'Agent

#### Inférence 1 : Si la tâche est relativement fixe et qu'il existe une solution fiable, il n'est pas nécessaire de faire appel à un grand modèle pour prendre des risques.

#### Inférence 2 : Les tâches ne sont pas fixes, et les adapter une par une est trop complexe. Le grand modèle a une certaine universalité, et nous devons bien utiliser cette universalité et la confier au grand modèle.

#### Inférence 3 : La tâche n'est pas fixe et peut être adaptée une par une, selon la situation réelle. Si l'on utilise un grand modèle, il est nécessaire de considérer la situation où le grand modèle répond incorrectement et de gérer les erreurs en conséquence.

#### Inférence 4 : La tâche est fixe et il n'y a pas de solution fiable. Si l'on utilise un grand modèle pour tenter des solutions créatives, une intervention manuelle est nécessaire.

# Comme c'est un Agent IA
## Comment ça marche
### Manuel(pour dev, ou vous devriez prendre votre propre sécurité car il ne s'exécute pas dans un bac à sable)
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
et vous devriez exécuter le linting par vous-même.

### Conteneur(exécution dans un bac à sable)
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
Je vous suggère d'activer la création de PR dans les paramètres du projet pour faire un PR auto en retour.

#### 1ère initialisation
```
name: Manuel i8n et Création de PR

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # Permet un déclenchement manuel

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # Utilise la branche actuelle ou la branche main
          fetch-depth: 0  # Récupère tout l'historique pour permettre la création de branche

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
"auto i18n avec GHA"
          body: "Cette PR fait l'i18n pour vous"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # branche cible
          draft: false
```
#### après chaque PR
```
name: Traiter les fichiers Markdown modifiés

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

      - name: Obtenir les fichiers markdown modifiés (excluant toutes les variantes i18n)
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # correspond à toutes les variantes linguistiques

      - name: Afficher et utiliser les fichiers modifiés
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo "Fichiers markdown modifiés (excluant toutes les variantes i18n):"
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: Utiliser cette action
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action
          FILE_LIST: ${{ steps.changed-files.outputs.all_changed_files }}

      - name: Créer une Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: "auto i18n avec GHA"
          body: "Cette PR fait l'i18n pour vous"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # branche cible
          draft: false
```

## Entrées
| Paramètre d'entrée | Requis | Valeur par défaut | Description |
|-----------------|----------|---------------|-------------|
| `apikey`        | Oui      | -             | Clé API pour le service LLM |
| `base_url`      | Non       | DeepSeek             | URL du point de terminaison du service LLM |
| `model`         | Non       | DeepSeek v3            | Nom/identifiant du modèle pour le service LLM |
| `RESERVED_WORD` | Oui      | -             | Termes/phrases réservés à exclure de la traduction |
| `DOCS_FOLDER`   | Oui      | -             | Chemin vers votre dossier de documentation |
| `CONFIG_FILE`   | Oui      | -             | Fichier de configuration pour les paramètres i18n du projet |
| `FILE_LIST`     | Non       | -             | Liste spécifique de fichiers à traiter (optionnel) |
| `workspace`     | Oui      | -             | Chemin vers votre espace de travail de dépôt de code |
| `target_language` | Non     | `'zh'`        | Code de langue cible pour la traduction (par exemple, `'zh'` pour le chinois) |
| `max_files`     | Non       | `'20'`        | Nombre maximum de fichiers à traiter |
| `dryRun`        | Non       | false             | Activer le mode dry-run (simule l'exécution sans apporter de modifications) |

## Testé com
muntiy/projet
- lui-même(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- HAMi

## Non inclus
- lint
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.