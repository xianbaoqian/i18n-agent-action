import os
import threading

from metric import (
    FILES_TRANSLATED,
    SOURCE_FILE_MISSING,
    TARGET_FILE_EXISTS,
    TRANSLATION_REQUESTS,
)
from utils import log


#
# if should_refresh("data.txt", force_refresh=True):
#    print("需要刷新")  # 强制刷新时始终返回True
def should_refresh(target_file: str, force_refresh: bool = False) -> bool:
    """判断是否需要刷新文件"""
    return force_refresh or not os.path.isfile(target_file)


# 定义处理函数
#### todo if there is a existing file, then skip
def translate_element(
    reserved_word, doc_folder, element, config, clientInfo, force_refresh: bool = True
):
    TRANSLATION_REQUESTS.labels(
        reserved_word=reserved_word,
        target_language=element["target_language"],
        status="started",
    ).inc()

    log(f"processing: {element}")

    source_file = element["source_file"]
    if doc_folder not in source_file:
        source_file = doc_folder + "/" + source_file

    if not os.path.exists(source_file):
        log("skip as source file missing file " + source_file)
        SOURCE_FILE_MISSING.labels(
            reserved_word=reserved_word, target_language=element["target_language"]
        ).inc()
        TRANSLATION_REQUESTS.labels(
            reserved_word=reserved_word,
            target_language=element["target_language"],
            status="source_missing",
        ).inc()
        return

    target_file = element["target_file"]
    if doc_folder not in target_file:
        target_file = doc_folder + "/" + target_file

    if not should_refresh(target_file, force_refresh):
        log("skip file as target already there," + target_file)
        TARGET_FILE_EXISTS.labels(
            reserved_word=reserved_word, target_language=element["target_language"]
        ).inc()
        TRANSLATION_REQUESTS.labels(
            reserved_word=reserved_word,
            target_language=element["target_language"],
            status="target_exists",
        ).inc()
        return

    target_language = element["target_language"]

    # Read the entire source file
    with open(source_file, "r", encoding="utf-8") as file:
        file_content = file.read()

    # Split content into chunks of 3000 characters
    chunk_size = 3000
    chunks = [
        file_content[i : i + chunk_size]
        for i in range(0, len(file_content), chunk_size)
    ]

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        log(f"Processing chunk {i+1}/{len(chunks)} of {source_file}")

        messages = [
            {"role": "system", "content": config["prompts"]["translator"]},
            {
                "role": "user",
                "content": """
                Please help translate the following content into """
                + target_language
                + """, reserved word: """
                + reserved_word
                + """ in English  
                This is part """
                + f"{i+1} of {len(chunks)} of the document.\n\n"
                + chunk,
            },
        ]

        try:
            response = clientInfo.talk_to_LLM(messages)
            translated_chunks.append(response.choices[0].message.content)
        except Exception as e:
            log(f"Error translating chunk {i+1}: {str(e)}")
            TRANSLATION_REQUESTS.labels(
                reserved_word=reserved_word,
                target_language=target_language,
                status="error",
            ).inc()
            raise

    # Combine all translated chunks
    output_content = "\n".join(translated_chunks) + "\n " + clientInfo.get_legal_info()

    log("translated " + target_file)
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as file:
        file.write(output_content)

    # Record successful translation metrics
    FILES_TRANSLATED.labels(
        reserved_word=reserved_word, target_language=target_language
    ).inc()
    TRANSLATION_REQUESTS.labels(
        reserved_word=reserved_word, target_language=target_language, status="success"
    ).inc()


### Phase 2
def flowtwo(
    json_todo_list,
    reserved_word,
    doc_folder,
    config,
    clientInfo,
    force_refresh: bool = True,
):
    total = len(json_todo_list["todo"])
    if clientInfo.get_dryRun():
        log("dry Run model skip")
        return

    # Create a list to hold our threads
    threads = []
    # Create a counter for completed tasks (similar to WaitGroup)
    completed = 0
    # Lock for thread-safe counter updates
    counter_lock = threading.Lock()

    def worker(item):
        nonlocal completed
        try:
            log("processing...one file")
            translate_element(
                reserved_word, doc_folder, item, config, clientInfo, force_refresh
            )
        finally:
            with counter_lock:
                completed += 1
                remaining = total - completed
                log(f"todo: {remaining}")

    # Create and start threads
    for item in json_todo_list["todo"]:
        thread = threading.Thread(target=worker, args=(item,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    log("All tasks completed")
