from prometheus_client import Counter

# 定义指标
SOURCE_FILE_MISSING = Counter(
    "translation_source_file_missing_total",
    "Total number of missing source files",
    ["reserved_word", "target_language"],
)

TARGET_FILE_EXISTS = Counter(
    "translation_target_file_exists_total",
    "Total number of skipped translations due to existing target files",
    ["reserved_word", "target_language"],
)

FILES_TRANSLATED = Counter(
    "translation_files_translated_total",
    "Total number of files successfully translated",
    ["reserved_word", "target_language"],
)

TRANSLATION_REQUESTS = Counter(
    "translation_requests_total",
    "Total number of translation requests attempted",
    ["reserved_word", "target_language", "status"],
)
