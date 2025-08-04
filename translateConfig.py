from typing import List, Optional
import os

class TranslationContext:
    def __init__(
        self,
        target_language: str,
        file_list: Optional[str] = None,
        configfile_path: Optional[str] = None,
        doc_folder: Optional[str] = None,
        reserved_word: Optional[str] = None,
    ):
        """
        初始化翻译上下文对象
        
        参数:
            target_language (str): 目标语言代码 (如 'zh', 'fr')
            file_list (str, optional): 逗号分隔的文件列表字符串
            configfile_path (str, optional): 配置文件路径
            doc_folder (str, optional): 文档目录路径
            reserved_word (str, optional): 保留字/关键词
        """
        self._target_language = target_language
        self._file_list = file_list
        self._configfile_path = configfile_path
        self._doc_folder = doc_folder
        self._reserved_word = reserved_word

    # ----------------------
    # 属性访问器 (使用 @property)
    # ----------------------
    @property
    def target_language(self) -> str:
        """获取目标语言代码"""
        return self._target_language

    @property
    def file_list(self) -> str:
        """获取文件列表(已拆分的列表形式)"""
        if not self._file_list:
            return None
        return self._file_list

    @property
    def raw_file_list(self) -> Optional[str]:
        """获取原始未处理的文件列表字符串"""
        return self._file_list

    @property
    def configfile_path(self) -> Optional[str]:
        """获取配置文件路径(返回Path对象)"""
        return self._configfile_path if self._configfile_path else None

    @property
    def doc_folder(self) -> Optional[str]:
        """获取文档目录路径(返回Path对象)"""
        return self._doc_folder if self._doc_folder else None

    @property
    def reserved_word(self) -> Optional[str]:
        """获取保留字/关键词"""
        return self._reserved_word

    def show_config(self) -> None:
        """
        显示当前配置信息
        
        参数:
            verbose (bool): 是否显示详细路径信息，默认为False
        """
        print("\nTranslation Context Configuration:")
        print(f"  Target Language: {self._target_language}")
        print(f"  File list:' {self._file_list}")
        print(f"  configfile path: {self._configfile_path}")
        print(f"  doc folder: {self._doc_folder}")
        print(f"  reserved words: {self._reserved_word}")
    
