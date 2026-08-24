---
title: Human Self-Consciousness and Few-Shot Learning
date: 2026-08-12
excerpt: For humans, one sample that violates expectations can change cognition — provided there is sufficient self-consciousness. What about AI?
tags: Self-Consciousness · Few-Shot Learning · Meta-Learning · AI · PINN
---

# Human Self-Consciousness and Few-Shot Learning

---

For humans, a single piece of information that violates expectations can change cognition — provided there is sufficient self-consciousness. One must be aware that what they have seen does not align with their prior expectations.

For AI, the field of few-shot learning probably has developed similar approaches? I'm curious. Wondering if it resembles how PINN directly injects physical concepts into neural networks.

---
from DeepSeek:
**AI's "one-shot cognitive shift" is called meta-learning.** The core idea is "learning to learn." Take the MAML algorithm, for example — it doesn't memorize data directly; instead, it trains an extremely sensitive initial model. When you give it a new sample (like a face), it only needs one gradient descent step to dramatically adjust its cognition. This mirrors human working memory — fast updating but prone to forgetting — essentially a rapid drift in parameter space.

**Closer to your description of "self-awareness" is Test-Time Training.** When encountering an unexpected sample during inference, the model temporarily fine-tunes itself, dynamically updating its internal representations. This is more "self-doubting" than meta-learning, because it acknowledges "my previous cognition might be wrong." However, the cost is significant computational overhead.

---

**PINN.** After asking AI, I understand its principle to be: constraining the solution space so that it necessarily satisfies the physics? That is effectively cutting off a large portion of impossible solutions under the given physical laws?

Whether hard constraints or soft constraints.

Self-consciousness — knowing that what you see does not match your prior expectations.

---

— THE END —

---

# 人的自我意识与少样本学习

---

对人来说，不符合预期的话，只要看一个样本就能更改自己的认知。当然这需要比较高的self-consciousness。自己知道自己看到的什么不符合自己原有的预期。

对AI来说，少样本学习的领域发展大概有发展类似的领域吧？蛮好奇的。似乎不类似于PINN直接给神经网络灌输物理概念。

---
来自DeepSeek:

**AI的“一眼改认知”叫元学习（Meta-Learning）。** 核心是“学会如何学习”，比如MAML算法，它不直接记住数据，而是训练出一个极度敏感的初始模型。当你给它一个新样本（比如那张脸），它只需一步梯度下降就能剧烈调整认知。这模拟了人的工作记忆——快速刷新，但容易遗忘，本质是参数空间的快速漂移。

**更接近你“自我意识”描述的是测试时训练（Test-Time Training）。** 推理时遇到不符合预期的样本，模型会临时自我微调，动态更新内部表征。这比元学习更“自我怀疑”，因为它承认“我之前的认知可能错了”，但代价是计算开销极大。

---

**PINN。** 问AI之后我理解这个的原理是：通过约束使得解空间必然满足物理？也就是砍掉了一大部分该物理定律下不可能的解空间？

不论是硬约束还是软约束。

self-consciousness——自己知道自己看到的什么不符合自己原有的预期。

---

— 完 —