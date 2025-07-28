from openai import OpenAI
import os
import sys
import yaml
from utils import log, validate_inputs
from flowTwo import flowtwo
from flowOne import missingfiles, givenfiles
from clientInfo import clientInfo

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

Info = clientInfo(
    api_key=os.getenv('api_key')
    base_url=os.getenv('base_url', "https://api.deepseek.com"),
    model=os.getenv('model', "deepseek-chat"),
    dryRun=os.getenv('dryRun',True)
)
Info.show_config()

log(f"base_url: {base_url}, model: {model}, dryRun: {dryRun}")
args = sys.argv
try:
    configfile_path, doc_folder, reserved_word = validate_inputs(args)
    log(f"Config: {configfile_path}, doc folder: {doc_folder}, reserved_word: {reserved_word}")
except ValueError as e:
    log(f"错误: {e}", file=sys.stderr)
    log("用法: python script.py <configfile_path> <doc_folder> <reserved_word>", file=sys.stderr)
    sys.exit(1)


## Workflow 1 missing files
### Phase 1
json_todo_list = missingfiles(configfile_path, doc_folder,config,api_key,base_url,model)
### Phase 2
flowtwo(json_todo_list, api_key,base_url, model, reserved_word, doc_folder, False)
## Workflow 2 
### Phase 1
if len(args) >4:
    file_list = args[4]
    log(file_list)
    json_todo_list = givenfiles(configfile_path,file_list,config,api_key,base_url,model)
### Phase 2
    flowtwo(json_todo_list, api_key,base_url, model, reserved_word, doc_folder)
