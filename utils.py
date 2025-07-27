from openai import OpenAI
import subprocess
import re
import json
import os

def log(msg):
    print(msg)

#
#if should_refresh("data.txt", force_refresh=True):
#    print("需要刷新")  # 强制刷新时始终返回True
def should_refresh(target_file: str, force_refresh: bool = False) -> bool:
    """ 判断是否需要刷新文件 """
    return force_refresh or not os.path.isfile(target_file)
# 定义处理函数
#### todo if there is a existing file, then skip
def translate_element(api_key,base_url,model,reserved_word,doc_folder,element, force_refresh: bool = True):
    log(f"processing: {element}")

    source_file = element['source_file']
    if not doc_folder in source_file:
       source_file = doc_folder+"/"+source_file

    if not os.path.exists(source_file):
        log("skip as source file missing file " + source_file)
        return

    target_file = element['target_file']
    if not doc_folder in target_file:
       target_file = doc_folder+"/"+target_file

    if not should_refresh(target_file, force_refresh):
        log("skip file as target already there," + target_file)
        return
    target_language = element['target_language']
    
    with open(source_file, 'r', encoding='utf-8') as file:
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
    log('translated '+target_file)
    with open(target_file, 'w', encoding='utf-8') as file:
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
