from AgentUtils.metric import LabeledCounter

# 定义指标
SOURCE_FILE_MISSING = LabeledCounter()
TARGET_FILE_EXISTS = LabeledCounter()
FILES_TRANSLATED = LabeledCounter()
TRANSLATION_REQUESTS = LabeledCounter()