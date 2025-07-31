from prometheus_client import REGISTRY, Counter
from prometheus_client.exposition import generate_latest

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


def print_metrics():
    try:
        # 获取所有指标数据并解码为UTF-8字符串
        metrics_data = generate_latest(REGISTRY).decode("utf-8")
        print("\n=== Current Prometheus Metrics ===")
        print(metrics_data)
        print("=================================\n")
    except Exception as e:
        print(f"Error printing metrics: {str(e)}")
