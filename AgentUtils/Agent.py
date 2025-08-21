class Agent:
    def __init__(self, LLM_Client):
        self.LLM_Client = LLM_Client

    def talk_to_LLM(self, messages):
        return self.LLM_Client.talk(messages, False)

    def talk_to_LLM_Json(self, messages):
        return self.LLM_Client.talk(messages, True)

    def dryRun(self):
        """获取干跑模式状态"""
        return self.LLM_Client.get_dryRun()

    def get_legal_info(self):
        return self.LLM_Client.get_legal_info()

    