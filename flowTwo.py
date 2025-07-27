from utils import log,translate_element
### Phase 2
def flowtwo(json_todo_list, api_key,base_url,model, reserved_word,doc_folder,force_refresh: bool = True):
    total = len(json_todo_list["todo"])
    i = 0
    for item in json_todo_list['todo']:
        log("processing...one file")
        translate_element(api_key,base_url, model, reserved_word, doc_folder, item, force_refresh)
        i = i + 1
        log("todo")
        log(total - i)