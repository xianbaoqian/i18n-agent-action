import json
import os
import re
import subprocess


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
    # if not reserved_word:
    #    raise ValueError("保留字不能为空")

    return configfile_path, doc_folder, reserved_word


def log(msg):
    print(msg)


def get_tree_output(directory="."):
    try:
        # 执行tree命令并捕获输出
        result = subprocess.run(
            ["tree", directory], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return None
    except FileNotFoundError:
        print("未找到tree命令，请确保已安装tree工具")
        return None
