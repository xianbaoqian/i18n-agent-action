import os

from utils import log


#
# if should_refresh("data.txt", force_refresh=True):
#    print("需要刷新")  # 强制刷新时始终返回True
def should_refresh(target_file: str, force_refresh: bool = False) -> bool:
    """判断是否需要刷新文件"""
    return force_refresh or not os.path.isfile(target_file)


# 定义处理函数
#### todo if there is a existing file, then skip
def translate_element(
    reserved_word, doc_folder, element, clientInfo, force_refresh: bool = True
):
    log(f"processing: {element}")

    source_file = element["source_file"]
    if doc_folder not in source_file:
        source_file = doc_folder + "/" + source_file

    if not os.path.exists(source_file):
        log("skip as source file missing file " + source_file)
        return

    target_file = element["target_file"]
    if doc_folder not in target_file:
        target_file = doc_folder + "/" + target_file

    if not should_refresh(target_file, force_refresh):
        log("skip file as target already there," + target_file)
        return
    target_language = element["target_language"]

    with open(source_file, "r", encoding="utf-8") as file:
        file_content = file.read()  # 读取全部内容为字符串
    # in this turn, we just use one short to translate the files
    messages = [
        {"role": "system", "content": "You are a senior translators"},
        {
            "role": "user",
            "content": """
            please help translate content below into """
            + target_language
            + """ for me, please keep """
            + reserved_word
            + """ in english and keep the markdown style, here is the content: \n
            """
            + file_content,
        },
    ]
    response = clientInfo.talk_to_LLM(messages)
    output_content = (
        response.choices[0].message.content + "\n " + clientInfo.get_legal_info()
    )

    log("translated " + target_file)
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as file:
        file.write(output_content)


### Phase 2
def flowtwo(
    json_todo_list, reserved_word, doc_folder, clientInfo, force_refresh: bool = True
):
    total = len(json_todo_list["todo"])
    i = 0
    if clientInfo.get_dryRun():
        log("dry Run model skip")
        return
    for item in json_todo_list["todo"]:
        log("processing...one file")
        translate_element(reserved_word, doc_folder, item, clientInfo, force_refresh)
        i = i + 1
        log("todo")
        log(total - i)
