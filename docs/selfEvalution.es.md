# Autoevaluación

Gracias al artículo 2507.21046v3

## Diseño

Para hacer que nuestro agente de traducción se autoevalúe, podemos intentar con la detección automática de nombres propios.
El PR para este repositorio en [enlace](https://github.com/SamYuan1990/i18n-agent-action/pull/53)

La idea central es que el prompt contiene una parte dinámica como nombres propios, ¿qué pasa si le pedimos a un LLM que detecte automáticamente nuevos nombres propios y los fusionamos juntos en la siguiente ronda/fragmento de tareas?

### 1er paso Añadir una variable para capturar nombres propios del LLM

Probado con [diffuser](https://github.com/huggingface/diffusers/pull/12179)
Desde el registro, vemos nombres propios detectados como
`Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks`
Con lo cual podemos comenzar el 2do paso como fusionar nombres propios como reserved_word.

### 2do paso Fusionar los nombres propios y la palabra reservada

Aquí hay una implementación de función de muestra para fusionar nombres propios (como respuesta del LLM) y la palabra reservada
```python
def MergePN(str1, str2):
    # Dividir y mantener el orden eliminando duplicados
    merged = list(OrderedDict.fromkeys(
        [item.strip() for item in str1.split(",")] + 
        [item.strip() for item in str2.split(",")]
    ))

    result = ", ".join(merged)
    return result
```

### Resultado
![](./img/selfevaluate.png)
![](./img/selfevaluate2.png)