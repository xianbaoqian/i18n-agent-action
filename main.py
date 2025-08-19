import logging
import os
import sys

from clientInfo import clientInfo
from ExpiringDictStorage import ExpiringDictStorage
from filesscopes import filesscopes
from metric import print_metrics
from translate import translate
from translateConfig import TranslationContext
from utils import validate_inputs

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
storage = ExpiringDictStorage(expiry_days=7)

## system
LLM_Client = clientInfo(
    api_key=os.getenv("api_key"),
    base_url=os.getenv("base_url", "https://api.deepseek.com"),
    model=os.getenv("model", "deepseek-chat"),
    dryRun=os.getenv("dryRun", False),
    local_cache=storage,
    usecache=os.getenv("usecache", True),
)
LLM_Client.show_config()

args = sys.argv
try:
    configfile_path, doc_folder, reserved_word = validate_inputs(args)
    logging.info(
        f"Config: {configfile_path}, doc folder: {doc_folder}, reserved_word: {reserved_word}"
    )
except ValueError as e:
    logging.info(f"错误: {e}", file=sys.stderr)
    logging.info(
        "用法: python script.py <configfile_path> <doc_folder> <reserved_word>",
        file=sys.stderr,
    )
    sys.exit(1)

file_list = args[4] if len(args) > 4 else None

context = TranslationContext(
    target_language=os.getenv("target_language", "support"),
    file_list=file_list,
    configfile_path=configfile_path,
    doc_folder=doc_folder,
    reserved_word=reserved_word,
    max_files=os.getenv("max_files", 20),
    disclaimers=os.gentenv("disclaimers", True),
)
context.show_config()
## Workflow 1 missing files
### Phase 1
json_todo_list = filesscopes(context, LLM_Client)
### Phase 2
translate(json_todo_list, context, LLM_Client)

### show metrics
print_metrics()
