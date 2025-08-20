# Self evaluation

Thanks to paper 2507.21046v3

## Design

To make our translate agent self evaluate, we can try with auto detect proper nouns.
The PR for this repo at [link](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

The core idea as prompt contains dynamic part as proper nouns, what if we ask LLM to auto detect new proper nouns and we merge them together in next round/chunk of tasks?

### 1st step Add a var to capture proper nouns from LLM

Tested with [diffuser](https://github.com/huggingface/diffusers/pull/12179)
From log, we see detected proper nouns as
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`
Which we can start 2nd steps as merge proper nouns as reserved_word.

### 2nd step Merge the proper nouns and reserved word

Here is a sample function impl to merge proper nouns(as response from LLM) and reserved word
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

### Result
![](./img/selfevaluate.png)
![](./img/selfevaluate2.png)
