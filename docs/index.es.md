# Por qué tenemos esto
Después de discutir en KCD 2025 Beijing y Community Over Code 2025 China, finalmente decidimos hacer un agente para manejar el trabajo de i18n de la comunidad.
Para mí, no puedo trabajar simultáneamente en [https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175) y en la reunión de Community Over Code 2025.

## Intentando mis propios principios de desarrollo de agentes

#### Corolario 1: Si la tarea es relativamente fija y tiene una solución confiable, no es necesario llamar a un modelo grande para arriesgarse.

#### Corolario 2: La tarea no es fija, adaptarse una por una es demasiado complejo. Los modelos grandes tienen cierta generalidad, necesitamos hacer buen uso de esta generalidad y delegarla al modelo grande.

#### Corolario 3: La tarea no es fija, puede adaptarse una por una según la situación real. Si se usa un modelo grande, hay que considerar la posibilidad de que el modelo grande responda incorrectamente y manejar el error en consecuencia.

#### Corolario 4: La tarea es fija pero no tiene una solución confiable. Si se usa un modelo grande para intentar soluciones creativas, se necesita intervención humana.

# Porque es un agente de IA
## Cómo funciona
### Manual (adecuado para desarrollo, o deberías asumir la responsabilidad de seguridad tú mismo, ya que no se ejecuta en un sandbox)
```
pip3 install -r ./requirements.txt
export api_key={your_key}
//python3 main.py {your config file} {your docs folder} {Reserved Word} {optional if you have a file list}
python3 main.py {full_path_to_your_repo}/mkdocs.yml {full_path_to_your_repo}/docs kepler {optional if you have a file list}
```
Y deberías ejecutar el linting tú mismo.

### Contenedor (se ejecuta en un sandbox)
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
Te sugiero que habilites la creación de PR en la configuración del proyecto para que PR se devuelva automáticamente.

#### Primera inicialización
```
name: i8n manual y creación de PR

permissions:
  contents: write
  pull-requests: write

on:
  workflow_dispatch:  # Permite la activación manual

jobs:
  i8n-and-create-pr:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout del código
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref || 'main' }}  # Usa la rama actual o la rama main
          fetch-depth: 0  # Obtiene todo el historial para crear una rama

      - name: Usar esta Action
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action

      - name: Crear Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title:
Usar GHA para i18n automático
          body: "Este PR completa la internacionalización por ti"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # Rama objetivo
          draft: false
```
#### Después de cada PR
```
name: Procesar archivos Markdown cambiados

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

      - name: Obtener archivos markdown cambiados (excluyendo todas las variantes i18n)
        id: changed-files
        uses: tj-actions/changed-files@v40
        with:
          since_last_remote_commit: true
          separator: ","
          files: |
            docs/**/*.md
          files_ignore: |
            docs/**/*.*.md  # Coincide con todas las variantes de idioma

      - name: Imprimir y usar archivos cambiados
        if: steps.changed-files.outputs.all_changed_files != ''
        run: |
          echo
Archivos markdown modificados (excluyendo todas las variantes i18n):
          echo "${{ steps.changed-files.outputs.all_changed_files }}"

      - name: Usar esta Acción
        id: use-action
        uses: SamYuan1990/i18n-agent-action@main
        with:
          apikey: ${{ secrets.API_KEY }}
          RESERVED_WORD: i18n-agent-action
          DOCS_FOLDER: /workspace/docs
          CONFIG_FILE: /workspace/mkdocs.yml
          workspace: /home/runner/work/i18n-agent-action/i18n-agent-action
          FILE_LIST: ${{ steps.changed-files.outputs.all_changed_files }}

      - name: Crear Pull Request
        uses: peter-evans/create-pull-request@v7
        with:
          title: "Usar GHA para internacionalización automática"
          body: "Este PR completa la internacionalización por usted"
          branch: feature/i18n-${{ github.run_id }}
          base: main  # Rama objetivo
          draft: false

## Entrada
| Parámetro de entrada | Requerido | Valor por defecto | Descripción |
|-----------------|----------|---------------|-------------|
| `apikey`        | Sí      | -             | Clave API del servicio LLM |
| `base_url`      | No       | DeepSeek             | URL del endpoint del servicio LLM |
| `model`         | No       | DeepSeek v3            | Nombre/identificador del modelo del servicio LLM |
| `RESERVED_WORD` | Sí      | -             | Término/frase reservado para excluir de la traducción |
| `DOCS_FOLDER`   | Sí      | -             | Ruta de su carpeta de documentos |
| `CONFIG_FILE`   | Sí      | -             | Archivo de configuración para la internacionalización del proyecto |
| `FILE_LIST`     | No       | -             | Lista específica de archivos a procesar (opcional) |
| `workspace`     | Sí      | -             | Ruta del espacio de trabajo de su repositorio de código |
| `target_language` | No     | `'zh'`        | Código del idioma objetivo para la traducción (por ejemplo, `'zh'` para chino) |
| `max_files`     | No       | `'20'`        | Número máximo de archivos a procesar |
| `dryRun`        | No       | false             | Habilitar modo dry-run (simular ejecución sin hacer cambios) |

## Prueba completada
muntiy/proyecto
- Propio(https://github.com/SamYuan1990/i18n-agent-action/pull/15)
- HAMi

## Fuera de alcance
- lint
 Descargo de responsabilidad: Este contenido está potenciado por i18n-agent-action con el servicio LLM https://api.deepseek.com con el modelo deepseek-chat, por alguna razón, (por ejemplo, no somos hablantes nativos) usamos LLM para proporcionar esta traducción para usted. Si encuentra alguna corrección, por favor abra un issue o envíe un PR de vuelta a github, y cambie de vuelta al idioma por defecto.
 Disclaimers: This content is powered by i18n-agent-action with LLM service https://api.deepseek.com with model deepseek-chat, for some reason, (for example, we are not native speaker) we use LLM to provide this translate for you. If you find any corrections, please file an issue or raise a PR back to github, and switch back to default language.