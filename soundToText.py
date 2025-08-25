#!/usr/bin/env python3
import os
import queue
import sys
import threading
import time

import numpy as np
import pyttsx3
import sherpa_onnx
import sounddevice as sd
from AgentUtils.clientInfo import clientInfo
from AgentUtils.ExpiringDictStorage import ExpiringDictStorage
from AgentUtils.span import Span_Mgr
from Business.translate import translateAgent
from Business.translateConfig import TranslationContext

storage = ExpiringDictStorage(expiry_days=7)
LLM_client = clientInfo(
    api_key=os.getenv("api_key"),
    base_url=os.getenv("base_url", "https://api.deepseek.com"),
    model=os.getenv("model", "deepseek-chat"),
    dryRun=os.getenv("dryRun", False),
    local_cache=storage,
    usecache=os.getenv("usecache", True),
)
context = TranslationContext(
    target_language="zh",
    file_list="",
    configfile_path="",
    doc_folder="",
    reserved_word="",
    max_files=20,
    disclaimers=False,
)
span_mgr = Span_Mgr(storage)
root_span = span_mgr.create_span("Root operation")
TsAgent = translateAgent(LLM_client, span_mgr)


class SpeechRecognizer:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.killed = False
        self.samples_queue = queue.Queue()
        self.recognizer = self._create_recognizer()
        self.vad = self._create_vad()
        self.display = Display()
        self.recording_thread = None
        self.pause_recording = threading.Event()  # 用于控制录音线程的暂停和恢复
        self.engine = pyttsx3.init()

    def _create_recognizer(self):
        """创建并返回语音识别器"""
        return sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder="./base-encoder.onnx",
            decoder="./base-decoder.onnx",
            tokens="./base-tokens.txt",
            language="",
        )

    def _create_vad(self):
        """创建并返回语音活动检测器"""
        config = sherpa_onnx.VadModelConfig()
        config.silero_vad.model = "./silero_vad.onnx"
        config.silero_vad.threshold = 0.5
        config.silero_vad.min_silence_duration = 0.1
        config.silero_vad.min_speech_duration = 0.25
        config.silero_vad.max_speech_duration = 8
        config.sample_rate = self.sample_rate

        return sherpa_onnx.VoiceActivityDetector(config, buffer_size_in_seconds=100)

    def start_recording(self):
        """录音线程函数"""
        samples_per_read = int(0.1 * self.sample_rate)  # 100 ms

        with sd.InputStream(
            channels=1, dtype="float32", samplerate=self.sample_rate
        ) as stream:
            while not self.killed:
                # 检查是否需要暂停
                if self.pause_recording.is_set():
                    time.sleep(0.01)  # 短暂休眠以减少CPU使用
                    continue
                samples, _ = stream.read(samples_per_read)
                self.samples_queue.put(samples.reshape(-1).copy())

    def process_audio(self, buffer, offset, started, started_time):
        """处理音频数据并返回更新后的状态"""
        window_size = self.vad.config.silero_vad.window_size

        # 更新VAD状态
        while offset + window_size < len(buffer):
            self.vad.accept_waveform(buffer[offset : offset + window_size])
            if not started and self.vad.is_speech_detected():
                started = True
                started_time = time.time()
            offset += window_size

        # 处理缓冲区溢出
        if not started and len(buffer) > 10 * window_size:
            offset -= len(buffer) - 10 * window_size
            buffer = buffer[-10 * window_size :]

        # 处理检测到的语音
        if started and time.time() - started_time > 0.2:
            stream = self.recognizer.create_stream()
            stream.accept_waveform(self.sample_rate, buffer)
            self.recognizer.decode_stream(stream)

            text = stream.result.text.strip()
            if text:
                self.display.update_text(text)
                started_time = time.time()

        # 处理VAD结果
        while not self.vad.empty():
            # 暂停录音线程
            self.pause_recording.set()

            try:
                stream = self.recognizer.create_stream()
                stream.accept_waveform(self.sample_rate, self.vad.front.samples)
                self.vad.pop()
                self.recognizer.decode_stream(stream)

                text = stream.result.text.strip()
                self.display.update_text(text)
                result = self.display.finalize_current_sentence()
                if result is not None:
                    print("Result:", result)
                    afterTs = TsAgent.translate(
                        context, context.target_language, result, root_span
                    )
                    self.engine.say(afterTs)
                    self.engine.runAndWait()
                    time.sleep(10)
            finally:
                # 确保无论发生什么都会恢复录音线程
                self.pause_recording.clear()

            # 重置状态
            buffer, offset, started, started_time = [], 0, False, None

        return buffer, offset, started, started_time

    def run(self):
        """运行语音识别主循环"""
        print("Started! Please speak")

        # 启动录音线程
        self.recording_thread = threading.Thread(target=self.start_recording)
        self.recording_thread.start()

        # 初始化状态
        buffer, offset, started, started_time = [], 0, False, None

        # 主处理循环
        while not self.killed:
            try:
                samples = self.samples_queue.get(timeout=0.1)
                buffer = np.concatenate([buffer, samples])
                buffer, offset, started, started_time = self.process_audio(
                    buffer, offset, started, started_time
                )
            except queue.Empty:
                continue

    def stop(self):
        """停止语音识别"""
        self.killed = True
        if self.recording_thread:
            self.recording_thread.join()


class Display:
    """简单的文本显示管理类"""

    def __init__(self):
        self.current_text = ""

    def update_text(self, text):
        self.current_text = text

    def finalize_current_sentence(self):
        text = self.current_text.strip()
        self.current_text = ""
        return text if text else None


def check_audio_devices():
    """检查可用的音频设备"""
    devices = sd.query_devices()
    if not devices:
        print("No microphone devices found")
        sys.exit(1)

    default_input_device_idx = sd.default.device[0]
    print(f'Using default device: {devices[default_input_device_idx]["name"]}')
    return devices


def monitor_pause_status(recognizer):
    """每秒检测一次pause_recording状态的函数"""
    while not recognizer.killed:
        status = "paused" if recognizer.pause_recording.is_set() else "recording"
        print(f"Recording status: {status}")
        time.sleep(1)


def main():
    """主函数"""
    check_audio_devices()

    print("Creating recognizer. Please wait...")
    recognizer = SpeechRecognizer()

    # 启动状态监控线程
    monitor_thread = threading.Thread(
        target=monitor_pause_status, args=(recognizer,), daemon=True
    )
    monitor_thread.start()

    try:
        recognizer.run()
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
    finally:
        recognizer.stop()


if __name__ == "__main__":
    main()
