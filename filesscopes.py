import json
import logging

from utils import get_all_files


### Phase 1 missingfiles
def filesscopes(TranslationContext, LLM_Client):
    with open(TranslationContext.configfile_path, "r", encoding="utf-8") as file:
        config_file_content = file.read()  # 读取全部内容为字符串

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
            "content": LLM_Client.get_config()["prompts"]["config_analysis"]
            + config_file_content,
        }
    )
    if LLM_Client.get_dryRun():
        logging.info("dry Run model using cache")
        return {
            "todo": [
                {
                    "source_file": "/workspace/docs/index.md",
                    "target_file": "/workspace/docs/index.zh.md",
                    "target_language": "zh",
                }
            ]
        }
    response1 = LLM_Client.talk_to_LLM(messages)
    answer1 = response1.choices[0].message.content
    logging.info("问题1 回答:" + answer1)
    messages.append({"role": "user", "content": answer1})

    filelist = [
        str(filepath) for filepath in get_all_files(TranslationContext.doc_folder)
    ]

    if TranslationContext.file_list:  # 检查是否非空
        given_files = TranslationContext.file_list.split(",")  # 拆分成列表
        filelist = given_files + filelist  # 合并到最前面
    # 将filelist分批次处理，每批30个文件
    batch_size = 30
    all_todos = []  # 用于累积所有批次的待办事项
    for i in range(0, len(filelist), batch_size):
        batch = filelist[i : i + batch_size]
        messages.append(
            {
                "role": "user",
                "content": (
                    f"here is part {i//batch_size + 1} of file lists for docs folder\n"
                    + "\n".join(batch)
                    + "\n\ncould you please list missing translated documents in "
                    + TranslationContext.target_language
                    + " language?\n\n"
                    + LLM_Client.get_config()["prompts"]["json_schema"]
                ),
            }
        )
        response2 = LLM_Client.talk_to_LLM_Json(messages)
        logging.info(
            f"问题2 回答(批次 {i//batch_size + 1}):"
            + response2.choices[0].message.content
        )

        current_batch = json.loads(response2.choices[0].message.content)
        logging.info(f"本批次待办数量: {len(current_batch['todo'])}")
        all_todos.extend(current_batch["todo"])
        if len(all_todos) > TranslationContext.max_files:
            break
    json_todo_list = {"todo": all_todos}
    logging.info(f"总待办数量: {len(all_todos)}")
    return json_todo_list
