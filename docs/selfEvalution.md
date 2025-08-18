# Self evaluation

Thanks to 2507.21046v3

## Design

To make our translate agent self evaluate, we can try with auto detect proper nouns.
The PR for this repo at [link](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

### 1st step we add a var to capture proper nouns from LLM

Tested with [diffuser](https://github.com/huggingface/diffusers/pull/12179)
From log, we see detected proper nouns as
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`
Which we can start 2nd steps as merge proper nouns as reserved_word.

### 2nd step we merge the proper nouns and reserved word

### result

