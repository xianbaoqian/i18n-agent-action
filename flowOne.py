import json

from utils import get_all_files, log

### Phase 1 missingfiles
def missingfiles(configfile_path, doc_folder, config, clientInfo, TranslationConfig):
    with open(configfile_path, "r", encoding="utf-8") as file:
        config_file_content = file.read()  # 读取全部内容为字符串

    log(doc_folder)
    #tree_list = get_tree_output(doc_folder)

    messages = [
        {
            "role": "user",
            "content": """You are a senior software engineer

    Your core responsibilities:
    - Analysis user's provided i18n config file.
    - Analysis the naming rule or file path rule for i18n mapping between different language editions?
    - Base on file lists from user, help analysis the file paths.
    
    File lists analysis steps:
    - According to naming rule or file path rule for i18n mapping between different language editions.
    - user will provide a list with absolute path, identify if the file is default language file or not.
    - if yes, please answer with translated language file name with absolute path.

    Quality assurance steps:
    - Verify you understand i18n config file.
    - Verify you understand the naming rule or file path rule for i18n mapping between different language editions.
    """,
        }
    ]

    messages.append(
        {
            "role": "user",
            "content": config["prompts"]["config_analysis"] + config_file_content,
        }
    )
    if clientInfo.get_dryRun():
        log("dry Run model using cache")
        return {
            "todo": [
                {
                    "source_file": "/workspace/docs/index.md",
                    "target_file": "/workspace/docs/index.zh.md",
                    "target_language": "zh",
                }
            ]
        }
    response1 = clientInfo.talk_to_LLM(messages)
    answer1 = response1.choices[0].message.content
    log("问题1 回答:" + answer1)
    messages.append({"role": "user", "content": answer1})

    filelist = get_all_files(doc_folder)
    # 将filelist分批次处理，每批30个文件
    batch_size = 30
    all_todos = []  # 用于累积所有批次的待办事项
    for i in range(0, len(filelist), batch_size):
        batch = filelist[i:i + batch_size]
        messages.append(
                {
                    "role": "user",
                    "content": (
                        f"here is part {i//batch_size + 1} of file lists for docs folder\n"
                        + "\n".join(str(filepath) for filepath in batch)
                        + "\n\ncould you please list missing translated documents in "
                        + TranslationConfig.get_target_language()
                        + " language?\n\n"
                        + config["prompts"]["json_schema"]
                    )
                }
            )
        response2 = clientInfo.talk_to_LLM_Json(messages)
        log(f"问题2 回答(批次 {i//batch_size + 1}):" + response2.choices[0].message.content)

        current_batch = json.loads(response2.choices[0].message.content)
        log(f"本批次待办数量: {len(current_batch['todo'])}")
        all_todos.extend(current_batch["todo"])
        if len(all_todos) > TranslationConfig.get_max_files():
            break
    # log(json_todo_list["todo"][0])
    json_todo_list = {"todo": all_todos}
    log(f"总待办数量: {len(all_todos)}")
    return json_todo_list


### Phase 1 givenfiles
def givenfiles(configfile_path, file_list, config, clientInfo, TranslationConfig):
    with open(configfile_path, "r", encoding="utf-8") as file:
        config_file_content = file.read()  # 读取全部内容为字符串
    messages = [{"role": "system", "content": "You are a senior software engineer"}]

    messages.append(
        {
            "role": "user",
            "content": config["prompts"]["config_analysis"] + config_file_content,
        }
    )
    if clientInfo.get_dryRun():
        log("dry Run model using cache")
        return {
            "todo": [
                {
                    "source_file": "/workspace/docs/index.md",
                    "target_file": "/workspace/docs/index.zh.md",
                    "target_language": "zh",
                }
            ]
        }
    response1 = clientInfo.talk_to_LLM(messages)
    answer1 = response1.choices[0].message.content
    log("问题1 回答:" + answer1)
    messages.append({"role": "assistant", "content": answer1})
    messages.append(
        {
            "role": "user",
            "content": """
    file list below been changed, could you please list the need translation files in """
            + TranslationConfig.get_target_language()
            + """ language?  \n
    """
            + config["prompts"]["json_schema"]
            + """\n
    here are the file list. \n
    """
            + file_list,
        }
    )
    response2 = clientInfo.talk_to_LLM_Json(messages)
    log("问题2 回答:" + response2.choices[0].message.content)
    json_todo_list = json.loads(response2.choices[0].message.content)
    log(len(json_todo_list["todo"]))
    return json_todo_list
