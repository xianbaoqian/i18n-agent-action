# 自己評価

論文 2507.21046v3 に感謝します

## 設計

翻訳エージェントを自己評価させるために、自動検出された固有名詞で試すことができます。
このリポジトリの PR は [link](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

コアアイデアは、プロンプトに固有名詞として動的な部分が含まれている場合、LLM に新しい固有名詞を自動検出するように依頼し、次のラウンド/タスクのチャンクでそれらをマージするというものです。

### 1 番目のステップ LLM から固有名詞をキャプチャするための変数を追加

[diffuser](https://github.com/huggingface/diffusers/pull/12179) でテスト済み
ログから、検出された固有名詞は
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`
これらを 2 番目のステップとして、固有名詞を reserved_word としてマージできます。

### 2 番目のステップ 固有名詞と予約語をマージ

以下は、固有名詞（LLM からの応答）と予約語をマージするサンプル関数の実装です
```python
def MergePN(str1, str2):
    # 分割して順序を保ちながら重複を除去
    merged = list(OrderedDict.fromkeys(
        [item.strip() for item in str1.split(",")] + 
        [item.strip() for item in str2.split(",")]
    ))

    result = ", ".join(merged)
    return result
```

### 結果
![](./img/selfevaluate.png)
![](./img/selfevaluate2.png)