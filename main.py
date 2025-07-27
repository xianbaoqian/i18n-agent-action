from openai import OpenAI
import os
import sys
import yaml
from utils import log
from flowTwo import flowtwo
from flowOne import missingfiles, givenfiles

with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

api_key = os.getenv('api_key')
base_url = os.getenv('base_url', "https://api.deepseek.com")
model = os.getenv('model', "deepseek-chat")

args = sys.argv  # 第一个元素是脚本名，之后是参数
#print("args:", args[1:])

configfile_path = args[1]
doc_folder = args[2]
reserved_word = args[3]

log(configfile_path)
log(doc_folder)
log(reserved_word)
log(model)
log(base_url)
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
