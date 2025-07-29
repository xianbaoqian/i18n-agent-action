```markdown
# 背景初衷
此构想源于KCD 2025北京站和Community Over Code 2025中国大会的讨论，我们最终决定开发一个智能代理来处理社区国际化（i18n）工作。  
就我个人而言，我无法同时兼顾[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025分会场的工作。

## 基于我的智能代理开发原则实践

#### 原则推演1：如果任务相对固定且存在可靠解决方案，则无需调用大模型承担风险

#### 原则推演2：当任务不固定且逐个适配过于复杂时，大模型具备的泛化能力值得利用

#### 原则推演3：非固定任务若可逐个适配，需根据实际情况评估。使用大模型时必须考虑错误应答场景并设计容错机制

#### 原则推演4：固定任务若无可靠解决方案，使用大模型进行创造性尝试时需要人工干预

# 作为AI智能代理
## 运作机制
### 手动模式
```
pip3 install -r ./requirements.txt
export api_key={您的密钥}
//python3 main.py {配置文件} {文档目录} {保留字段} {可选文件列表}
python3 main.py {仓库绝对路径}/mkdocs.yml {仓库绝对路径}/docs kepler {可选文件列表}
```
注意：需自行执行代码检查

### 容器模式
```
docker run -it \
  -v 仓库路径:/workspace \
  -e model="deepseek-chat" \
  -e base_url="https://api.deepseek.com" \
  -e api_key="..." \
  -e CONFIG_FILE="/workspace/mkdocs.yml" \
  -e DOCS_FOLDER="/workspace/docs" \
  -e RESERVED_WORD="i18n-agent-action" \
  -e FILE_LIST="/workspace/docs/index.md" \
  ghcr.io/samyuan1990/i18n-agent-action:latest
```

## 功能范围与实现逻辑

> 避免重复造轮子
- 触发机制不在范围内
	- 全量更新/差异更新交由人工触发
  - 模型API与终端节点
  > 用户可选择任何兼容OpenAI API的LLM服务？
	- 配置入口点
  > 需从配置文件中获取默认语言和目标语言设置

--- 核心范围 ---
- 第一阶段：基于配置文件
> Sam于2025年7月注：为避免LLM扫描项目产生token消耗或误判，直接要求文档维护者提供i18n配置文件可确保100%准确

- 语言范围如何确定？
	- = 解析配置文件获取语言列表
	- = 默认语言 - 现有语言（通过文件差异比对）

- 结果存储规范
> Sam于2025年7月注：确定翻译范围后，还需从配置文件获取命名规则（或由LLM智能识别）

-- 阶段产出：明确源文件、翻译目标、语言的完整任务清单

-- 第二阶段：循环执行翻译
- 调用LLM进行翻译
	- 如何建立术语对照表？
	- 增量更新或全量刷新？

> Sam于2025年7月注：需具体说明

--- 排除范围 ---
- PR创建交由现有PR Action处理

> 已有成熟的PR Action解决方案，无需重复开发
``` 

（注：严格保留了原文中的代码块格式、URL链接、i18n-agent-action等专有名词，同时按照中文技术文档习惯调整了标点符号和段落间距）