以下是按照您的要求翻译的中文内容，保持了原始Markdown格式及`i18n-agent-action`的英文状态：

# 背景初衷
此议题曾在KCD 2025北京站、Community Over Code 2025中国峰会讨论过，我们最终决定开发一个智能代理来处理社区国际化事务。就我个人而言，我无法同时并行处理https://github.com/sustainable-computing-io/kepler-doc/issues/175和Community Over Code 2025分会场的工作。

## 基于我的智能代理开发原则实践

#### 推论一：如果任务相对固定且存在可靠解决方案，则无需调用大模型承担风险

#### 推论二：任务不固定且逐项适配过于复杂时，大模型具有普适性优势，应善用其泛化能力

#### 推论三：任务不固定但可逐项适配时，需根据实际情况判断。若使用大模型，必须考虑其错误应答的可能性并建立容错机制

#### 推论四：任务固定但无可靠解决方案时，若尝试用大模型创造性解决，需人工介入监督

# 作为AI智能代理
## 运作机制
### 手动模式
```
pip3 install -r ./requirements.txt
export api_key={您的密钥}
//python3 main.py {配置文件路径} {文档目录} {保留字} {可选文件列表}
python3 main.py {仓库绝对路径}/mkdocs.yml {仓库绝对路径}/docs kepler {可选文件列表}
```
注意需自行执行代码校验

### 容器模式
```
docker run -it \
  -v /path_to_repo.../kepler-doc:/workspace \
  -e api_key="" \
  -e CONFIG_FILE="/workspace/mkdocs.yml" \
  -e DOCS_FOLDER="/workspace/docs" \
  -e RESERVED_WORD="kepler" \
  -e FILE_LIST="/workspace/docs/index.md" \
  ghcr.io/samyuan1990/i18n-agent-action:latest
```

## 功能范围界定与实现逻辑

> 避免重复造轮子
- 触发机制不在范畴内
	- 全量更新/差异更新交由人工处理
  - 模型API及服务端点
  > 用户可任选兼容OpenAI API的LLM服务？
	- 配置入口
  > 需从配置文件获取默认语言与目标语言参数

--- 核心范畴 ---
- 第一阶段：配置文件解析
> Sam于2025年7月备注：我不希望LLM扫描整个项目，既存在token成本也可能出错。直接要求文档维护者提供i18n配置文件，这种人工指定的方式能100%确保配置准确性

- 语言范围如何确定？
	- = 解析配置文件获取语言列表
	- = 默认语言 - 现有语言（通过文件差异比对）

- 结果存储规范
> Sam于2025年7月备注：确定翻译范围后，还需从配置文件获取命名规则（或让LLM注意此事项）

-- 阶段产出：明确源文件列表、翻译目标、语言范围
> Sam于2025年7月备注：本阶段最终需输出清晰的任务范围清单

-- 第二阶段：循环翻译处理
- 调用LLM进行翻译
	- 如何建立术语对照表？
	- 增量更新或全量刷新？

> Sam于2025年7月备注：需具体说明

--- 非功能范畴 ---
- PR创建交由PR Action处理

> 避免重复造轮子，已有现成的PR Action可实现变更提交流程