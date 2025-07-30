from utils import log, get_tree_output,extract_json_from_text
from openai import OpenAI
from clientInfo import clientInfo

### Phase 1 missingfiles
def missingfiles(configfile_path,doc_folder,config, clientInfo):
    with open(configfile_path, 'r', encoding='utf-8') as file:
        config_file_content = file.read()  # 读取全部内容为字符串

    log(doc_folder)
    tree_list = get_tree_output(doc_folder)

    messages = [
        {"role": "system", "content": "You are a senior software engineer"}
    ]

    messages.append(
        {"role": "user", "content": 
        config['prompts']['config_analysis'] +
        config_file_content}
    )
    if clientInfo.get_dryRun():
        log("dry Run model using cache")
        return {"todo":[{
            "source_file": "/workspace/docs/index.md",
            "target_file": "/workspace/docs/index.zh.md",
            "target_language": "zh"
        }]}
    response1 = clientInfo.talk_to_LLM(messages)
    answer1 = response1.choices[0].message.content
    log("问题1 回答:" + answer1)
    messages.append({"role": "assistant", "content": answer1})
    messages.append({"role": "user", "content": """
    here is the tree command result for docs folder \n
    """
    +tree_list+
    """\n
    could you please list the missing file in support language?  \n
    """ + config['prompts']['json_schema']
    })
    response2 = clientInfo.talk_to_LLM(messages)
    log("问题2 回答:" + response2.choices[0].message.content)
    json_todo_list=extract_json_from_text(response2.choices[0].message.content)
    log(len(json_todo_list["todo"]))
    # log(json_todo_list["todo"][0])
    return json_todo_list

### Phase 1 givenfiles
def givenfiles(configfile_path,file_list,config,clientInfo):
    with open(configfile_path, 'r', encoding='utf-8') as file:
        config_file_content = file.read()  # 读取全部内容为字符串
    messages = [
        {"role": "system", "content": "You are a senior software engineer"}
    ]

    messages.append(
        {"role": "user", "content": 
        config['prompts']['config_analysis'] +
        config_file_content}
    )
    if clientInfo.get_dryRun():
        log("dry Run model using cache")
        return {"todo":[{
            "source_file": "/workspace/docs/index.md",
            "target_file": "/workspace/docs/index.zh.md",
            "target_language": "zh"
        }]}
    response1 = clientInfo.talk_to_LLM(messages)
    answer1 = response1.choices[0].message.content
    log("问题1 回答:" + answer1)
    messages.append({"role": "assistant", "content": answer1})
    messages.append({"role": "user", "content": """
    file list below been changed, could you please list the need translation files in support language?  \n
    """ + config['prompts']['json_schema'] + 
    """\n
    here are the file list. \n
    """ + file_list
    })
    response2 = clientInfo.talk_to_LLM(messages)
    log("问题2 回答:" + response2.choices[0].message.content)
    json_todo_list=extract_json_from_text(response2.choices[0].message.content)
    log(len(json_todo_list["todo"]))
    log(json_todo_list["todo"][0])
    return json_todo_list