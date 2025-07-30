import subprocess
import re
import json
import os
import sys

def validate_inputs(args):
    """
    验证并处理输入参数，提供灵活的参数检测
    
    参数:
        args (list): 命令行参数列表
        
    返回:
        tuple: (configfile_path, doc_folder, reserved_word)
        
    异常:
        ValueError: 当参数无效时抛出
    """
    # 参数数量检查
    if len(args) < 4:
        raise ValueError("需要3个参数: 配置文件路径、文档文件夹路径和保留字")
    
    # 获取参数
    configfile_path = args[1].strip() if len(args) > 1 else None
    doc_folder = args[2].strip() if len(args) > 2 else None
    reserved_word = args[3].strip() if len(args) > 3 else None
    
    # 配置文件路径验证
    if not configfile_path:
        raise ValueError("配置文件路径不能为空")
    
    # 检查配置文件是否存在（如果需要）
    if not os.path.isfile(configfile_path):
        raise ValueError(f"配置文件不存在: {configfile_path}")
    
    # 文档文件夹路径验证
    if not doc_folder:
        raise ValueError("文档文件夹路径不能为空")
    
    # 检查文档文件夹是否存在（如果需要）
    if not os.path.isdir(doc_folder):
        raise ValueError(f"文档文件夹不存在: {doc_folder}")
    
    # 保留字验证
    #if not reserved_word:
    #    raise ValueError("保留字不能为空")
    
    return configfile_path, doc_folder, reserved_word

def log(msg):
    print(msg)

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
    # re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, text, re.DOTALL)
    
    if not match:
        return None
    
    json_str = match.group(1)
    
    try:
        # 尝试解析 JSON
        log(json_str)
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        log(f"JSON 解析错误: {e}")
        return None
