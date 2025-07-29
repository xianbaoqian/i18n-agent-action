# 背景缘由  
此议题已在KCD 2025北京站、Community Over Code 2025中国峰会讨论过，我们最终决定开发一个AI代理来处理社区国际化(i18n)工作。  
就我个人而言，我无法同时处理[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025分会场的工作。

## 基于我的智能代理开发原则实践

#### 原则推演1：若任务相对固定且存在可靠解决方案，则无需调用大模型增加风险

#### 原则推演2：任务不固定且逐个适配过于复杂时，大模型具有普适性优势，应善用其泛化能力

#### 原则推演3：任务不固定但可逐个适配时，需根据实际情况判断。若使用大模型，必须考虑其错误应答场景并设计容错机制

#### 原则推演4：任务固定但无可靠方案时，若使用大模型尝试创造性解决方案，需保留人工干预通道

# 作为AI代理的实现
## 运作机制
### 手动模式
```
pip3 install -r ./requirements.txt
export api_key={您的密钥}
//python3 main.py {配置文件} {文档目录} {保留字} {可选文件列表}
python3 main.py {仓库绝对路径}/mkdocs.yml {仓库绝对路径}/docs kepler {可选文件列表}
```
运行后需自行执行代码检查(linting)

### 容器模式
```
docker run -it \
  -v path_to_your_repo:/workspace \
  -e model="deepseek-chat" \
  -e base_url="https://api.deepseek.com" \
  -e api_key="..." \
  -e CONFIG_FILE="/workspace/mkdocs.yml" \
  -e DOCS_FOLDER="/workspace/docs" \
  -e RESERVED_WORD="i18n-agent-action" \
  -e FILE_LIST="/workspace/docs/index.md" \
  ghcr.io/samyuan1990/i18n-agent-action:latest
```

## 功能范围界定与实现逻辑

> 避免重复造轮子
- 触发机制不在范畴内
	- 全量更新/差异更新交由人工触发
  - 模型API与接入端点
  > 允许用户选择任意兼容OpenAI API的LLM服务？
	- 配置入口
  > 需从配置文件获取基准语言与目标语言参数

--- 核心范畴 ---
- 第一阶段：基于配置文件
> Sam于2025年7月注：为避免LLM扫描项目产生额外token成本或误判，要求文档维护者直接提供i18n配置文件，通过人工指定的配置文件能100%准确反映国际化配置

- 语言范围如何确定？
	- = 解析配置文件获取语言列表
	- = 基准语言 - 现存语言(通过文件差异分析)

- 结果存储规范
> Sam于2025年7月注：确定翻译范围后，需从配置文件获取命名规则(或由LLM智能识别)

-- 阶段产出：明确源文件列表、翻译目标、语言类型
> Sam于2025年7月注：本阶段最终需输出清晰的任务范围界定

-- 第二阶段：循环执行翻译
- 调用LLM进行翻译
	- 如何获取术语对照表？
	- 增量更新或全量刷新？

> Sam于2025年7月注：需具体说明实现细节

--- 非功能范畴 ---
- PR创建交由现有PR Action实现

> 避免重复造轮子，直接复用现有的PR创建流程