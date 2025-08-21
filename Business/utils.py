from collections import OrderedDict
from pathlib import Path


def get_all_files(directory):
    path = Path(directory)
    return [file.resolve() for file in path.rglob("**/*.md") if file.is_file()]


def MergePN(str1, str2):
    # 分割并保持顺序去重
    merged = list(
        OrderedDict.fromkeys(
            [item.strip() for item in str1.split(",")]
            + [item.strip() for item in str2.split(",")]
        )
    )

    result = ", ".join(merged)
    return result
