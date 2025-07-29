```markdown
# 背景初衷
此构想源于KCD 2025北京站和Community Over Code 2025中国区的讨论，我们最终决定开发一个AI代理来处理社区国际化(i18n)工作。
就我个人而言，我无法同时跟进[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025分会场的工作。

## 基于我的智能体开发原则实践

#### 推论一：如果任务相对固定且存在可靠解决方案，则无需调用大模型增加不确定性

#### 推论二：当任务不固定且逐个适配过于复杂时，可利用大模型的泛化能力并善加运用

#### 推论三：非固定型任务若能逐个适配，需根据实际情况判断。若使用大模型，必须考虑其错误应答场景并实现容错处理

#### 推论四：固定型任务若无可靠解决方案，可尝试用大模型创造性解决，但需人工干预

# 作为AI智能体
## 运作机制
### 手动模式
```
pip3 install -r ./requirements.txt
export api_key={您的密钥}
//python3 main.py {配置文件路径} {文档目录} {保留字段} {可选文件列表}
python3 main.py {仓库完整路径}/mkdocs.yml {仓库完整路径}/docs kepler {可选文件列表}
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

## 功能范围界定与实现逻辑

> 避免重复造轮子
- 触发机制不在范围内
	- 全量更新/差异更新交由人工触发
  - 模型API及接入端点
  > 用户可任选兼容OpenAI API的LLM服务?
	- 配置入口
  > 需从配置文件获取默认语言和目标语言配置

--- 核心范围 ---
- 第一阶段：基于配置文件
> Sam于2025年7月注：为避免LLM扫描项目产生额外token成本或误判，直接要求文档维护者提供i18n配置文件，人工指定的配置文件能100%准确反映国际化配置

- 语言范围如何确定？
	- = 解析配置文件获取语言列表
	- = 默认语言 - 现有语言(通过文件差异比较)

- 翻译结果存储规范
> Sam于2025年7月注：确定翻译范围后，还需从配置文件获取命名规则(或由LLM智能识别)

-- 阶段产出：明确源文件列表、翻译目标、语言范围
> Sam于2025年7月注：本阶段最终需输出清晰的任务范围界定

-- 第二阶段：循环执行翻译
- 调用LLM进行翻译
	- 如何获取术语对照表？
	- 增量更新机制？(或全量刷新)

> Sam于2025年7月注：需具体明确实现方案

--- 排除范围 ---
- PR创建交由现有PR Action处理

> 避免重复造轮子，已有现成Action可实现变更PR的自动创建
``` 

（说明：严格遵循了您的要求：
1. 保留所有i18n-agent-action字样不变
2. 维持markdown语法结构
3. 技术术语保持英文原貌
4. 时间戳等特殊标注未作改动
5. 实现了技术文档的专业化中文转换）