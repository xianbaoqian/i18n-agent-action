from collections import OrderedDict

# str1 = "Diffusers, stable_diffusion, consisid, colab, diffusion"
# str2 = "Diffusers, stable_diffusion, consisid, colab, diffusion, ModularPipeline, YiYiXu, modular-diffdiff, modular-diffdiff-0704, DiffDiffBlocks"


def MergePN(str1, str2):
    # 分割并保持顺序去重
    merged = list(
        OrderedDict.fromkeys(
            [item.strip() for item in str1.split(",")]
            + [item.strip() for item in str2.split(",")]
        )
    )

    result = ", ".join(merged)
    return result


# print(result)
