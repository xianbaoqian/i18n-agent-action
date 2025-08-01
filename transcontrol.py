class TranslationConfig:
    """
    翻译配置类，从环境变量中读取配置

    属性:
        target_language (str): 目标翻译语言代码，如'zh'
        max_files (int): 最大处理文件数量
    """

    def __init__(self, target_language, max_files):
        """
        初始化翻译配置

        参数:
            target_language: 可手动指定目标语言，否则从环境变量读取
            max_files: 可手动指定最大文件数，否则从环境变量读取
        """
        # 设置目标语言
        self._target_language = target_language

        # 设置最大文件数量，默认为20
        try:
            self._max_files = int(max_files)
        except ValueError:
            self._max_files = 20
            print(f"警告: MAX_FILES 环境变量值无效，使用默认值 {self._max_files}")

    def show_config(self) -> str:
        print(
            f"TranslationConfig(target_language='{self._target_language}', "
            f"max_files={self._max_files})"
        )

    # Getter方法
    def get_max_files(self):
        """获取API密钥"""
        return self._max_files

    def get_target_language(self):
        """获取API密钥"""
        return self._target_language
