# 自我评估

感谢论文 2507.21046v3

## 设计

为了让我们的翻译代理进行自我评估，我们可以尝试自动检测专有名词。
该仓库的拉取请求在[链接](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

核心思路是提示中包含动态部分作为专有名词，如果我们要求大语言模型自动检测新的专有名词，并在下一轮/任务块中合并它们会怎样？

### 第一步 添加一个变量来捕获大语言模型中的专有名词

使用[diffuser](https://github.com/huggingface/diffusers/pull/12179)进行测试
从日志中，我们看到检测到的专有名词为
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`
我们可以开始第二步，将专有名词合并为保留词。

### 第二步 合并专有名词和保留词

这是一个示例函数实现，用于合并专有名词（作为大语言模型的响应）和保留词
```python
def MergePN(str1, str2):
    # 分割并保持顺序去重
    merged = list(OrderedDict.fromkeys(
        [item.strip() for item in str1.split(",")] + 
        [item.strip() for item in str2.split(",")]
    ))

    result = ", ".join(merged)
    return result
```

### 结果
![](./img/selfevaluate.png)
![](./img/selfevaluate2.png)