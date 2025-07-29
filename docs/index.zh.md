```markdown
# 背景初衷
这一想法源于KCD 2025北京站和Community Over Code 2025中国区的讨论，我们最终决定开发一个AI代理来处理社区国际化(i18n)工作。  
就我个人而言，我无法同时跟进[https://github.com/sustainable-computing-io/kepler-doc/issues/175](https://github.com/sustainable-computing-io/kepler-doc/issues/175)和Community Over Code 2025分会场的工作。

## 基于我的智能体开发原则实践

#### 推论一：如果任务相对固定且存在可靠解决方案，则无需调用大模型增加风险

#### 推论二：任务不固定且逐个适配过于复杂时，应善用大模型的泛化能力

#### 推论三：非固定任务可逐个适配时，若使用大模型需考虑错误应答的容错处理

#### 推论四：固定任务无可靠方案时，若用大模型尝试创造性方案需人工干预

# 作为AI智能体
## 工作原理
### 手动模式
```
pip3 install -r ./requirements.txt
export api_key={你的密钥}
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
- 触发机制不在范畴内
	- 全量更新/差异更新交由人工处理
  - 模型API与接入端点
  > 用户可自由选择兼容OpenAI API的LLM服务
	- 配置入口
  > 需通过配置文件明确源语言与目标语言

--- 核心范畴 ---
- 第一阶段：基于配置文件
> Sam于2025年7月注：为避免LLM扫描项目产生额外token成本或误判，直接要求文档维护者提供i18n配置文件可确保100%准确

- 语言范围如何确定？
	- 解析配置文件获取语言列表
	- 默认语言 - 现有语言(通过文件差异比对)

- 按规则保存结果文件
> Sam于2025年7月注：确定翻译范围后，需从配置文件获取命名规则（或由LLM智能识别）

-- 阶段产出：明确源文件清单、翻译目标、语言类型
> Sam于2025年7月注：本阶段将输出所有任务的明确范围

-- 第二阶段：循环执行翻译
- 调用LLM进行翻译
	- 如何获取术语对照表？
	- 增量更新或全量刷新？

> Sam于2025年7月注：需进一步明确细节

--- 非核心范畴 ---
- PR创建交由现有PR Action处理

> 已有成熟PR Action方案，无需重复开发
``` 

注：
1. 保留了所有技术术语如i18n-agent-action、LLM、API等原文
2. 维持了原始markdown格式与代码块结构
3. 对长句进行了符合中文习惯的断句处理
4. 专业术语（如deepseek-chat）保持原样
5. 时间戳格式与原文保持一致