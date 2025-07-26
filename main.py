from openai import OpenAI
import os
import json
import re
import subprocess
import sys

# 定义处理函数
def translate_element(api_key,base_url,model,reserved_word,doc_folder,element):
    print(f"processing: {element}")
    
    source_file = element['source_file']
    target_file = element['target_file']
    target_language = element['target_language']
    
    with open(doc_folder+"/"+source_file, 'r', encoding='utf-8') as file:
        file_content = file.read()  # 读取全部内容为字符串
    # in this turn, we just use one short to translate the files
    client = OpenAI(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a senior translators"},
            {"role": "user", "content": """
            please help translate content below into """ + target_language + """ for me, please keep """ + reserved_word + """ in english and keep the markdown style, here is the content: \n
            """ + file_content},
        ],
        stream=False
    )
    output_content = response.choices[0].message.content
    with open(doc_folder+"/"+target_file, 'w', encoding='utf-8') as file:
        file.write(output_content)

    

def get_tree_output(directory='.'):
    try:
        # 执行tree命令并捕获输出
        result = subprocess.run(['tree', directory], 
                              capture_output=True,
                              text=True,
                              check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return None
    except FileNotFoundError:
        print("未找到tree命令，请确保已安装tree工具")
        return None

def extract_json_from_text(text):
    """
    从文本中提取 JSON 对象
    
    参数:
        text (str): 包含 JSON 的文本内容
        
    返回:
        dict: 提取的 JSON 对象
        None: 如果未找到有效的 JSON
    """
    # 使用正则表达式匹配 JSON 部分（从第一个 { 到最后一个 }）
    json_pattern = r'\{[\s\S]*\}'
    match = re.search(json_pattern, text)
    
    if not match:
        return None
    
    json_str = match.group(0)
    
    try:
        # 尝试解析 JSON
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None

api_key = os.getenv('api_key')
base_url = os.getenv('base_url', "https://api.deepseek.com")
model = os.getenv('model', "deepseek-chat")

args = sys.argv  # 第一个元素是脚本名，之后是参数
#print("args:", args[1:])

configfile_path = args[1]
doc_folder = args[2]
reserved_word = args[3]

client = OpenAI(api_key=api_key, base_url=base_url)

## Phase 1
with open(configfile_path, 'r', encoding='utf-8') as file:
    config_file_content = file.read()  # 读取全部内容为字符串

print(doc_folder)
tree_list = get_tree_output(doc_folder)

messages = [
    {"role": "system", "content": "You are a senior software engineer"}
]

messages.append(
    {"role": "user", "content": 
            """
    according to config file below, 
    - which i18n does the project cover? 
    - what's the naming rule or file path rule for i18n mapping between different language edition? \n
    """ +
    config_file_content}
)

response1 = client.chat.completions.create(
    model=model,
    messages=messages
)
answer1 = response1.choices[0].message.content
print("问题1 回答:", answer1)
#print(response.choices[0].message.content)
messages.append({"role": "assistant", "content": answer1})
messages.append({"role": "user", "content": """
here is the tree command result for docs folder \n
"""
+tree_list+
"""\n
could you please list the missing file in support language? please result in mapping as source file, support file.
the empty json schema is
{
"todo":[],
}
if there one object in json
{
"todo":[
{
"source_file": "/path_to_file",
"target_file":"/path_to_file_i18n",
"target_language":"zh"
}
],
}
"""
})

response2 = client.chat.completions.create(
    model=model,
    messages=messages
)
print("问题2 回答:", response2.choices[0].message.content)

json_todo_list = extract_json_from_text(response2.choices[0].message.content)
# print(json_todo_list)

print(len(json_todo_list["todo"]))
print(json_todo_list["todo"][0])
print(reserved_word)
## Phase 2
total = len(json_todo_list["todo"])
i = 0
for item in json_todo_list['todo']:
    # def translate_element(api_key,base_url,language,reserved_word,model,element):
    # todo here identfy target language as Chinese
    print("processing...one file")
    translate_element(api_key,base_url, model, reserved_word, doc_folder, item)
    i = i + 1
    print("todo")
    print(total - i)
    
