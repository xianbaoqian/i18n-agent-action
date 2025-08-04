import os
import sys

import yaml
from clientInfo import clientInfo
from filesscopes import filesscopes
from translate import translate
from metric import print_metrics
from transcontrol import TranslationConfig
from utils import log, validate_inputs

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

Info = clientInfo(
    api_key=os.getenv("api_key"),
    base_url=os.getenv("base_url", "https://api.deepseek.com"),
    model=os.getenv("model", "deepseek-chat"),
    dryRun=os.getenv("dryRun", False),
)
Info.show_config()

TranslationConfig = TranslationConfig(
    target_language=os.getenv("target_language", "support"),
    max_files=os.getenv("max_files", 20),
)
TranslationConfig.show_config()

args = sys.argv
try:
    configfile_path, doc_folder, reserved_word = validate_inputs(args)
    log(
        f"Config: {configfile_path}, doc folder: {doc_folder}, reserved_word: {reserved_word}"
    )
except ValueError as e:
    log(f"错误: {e}", file=sys.stderr)
    log(
        "用法: python script.py <configfile_path> <doc_folder> <reserved_word>",
        file=sys.stderr,
    )
    sys.exit(1)

file_list = args[4] if len(args) > 4 else None
log(file_list)
## Workflow 1 missing files
### Phase 1
json_todo_list = filesscopes(
    configfile_path, doc_folder, file_list, 
    config, Info, TranslationConfig
)
### Phase 2
translate(
    json_todo_list, reserved_word, doc_folder, file_list,
    config, Info)

### show metrics
print_metrics()
