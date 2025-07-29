from utils import log,translate_element
from clientInfo import clientInfo
### Phase 2
def flowtwo(json_todo_list, reserved_word,doc_folder, clientInfo, force_refresh: bool = True):
    total = len(json_todo_list["todo"])
    i = 0
    if clientInfo.get_dryRun:
        log("dry Run model skip")
        return 
    for item in json_todo_list['todo']:
        log("processing...one file")
        translate_element(reserved_word, doc_folder, item, clientInfo, force_refresh)
        i = i + 1
        log("todo")
        log(total - i)