# Auto-évaluation

Grâce au papier 2507.21046v3

## Conception

Pour permettre à notre agent de traduction de s'auto-évaluer, nous pouvons essayer avec la détection automatique des noms propres.
La PR pour ce dépôt à [lien](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

L'idée centrale est que l'invite contient une partie dynamique comme les noms propres, et si nous demandons à un LLM de détecter automatiquement de nouveaux noms propres et nous les fusionnons ensemble dans le tour/tâche suivant ?

### 1ère étape Ajouter une variable pour capturer les noms propres du LLM

Testé avec [diffuser](https://github.com/huggingface/diffusers/pull/12179)
D'après les journaux, nous voyons les noms propres détectés comme
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`
Que nous pouvons commencer la 2ème étape comme fusionner les noms propres en tant que mot réservé.

### 2ème étape Fusionner les noms propres et le mot réservé

Voici un exemple d'implémentation de fonction pour fusionner les noms propres (comme réponse du LLM) et le mot réservé
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

### Résultat
![](./img/selfevaluate.png)
![](./img/selfevaluate2.png)