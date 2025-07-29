from openai import OpenAI

class clientInfo:
    def __init__(self, api_key=None, base_url="https://api.example.com", model="gpt-4", dryRun=False):
        """
        初始化ApiClient
        
        参数:
            api_key (str): API密钥，默认为None
            base_url (str): 基础URL，默认为"https://api.example.com"
            model (str): 模型名称，默认为"gpt-4"
            dryRun (bool): 是否干跑模式，默认为False
        """
        self._api_key = api_key
        self._base_url = base_url
        self._model = model
        # 鲁棒性处理dryRun参数
        if isinstance(dryRun, str):
            self._dryRun = dryRun.lower() == "true"
        elif isinstance(dryRun, int):
            self._dryRun = bool(dryRun)
        else:
            self._dryRun = bool(dryRun)
        if not self._dryRun:
           self._client = OpenAI(api_key=self._api_key, 
                                base_url=self._base_url)
        else:
           self._client = None

    
    # Getter方法
    def get_api_key(self):
        """获取API密钥"""
        return self._api_key
    
    def get_base_url(self):
        """获取基础URL"""
        return self._base_url
    
    def get_model(self):
        """获取模型名称"""
        return self._model
    
    def get_dryRun(self):
        """获取干跑模式状态"""
        return self._dryRun
    
    # 可选：添加一个显示所有配置的方法
    def show_config(self):
        """显示当前配置"""
        print(f"API Client Configuration:")
        print(f"  Base URL: {self._base_url}")
        print(f"  Model: {self._model}")
        print(f"  Dry Run: {self._dryRun}")

    def talk_to_LLM(self, messages):
        if not self._dryRun:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=False
            )
            return response
        else: 
            return None