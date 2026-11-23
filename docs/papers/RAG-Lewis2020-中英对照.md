---
title: "RAG 论文中英对照：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*"
---
# RAG 论文中英对照：*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*

> **原文**：Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020. arXiv:2005.11401v4
> **来源**：<https://arxiv.org/abs/2005.11401>（正文据 arXiv HTML v4 提取，附录与参考文献未译）
> **用途**：D01「RAG 到底在解决什么问题」的当日读物。

**阅读约定**：`>` 引用块 = 英文原文；其下正文 = 中文译文。公式保留 LaTeX 记号，术语首次出现时括注英文。

---

## 摘要 / Abstract

> Large pre-trained language models have been shown to store factual knowledge in their parameters, and achieve state-of-the-art results when fine-tuned on downstream NLP tasks. However, their ability to access and precisely manipulate knowledge is still limited, and hence on knowledge-intensive tasks, their performance lags behind task-specific architectures. Additionally, providing provenance for their decisions and updating their world knowledge remain open research problems. Pre-trained models with a differentiable access mechanism to explicit non-parametric memory have so far been only investigated for extractive downstream tasks. We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) — models which combine pre-trained parametric and non-parametric memory for language generation. We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We compare two RAG formulations, one which conditions on the same retrieved passages across the whole generated sequence, and another which can use different passages per token. We fine-tune and evaluate our models on a wide range of knowledge-intensive NLP tasks and set the state of the art on three open domain QA tasks, outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures. For language generation tasks, we find that RAG models generate more specific, diverse and factual language than a state-of-the-art parametric-only seq2seq baseline.

大型预训练语言模型已被证明能在参数中存储事实知识，并在下游 NLP 任务上微调后取得当前最佳（state-of-the-art）结果。然而，它们访问并精确操作知识的能力仍然有限，因此在知识密集型任务上，其表现落后于任务专用架构。此外，为其决策提供溯源（provenance，即「这个答案的依据在哪」）、以及更新其世界知识，仍是未解决的研究问题。迄今为止，具备对显式非参数记忆做**可微访问**（differentiable access）机制的预训练模型，只在抽取式（extractive）下游任务上被研究过。

我们探索一套通用的微调配方，用于检索增强生成（retrieval-augmented generation，RAG）——即把预训练的参数记忆与非参数记忆结合起来做语言生成的模型。我们提出的 RAG 模型中，参数记忆是一个预训练 seq2seq 模型，非参数记忆是 Wikipedia 的稠密向量索引，由预训练的神经检索器访问。我们比较两种 RAG 形式：一种在整个生成序列上条件于同一批检索段落；另一种可以逐 token 使用不同段落。我们在广泛的知识密集型 NLP 任务上微调并评估模型，在三个开放域问答任务上取得当前最佳，超过了参数化 seq2seq 模型与任务专用的「检索-抽取」（retrieve-and-extract）架构。对于语言生成任务，我们发现 RAG 生成的文本比当前最佳的纯参数化 seq2seq 基线更具体、更多样、也更符合事实。

---

## 1 引言 / Introduction

> Pre-trained neural language models have been shown to learn a substantial amount of in-depth knowledge from data [47]. They can do so without any access to an external memory, as a parameterized implicit knowledge base [51, 52]. While this development is exciting, such models do have downsides: They cannot easily expand or revise their memory, can't straightforwardly provide insight into their predictions, and may produce "hallucinations" [38]. Hybrid models that combine parametric memory with non-parametric (i.e., retrieval-based) memories [20, 26, 48] can address some of these issues because knowledge can be directly revised and expanded, and accessed knowledge can be inspected and interpreted. REALM [20] and ORQA [31], two recently introduced models that combine masked language models [8] with a differentiable retriever, have shown promising results, but have only explored open-domain extractive question answering. Here, we bring hybrid parametric and non-parametric memory to the "workhorse of NLP," i.e. sequence-to-sequence (seq2seq) models.

预训练神经语言模型已被证明能从数据中学到大量深入的知识。它们无需访问任何外部记忆即可做到这一点，因为模型本身就是一个参数化的隐式知识库（parameterized implicit knowledge base）。这一进展令人兴奋，但这类模型也有缺点：它们**难以扩展或修订记忆**，**无法直截了当地解释自己的预测**，还可能产生「幻觉」（hallucination）。把参数记忆与非参数（即基于检索的）记忆结合的混合模型，可以缓解其中部分问题——因为知识可以被直接修订和扩充，被访问到的知识也可以被检视与解释。REALM 与 ORQA 这两个新近提出的模型把掩码语言模型与可微检索器结合，已显示出有希望的结果，但它们只探索了开放域抽取式问答。本文把参数记忆与非参数记忆的混合引入「NLP 的主力军」，即序列到序列（seq2seq）模型。

> We endow pre-trained, parametric-memory generation models with a non-parametric memory through a general-purpose fine-tuning approach which we refer to as retrieval-augmented generation (RAG). We build RAG models where the parametric memory is a pre-trained seq2seq transformer, and the non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural retriever. We combine these components in a probabilistic model trained end-to-end (Fig. 1). The retriever (Dense Passage Retriever [26], henceforth DPR) provides latent documents conditioned on the input, and the seq2seq model (BART [32]) then conditions on these latent documents together with the input to generate the output. We marginalize the latent documents with a top-K approximation, either on a per-output basis (assuming the same document is responsible for all tokens) or a per-token basis (where different documents are responsible for different tokens). Like T5 [51] or BART, RAG can be fine-tuned on any seq2seq task, whereby both the generator and retriever are jointly learned.

我们通过一套通用微调方法，为「参数记忆型」的预训练生成模型配上一份非参数记忆，并称之为检索增强生成（RAG）。在构建的 RAG 模型中，参数记忆是一个预训练的 seq2seq Transformer，非参数记忆是 Wikipedia 的稠密向量索引，由预训练的神经检索器访问。我们把这些组件放进一个端到端训练的概率模型中（图 1）。检索器（Dense Passage Retriever，下文简称 DPR）以输入为条件给出潜在文档（latent documents）的分布；seq2seq 模型（BART）再以这些潜在文档连同输入为条件生成输出。我们用 top-K 近似对潜在文档做边缘化（marginalize），有两种口径：**按整条输出**（假设同一个文档对所有 token 负责），或**按每个 token**（不同 token 由不同文档负责）。与 T5 或 BART 一样，RAG 可以在任意 seq2seq 任务上微调，且生成器与检索器是联合学习的。

> There has been extensive previous work proposing architectures to enrich systems with non-parametric memory which are trained from scratch for specific tasks, e.g. memory networks [64, 55], stack-augmented networks [25] and memory layers [30]. In contrast, we explore a setting where both parametric and non-parametric memory components are pre-trained and pre-loaded with extensive knowledge. Crucially, by using pre-trained access mechanisms, the ability to access knowledge is present without additional training.

以往已有大量工作提出为非参数记忆扩充系统架构，但它们都是针对特定任务从零训练的，例如记忆网络（memory networks）、栈增强网络（stack-augmented networks）和记忆层（memory layers）。与之不同，我们探索的场景中，参数记忆与非参数记忆两个组件都是**预训练好、且已预装入大量知识**的。关键在于，借助预训练的访问机制，访问知识的能力**无需额外训练**就已具备。

> Our results highlight the benefits of combining parametric and non-parametric memory with generation for knowledge-intensive tasks—tasks that humans could not reasonably be expected to perform without access to an external knowledge source. Our RAG models achieve state-of-the-art results on open Natural Questions [29], WebQuestions [3] and CuratedTrec [2] and strongly outperform recent approaches that use specialised pre-training objectives on TriviaQA [24]. Despite these being extractive tasks, we find that unconstrained generation outperforms previous extractive approaches. For knowledge-intensive generation, we experiment with MS-MARCO [1] and Jeopardy question generation, and we find that our models generate responses that are more factual, specific, and diverse than a BART baseline. For FEVER [56] fact verification, we achieve results within 4.3% of state-of-the-art pipeline models which use strong retrieval supervision. Finally, we demonstrate that the non-parametric memory can be replaced to update the models' knowledge as the world changes.

我们的结果凸显了「参数记忆 + 非参数记忆 + 生成」这一组合在知识密集型任务上的好处——所谓知识密集型任务，指人类若不借助外部知识源就无法合理完成的任务。RAG 在开放的 Natural Questions、WebQuestions 与 CuratedTrec 上取得当前最佳，并在 TriviaQA 上大幅超过近期使用专门预训练目标的方法。尽管这些都是抽取式任务，我们发现**不受约束的生成**反而优于以往的抽取式方法。在知识密集型生成方面，我们在 MS-MARCO 与 Jeopardy 问题生成上做实验，发现模型生成的回答比 BART 基线更符合事实、更具体、也更多样。在 FEVER 事实核查任务上，我们的结果与使用强检索监督的当前最佳流水线模型相差在 4.3% 以内。最后，我们演示了非参数记忆可以整体替换，从而在世界变化时更新模型的知识。

> Figure 1: Overview of our approach. We combine a pre-trained retriever (Query Encoder + Document Index) with a pre-trained seq2seq model (Generator) and fine-tune end-to-end. For query $x$, we use Maximum Inner Product Search (MIPS) to find the top-K documents $z_{i}$. For final prediction $y$, we treat $z$ as a latent variable and marginalize over seq2seq predictions given different documents.

**图 1（方法总览）**：我们把预训练检索器（查询编码器 Query Encoder + 文档索引 Document Index）与预训练 seq2seq 模型（生成器 Generator）组合起来，端到端微调。对查询 $x$，用最大内积搜索（Maximum Inner Product Search，MIPS）找出 top-K 文档 $z_{i}$；对最终预测 $y$，把 $z$ 当作潜在变量，对不同文档下 seq2seq 的预测做边缘化。

**脚注 1（原注，节译）**：Code to run experiments with RAG has been open-sourced as part of the HuggingFace Transformers Library [66] … An interactive demo of RAG models can be found at https://huggingface.co/rag/

脚注 1：RAG 实验代码已作为 HuggingFace Transformers 库的一部分开源，地址 <https://github.com/huggingface/transformers/blob/master/examples/rag/>；RAG 模型的交互式 demo 见 <https://huggingface.co/rag/>。
---

## 2 方法 / Methods

> We explore RAG models, which use the input sequence $x$ to retrieve text documents $z$ and use them as additional context when generating the target sequence $y$. As shown in Figure 1, our models leverage two components: (i) a retriever $p_{\eta}(z|x)$ with parameters $\eta$ that returns (top-K truncated) distributions over text passages given a query $x$ and (ii) a generator $p_{\theta}(y_{i}|x,z,y_{1:i-1})$ parametrized by $\theta$ that generates a current token based on a context of the previous $i-1$ tokens $y_{1:i-1}$, the original input $x$ and a retrieved passage $z$.

我们研究 RAG 模型：它用输入序列 $x$ 检索出文本文档 $z$，并在生成目标序列 $y$ 时把检索到的文档作为额外上下文。如图 1 所示，模型由两个组件构成：

1. **检索器** $p_{\eta}(z|x)$，参数为 $\eta$：给定查询 $x$，返回文本段落的分布（截断到 top-K）；
2. **生成器** $p_{\theta}(y_{i}|x,z,y_{1:i-1})$，参数为 $\theta$：基于前 $i-1$ 个 token $y_{1:i-1}$、原始输入 $x$ 以及检索到的段落 $z$，生成当前 token。

> To train the retriever and generator end-to-end, we treat the retrieved document as a latent variable. We propose two models that marginalize over the latent documents in different ways to produce a distribution over generated text. In one approach, RAG-Sequence, the model uses the same document to predict each target token. The second approach, RAG-Token, can predict each target token based on a different document. In the following, we formally introduce both models and then describe the $p_{\eta}$ and $p_{\theta}$ components, as well as the training and decoding procedure.

为端到端训练检索器与生成器，我们把检索到的文档视为**潜在变量**（latent variable）。我们提出两种模型，用不同方式对潜在文档做边缘化，从而得到生成文本的分布：

- **RAG-Sequence**：预测每个目标 token 时都用**同一个**文档；
- **RAG-Token**：预测每个目标 token 时可以基于**不同的**文档。

下面先正式介绍这两个模型，再说明 $p_{\eta}$ 与 $p_{\theta}$ 两个组件，以及训练与解码流程。

### 2.1 模型 / Models

#### RAG-Sequence 模型 / RAG-Sequence Model

> The RAG-Sequence model uses the same retrieved document to generate the complete sequence. Technically, it treats the retrieved document as a single latent variable that is marginalized to get the seq2seq probability $p(y|x)$ via a top-K approximation. Concretely, the top K documents are retrieved using the retriever, and the generator produces the output sequence probability for each document, which are then marginalized,

RAG-Sequence 用同一个检索到的文档生成**整条**序列。技术上，它把该文档当作单个潜在变量，通过 top-K 近似做边缘化得到 seq2seq 概率 $p(y|x)$：检索器取出 top-K 文档，生成器为每个文档给出整条输出序列的概率，再把这些概率边缘化：

$$
p_{\text{RAG-Sequence}}(y|x)\;\approx\;\sum_{z\in\text{top-}k(p(\cdot|x))}p_{\eta}(z|x)\,p_{\theta}(y|x,z)\;=\;\sum_{z\in\text{top-}k(p(\cdot|x))}p_{\eta}(z|x)\prod_{i=1}^{N}p_{\theta}(y_{i}|x,z,y_{1:i-1})
$$

（读法：先按文档加权，再在文档内逐 token 连乘，最后对 top-K 个文档求和——「一篇文档讲完整个答案」。）

#### RAG-Token 模型 / RAG-Token Model

> In the RAG-Token model we can draw a different latent document for each target token and marginalize accordingly. This allows the generator to choose content from several documents when producing an answer. Concretely, the top K documents are retrieved using the retriever, and then the generator produces a distribution for the next output token for each document, before marginalizing, and repeating the process with the following output token, Formally, we define:

RAG-Token 中，每个目标 token 都可以抽取**不同的**潜在文档并相应边缘化，这使生成器在给出答案时能从多个文档里各取所需。具体做法是：检索 top-K 文档后，生成器为**每个文档**给出下一个输出 token 的分布，先边缘化，再用同样的方式处理下一个输出 token。形式化地：

$$
p_{\text{RAG-Token}}(y|x)\;\approx\;\prod_{i=1}^{N}\;\sum_{z\in\text{top-}k(p(\cdot|x))}p_{\eta}(z|x)\,p_{\theta}(y_{i}|x,z,y_{1:i-1})
$$

（读法：每一步先在文档维求和、再逐 token 连乘——「每个 token 各自找最合适的文档」。与 RAG-Sequence 的差别只在于**求和与连乘的先后顺序**。）

> Finally, we note that RAG can be used for sequence classification tasks by considering the target class as a target sequence of length one, in which case RAG-Sequence and RAG-Token are equivalent.

最后说明：把目标类别视为长度为 1 的目标序列，RAG 即可用于序列分类任务；此时 RAG-Sequence 与 RAG-Token 等价。

### 2.2 检索器：DPR / Retriever: DPR

> The retrieval component $p_{\eta}(z|x)$ is based on DPR [26]. DPR follows a bi-encoder architecture:

检索组件 $p_{\eta}(z|x)$ 基于 DPR。DPR 采用双塔（bi-encoder，双编码器）架构：

$$
p_{\eta}(z|x)\propto\exp\left(\mathbf{d}(z)^{\top}\mathbf{q}(x)\right),\qquad \mathbf{d}(z)=\text{BERT}_{d}(z),\;\;\mathbf{q}(x)=\text{BERT}_{q}(x)
$$

> where $\mathbf{d}(z)$ is a dense representation of a document produced by a BERTBASE document encoder [8], and $\mathbf{q}(x)$ a query representation produced by a query encoder, also based on BERTBASE. Calculating $\text{top-k}(p_{\eta}(\cdot|x))$, the list of $k$ documents $z$ with highest prior probability $p_{\eta}(z|x)$, is a Maximum Inner Product Search (MIPS) problem, which can be approximately solved in sub-linear time [23]. We use a pre-trained bi-encoder from DPR to initialize our retriever and to build the document index. This retriever was trained to retrieve documents which contain answers to TriviaQA [24] questions and Natural Questions [29]. We refer to the document index as the non-parametric memory.

其中 $\mathbf{d}(z)$ 是 BERT_BASE 文档编码器产出的文档稠密表示，$\mathbf{q}(x)$ 是由同样基于 BERT_BASE 的查询编码器产出的查询表示。计算 $\text{top-k}(p_{\eta}(\cdot|x))$——即按先验概率 $p_{\eta}(z|x)$ 最高的 $k$ 个文档组成的列表——是一个**最大内积搜索**（MIPS）问题，可以在次线性时间内近似求解。我们用 DPR 预训练好的双塔来初始化检索器并构建文档索引。该检索器训练时的目标，是检索出**包含 TriviaQA 与 Natural Questions 问题答案**的文档。我们把这份文档索引称为**非参数记忆**。

### 2.3 生成器：BART / Generator: BART

> The generator component $p_{\theta}(y_{i}|x,z,y_{1:i-1})$ could be modelled using any encoder-decoder. We use BART-large [32], a pre-trained seq2seq transformer [58] with 400M parameters. To combine the input $x$ with the retrieved content $z$ when generating from BART, we simply concatenate them. BART was pre-trained using a denoising objective and a variety of different noising functions. It has obtained state-of-the-art results on a diverse set of generation tasks and outperforms comparably-sized T5 models [32]. We refer to the BART generator parameters $\theta$ as the parametric memory henceforth.

生成器组件 $p_{\theta}(y_{i}|x,z,y_{1:i-1})$ 可以用任意编码器-解码器建模。我们使用 BART-large——一个 4 亿参数的预训练 seq2seq Transformer。用 BART 生成时，把输入 $x$ 与检索内容 $z$ **直接拼接**（concatenate）即可。BART 以去噪（denoising）目标、配合多种加噪函数预训练，已在多种生成任务上取得当前最佳，并优于规模相当的 T5。后文把 BART 生成器参数 $\theta$ 称作**参数记忆**。

**📌 译注**：「直接拼接」这一句是全文最朴素、也最值得盯住的实现细节——RAG 在生成侧没有引入任何新结构，检索内容只是作为一段前缀上下文塞进 encoder。

### 2.4 训练 / Training

> We jointly train the retriever and generator components without any direct supervision on what document should be retrieved. Given a fine-tuning training corpus of input/output pairs $(x_{j},y_{j})$, we minimize the negative marginal log-likelihood of each target, $\sum_{j}-\log p(y_{j}|x_{j})$ using stochastic gradient descent with Adam [28]. Updating the document encoder $\text{BERT}_{d}$ during training is costly as it requires the document index to be periodically updated as REALM does during pre-training [20]. We do not find this step necessary for strong performance, and keep the document encoder (and index) fixed, only fine-tuning the query encoder $\text{BERT}_{q}$ and the BART generator.

我们联合训练检索器与生成器，但**对「该检索哪个文档」没有任何直接监督**。给定由输入/输出对 $(x_{j},y_{j})$ 组成的微调语料，我们用 Adam 做随机梯度下降，最小化每个目标的**负边缘对数似然**：

$$
\sum_{j}-\log p(y_{j}|x_{j})
$$

训练中更新文档编码器 $\text{BERT}_{d}$ 代价很高，因为需要像 REALM 预训练时那样周期性重建文档索引。我们发现这一步对取得强性能并不必要，因此**固定**文档编码器（以及索引），只微调查询编码器 $\text{BERT}_{q}$ 与 BART 生成器。

**📌 译注｜呼应 RAGFlow**：「只训查询侧、冻结文档侧」是 RAG 能被工程落地的关键取舍——索引不必随训练翻滚。RAGFlow 里 embedding 模型对文档与查询分别调用同一模型、索引离线构建，正是同一思路的工程化。

### 2.5 解码 / Decoding

> At test time, RAG-Sequence and RAG-Token require different ways to approximate $\argmax_{y}p(y|x)$.

测试时，RAG-Sequence 与 RAG-Token 需要不同的方式来近似 $\argmax_{y}p(y|x)$。

#### RAG-Token

> The RAG-Token model can be seen as a standard, autoregressive seq2seq generator with transition probability: … To decode, we can plug $p'_{\theta}(y_{i}|x,y_{1:i-1})$ into a standard beam decoder.

RAG-Token 可以看作一个标准的自回归 seq2seq 生成器，只是转移概率改成了「先对文档边缘化」的形式：

$$
p'_{\theta}(y_{i}|x,y_{1:i-1})=\sum_{z\in\text{top-}k(p(\cdot|x))}p_{\eta}(z_{i}|x)\,p_{\theta}(y_{i}|x,z_{i},y_{1:i-1})
$$

解码时，把 $p'_{\theta}(y_{i}|x,y_{1:i-1})$ 直接插进标准**束搜索**（beam search）即可。

#### RAG-Sequence

> For RAG-Sequence, the likelihood $p(y|x)$ does not break into a conventional per-token likelihood, hence we cannot solve it with a single beam search. Instead, we run beam search for each document $z$, scoring each hypothesis using $p_{\theta}(y_{i}|x,z,y_{1:i-1})$. This yields a set of hypotheses $Y$, some of which may not have appeared in the beams of all documents. To estimate the probability of an hypothesis $y$ we run an additional forward pass for each document $z$ for which $y$ does not appear in the beam, multiply generator probability with $p_{\eta}(z|x)$ and then sum the probabilities across beams for the marginals. We refer to this decoding procedure as "Thorough Decoding." For longer output sequences, $|Y|$ can become large, requiring many forward passes. For more efficient decoding, we can make a further approximation that $p_{\theta}(y|x,z_{i})\approx 0$ where $y$ was not generated during beam search from $x,z_{i}$. This avoids the need to run additional forward passes once the candidate set $Y$ has been generated. We refer to this decoding procedure as "Fast Decoding."

对 RAG-Sequence，似然 $p(y|x)$ **不能**分解成常规的逐 token 似然（求和在外、连乘在内），因此无法用单次束搜索求解。做法是**为每个文档 $z$ 各跑一次束搜索**，用 $p_{\theta}(y_{i}|x,z,y_{1:i-1})$ 给每条假设打分。这样得到假设集合 $Y$，其中有些假设并未出现在所有文档的束里。要估计某条假设 $y$ 的概率，对「$y$ 未出现在其束中」的每个文档 $z$ 额外做一次前向计算，把生成器概率乘以 $p_{\eta}(z|x)$，再把各条束的概率求和完成边缘化——这称为**彻底解码**（Thorough Decoding）。输出较长时 $|Y|$ 会很大，需要大量前向计算。更高效的做法是进一步近似：若 $y$ 在「以 $x,z_{i}$ 为条件」的束搜索中根本没被生成，就令 $p_{\theta}(y|x,z_{i})\approx 0$——这样候选集 $Y$ 一旦生成，就无需额外前向计算。这称为**快速解码**（Fast Decoding）。

**📌 工程含义**：RAG-Sequence 的「每文档一次束搜索」在批量服务里意味着 beam × k 次解码，成本随检索数线性增长；这也是后来工程实现（含 RAGFlow 一类系统）普遍只取「拼接后单次生成」、把多文档聚合交给 prompt 的原因。
---

## 3 实验 / Experiments

> We experiment with RAG in a wide range of knowledge-intensive tasks. For all experiments, we use a single Wikipedia dump for our non-parametric knowledge source. Following Lee et al. [31] and Karpukhin et al. [26], we use the December 2018 dump. Each Wikipedia article is split into disjoint 100-word chunks, to make a total of 21M documents. We use the document encoder to compute an embedding for each document, and build a single MIPS index using FAISS [23] with a Hierarchical Navigable Small World approximation for fast retrieval [37]. During training, we retrieve the top $k$ documents for each query. We consider $k\in\{5,10\}$ for training and set $k$ for test time using dev data. We now discuss experimental details for each task.

我们在广泛的知识密集型任务上做 RAG 实验。所有实验共用同一份 Wikipedia dump 作为非参数知识源：沿用 Lee 等与 Karpukhin 等的做法，使用 **2018 年 12 月**的 dump。每篇 Wikipedia 文章被切成**互不重叠的 100 词块**（chunk），共 **2100 万**篇文档。用文档编码器为每篇文档算一个 embedding，再用 FAISS 建立单一 MIPS 索引，其中使用 **HNSW（分层可导航小世界）近似**来加速检索。训练时对每个查询检索 top $k$ 篇文档，训练取 $k\in\{5,10\}$，测试时的 $k$ 由 dev 数据确定。下面分别讨论各任务的实验细节。

**📌 对照 D01 链路图**：这一段就是「切分 → 编码 → 建索引」三个环节的 2020 年版本——固定 100 词、不重叠、21M 条、单索引、HNSW。今天 RAGFlow 的 `naive.chunk` 与 `search.retrieval` 只是把「固定 100 词」换成了按模板/按标题层级切、把单一索引换成了多知识库多索引。

### 3.1 开放域问答 / Open-domain Question Answering

> Open-domain question answering (QA) is an important real-world application and common testbed for knowledge-intensive tasks [20]. We treat questions and answers as input-output text pairs $(x,y)$ and train RAG by directly minimizing the negative log-likelihood of answers. We compare RAG to the popular extractive QA paradigm [5, 7, 31, 26], where answers are extracted spans from retrieved documents, relying primarily on non-parametric knowledge. We also compare to "Closed-Book QA" approaches [52], which, like RAG, generate answers, but which do not exploit retrieval, instead relying purely on parametric knowledge. We consider four popular open-domain QA datasets: Natural Questions (NQ) [29], TriviaQA (TQA) [24]. WebQuestions (WQ) [3] and CuratedTrec (CT) [2]. As CT and WQ are small, we follow DPR [26] by initializing CT and WQ models with our NQ RAG model. We use the same train/dev/test splits as prior work [31, 26] and report Exact Match (EM) scores. For TQA, to compare with T5 [52], we also evaluate on the TQA Wiki test set.

开放域问答（QA）是重要的真实应用，也是知识密集型任务的常用试验台。我们把问题与答案当作输入-输出文本对 $(x,y)$，通过直接最小化答案的负对数似然来训练 RAG。对比对象有两类：

- **抽取式 QA** 范式：答案是从检索文档中**抽出的片段**，主要依赖非参数知识；
- **闭卷 QA**（Closed-Book QA）：与 RAG 一样是「生成」答案，但**不用检索**，纯靠参数知识。

我们使用四个常用开放域 QA 数据集：Natural Questions（NQ）、TriviaQA（TQA）、WebQuestions（WQ）与 CuratedTrec（CT）。由于 CT 与 WQ 规模较小，沿用 DPR 的做法，用 NQ 上训好的 RAG 模型来初始化 CT 与 WQ 的模型。训练/验证/测试划分与先前工作一致，指标为**精确匹配**（Exact Match，EM）。对 TQA，为与 T5 可比，我们也在 TQA Wiki 测试集上评估。

### 3.2 摘要式问答 / Abstractive Question Answering

> RAG models can go beyond simple extractive QA and answer questions with free-form, abstractive text generation. To test RAG's natural language generation (NLG) in a knowledge-intensive setting, we use the MSMARCO NLG task v2.1 [43]. The task consists of questions, ten gold passages retrieved from a search engine for each question, and a full sentence answer annotated from the retrieved passages. We do not use the supplied passages, only the questions and answers, to treat MSMARCO as an open-domain abstractive QA task. MSMARCO has some questions that cannot be answered in a way that matches the reference answer without access to the gold passages, such as "What is the weather in Volcano, CA?" so performance will be lower without using gold passages. We also note that some MSMARCO questions cannot be answered using Wikipedia alone. Here, RAG can rely on parametric knowledge to generate reasonable responses.

RAG 不止能做抽取式问答，还能用自由的、摘要式（abstractive）文本生成来回答问题。为检验 RAG 在知识密集型场景下的自然语言生成（NLG）能力，我们使用 MSMARCO NLG v2.1 任务。该任务包含：问题、每个问题从搜索引擎检索到的十条**金标段落**（gold passages），以及基于这些段落标注的一整句答案。我们**不使用**提供的段落，只用问题与答案，从而把 MSMARCO 当作开放域摘要式问答来做。MSMARCO 中有一些问题若拿不到金标段落就无法答到与参考答案一致（例如「加州 Volcano 的天气如何？」），所以不用金标段落时性能必然更低。另需注意，部分 MSMARCO 问题光靠 Wikipedia 也答不了——此时 RAG 可以依靠参数知识给出合理的回答。

### 3.3 Jeopardy 问题生成 / Jeopardy Question Generation

> To evaluate RAG's generation abilities in a non-QA setting, we study open-domain question generation. Rather than use questions from standard open-domain QA tasks, which typically consist of short, simple questions, we propose the more demanding task of generating Jeopardy questions. Jeopardy is an unusual format that consists of trying to guess an entity from a fact about that entity. For example, "The World Cup" is the answer to the question "In 1986 Mexico scored as the first country to host this international sports competition twice." As Jeopardy questions are precise, factual statements, generating Jeopardy questions conditioned on their answer entities constitutes a challenging knowledge-intensive generation task.

为在非问答场景下评估 RAG 的生成能力，我们研究开放域**问题生成**。标准开放域 QA 中的问题通常短而简单；我们不采用它们，而是提出更有难度的任务：生成 **Jeopardy 问题**。Jeopardy（美国电视智力竞赛）的格式很特别——从一个关于某实体的事实出发，去猜这个实体。例如「1986 年墨西哥成为第一个两次主办这项国际体育赛事的国家」对应的答案是「世界杯」。由于 Jeopardy 问题是精确的、事实性的陈述，以答案实体为条件生成 Jeopardy 问题，构成一个有挑战性的知识密集型生成任务。

> We use the splits from SearchQA [10], with 100K train, 14K dev, and 27K test examples. As this is a new task, we train a BART model for comparison. Following [67], we evaluate using the SQuAD-tuned Q-BLEU-1 metric [42]. Q-BLEU is a variant of BLEU with a higher weight for matching entities and has higher correlation with human judgment for question generation than standard metrics. We also perform two human evaluations, one to assess generation factuality, and one for specificity. We define factuality as whether a statement can be corroborated by trusted external sources, and specificity as high mutual dependence between the input and output [33]. We follow best practice and use pairwise comparative evaluation [34]. Evaluators are shown an answer and two generated questions, one from BART and one from RAG. They are then asked to pick one of four options—question A is better, question B is better, both are good, or neither is good.

数据划分沿用 SearchQA：训练 10 万、验证 1.4 万、测试 2.7 万条。由于这是新任务，我们另训一个 BART 模型作对比。评测沿用先前工作，用经过 SQuAD 调优的 **Q-BLEU-1** 指标：Q-BLEU 是 BLEU 的变体，对实体匹配赋予更高权重，在问题生成任务上与人工判断的相关性高于标准指标。我们还做了两项人工评测，一项评**事实性**（factuality），一项评**具体性**（specificity）。事实性定义为「陈述能否被可信的外部来源佐证」，具体性定义为输入与输出之间的高度相互依赖。评测遵循最佳实践采用**成对比较**：给评测者一个答案和两条生成的问题（一条来自 BART、一条来自 RAG），让其从四个选项中选一个——A 更好、B 更好、两者都好、两者都不好。

### 3.4 事实核查 / Fact Verification

> FEVER [56] requires classifying whether a natural language claim is supported or refuted by Wikipedia, or whether there is not enough information to decide. The task requires retrieving evidence from Wikipedia relating to the claim and then reasoning over this evidence to classify whether the claim is true, false, or unverifiable from Wikipedia alone. FEVER is a retrieval problem coupled with an challenging entailment reasoning task. It also provides an appropriate testbed for exploring the RAG models' ability to handle classification rather than generation. We map FEVER class labels (supports, refutes, or not enough info) to single output tokens and directly train with claim-class pairs. Crucially, unlike most other approaches to FEVER, we do not use supervision on retrieved evidence. In many real-world applications, retrieval supervision signals aren't available, and models that do not require such supervision will be applicable to a wider range of tasks. We explore two variants: the standard 3-way classification task (supports/refutes/not enough info) and the 2-way (supports/refutes) task studied in Thorne and Vlachos [57]. In both cases we report label accuracy.

FEVER 要求判定一条自然语言论断是被 Wikipedia **支持**、**反驳**，还是**信息不足**。该任务需要先从 Wikipedia 检索与论断相关的证据，再对这些证据做推理，判断论断为真、为假，或无法仅凭 Wikipedia 判定。FEVER 是「检索问题 + 有难度的蕴含推理任务」的组合，也正好用来检验 RAG 处理**分类**（而非生成）的能力。我们把 FEVER 的类别标签（supports / refutes / not enough info）映射为单个输出 token，直接用「论断-类别」对训练。关键在于：与大多数 FEVER 方法不同，我们**不使用对检索证据的监督**。现实应用中往往拿不到检索监督信号；不需要这种监督的模型能适用更广的任务。我们探索两个变体：标准的三分类（支持/反驳/信息不足）与 Thorne 和 Vlachos 研究的二分类（支持/反驳），两者都报告标签准确率。

---

## 4 结果 / Results

> Table 1: Open-Domain QA Test Scores. For TQA, left column uses the standard test set for Open-Domain QA, right column uses the TQA-Wiki test set. See Appendix D for further details.

**表 1（开放域 QA 测试分数）**：TQA 一列左边是开放域 QA 的标准测试集，右边是 TQA-Wiki 测试集；细节见附录 D。

> Table 2: Generation and classification Test Scores. MS-MARCO SotA is [4], FEVER-3 is [68] and FEVER-2 is [57] *Uses gold context/evidence. Best model without gold access underlined.

**表 2（生成与分类测试分数）**：MS-MARCO 的 SotA 取自文献 [4]，FEVER-3 取自 [68]，FEVER-2 取自 [57]；标 `*` 者使用了金标上下文/证据；在**不使用**金标访问的模型里，最优者以下划线标出。

### 4.1 开放域问答 / Open-domain Question Answering

> Table 2 shows results for RAG along with state-of-the-art models. On all four open-domain QA tasks, RAG sets a new state of the art (only on the T5-comparable split for TQA). RAG combines the generation flexibility of the "closed-book" (parametric only) approaches and the performance of "open-book" retrieval-based approaches. Unlike REALM and T5+SSM, RAG enjoys strong results without expensive, specialized "salient span masking" pre-training [20]. It is worth noting that RAG's retriever is initialized using DPR's retriever, which uses retrieval supervision on Natural Questions and TriviaQA. RAG compares favourably to the DPR QA system, which uses a BERT-based "cross-encoder" to re-rank documents, along with an extractive reader. RAG demonstrates that neither a re-ranker nor extractive reader is necessary for state-of-the-art performance.

表 2 给出 RAG 与当前最佳模型的对比。在四个开放域 QA 任务上，RAG 都刷新了当前最佳（TQA 仅在与 T5 可比的那个划分上）。RAG 兼得「闭卷」（纯参数）方法的**生成灵活性**与「开卷」（基于检索）方法的**性能**。与 REALM、T5+SSM 不同，RAG 无需代价高昂的专门预训练（「显著跨度掩码」salient span masking）就能取得强结果。需说明：RAG 的检索器是用 DPR 的检索器初始化的，而 DPR 在 NQ 与 TQA 上用过检索监督。RAG 相比 DPR 问答系统（用 BERT「交叉编码器」重排文档、再配抽取式阅读器）也不落下风——这说明要达到当前最佳，**重排器与抽取式阅读器都不是必需的**。

> There are several advantages to generating answers even when it is possible to extract them. Documents with clues about the answer but do not contain the answer verbatim can still contribute towards a correct answer being generated, which is not possible with standard extractive approaches, leading to more effective marginalization over documents. Furthermore, RAG can generate correct answers even when the correct answer is not in any retrieved document, achieving 11.8% accuracy in such cases for NQ, where an extractive model would score 0%.

即使答案可以被抽取出来，用生成的方式作答仍有若干好处：那些**含有答案线索但答案并未原样出现**的文档，也能为生成出正确答案作出贡献——这在标准抽取式方法里做不到，从而让「对文档做边缘化」更有效。更进一步，即使正确答案不在任何检索到的文档中，RAG 也能生成出正确答案：在 NQ 上这类情况准确率为 **11.8%**，而抽取式模型此时只能是 0%。

### 4.2 摘要式问答 / Abstractive Question Answering

> As shown in Table 2, RAG-Sequence outperforms BART on Open MS-MARCO NLG by 2.6 Bleu points and 2.6 Rouge-L points. RAG approaches state-of-the-art model performance, which is impressive given that (i) those models access gold passages with specific information required to generate the reference answer, (ii) many questions are unanswerable without the gold passages, and (iii) not all questions are answerable from Wikipedia alone. Table 3 shows some generated answers from our models. Qualitatively, we find that RAG models hallucinate less and generate factually correct text more often than BART. Later, we also show that RAG generations are more diverse than BART generations (see §4.5).

如表 2，在 Open MS-MARCO NLG 上 RAG-Sequence 比 BART 高 **2.6 个 BLEU 点、2.6 个 ROUGE-L 点**，接近当前最佳。考虑到以下三点，这一结果相当可观：(i) 那些最佳模型能访问**含生成参考答案所需具体信息的金标段落**；(ii) 许多问题若没有金标段落根本无法作答；(iii) 并非所有问题都能仅靠 Wikipedia 作答。表 3 给出部分生成答案。定性上看，RAG 比 BART **幻觉更少、生成文本事实正确的时候更多**；后文还会表明 RAG 的生成比 BART 更多样（见 §4.5）。

### 4.3 Jeopardy 问题生成 / Jeopardy Question Generation

> Table 2 shows that RAG-Token performs better than RAG-Sequence on Jeopardy question generation, with both models outperforming BART on Q-BLEU-1. 5 shows human evaluation results, over 452 pairs of generations from BART and RAG-Token. Evaluators indicated that BART was more factual than RAG in only 7.1% of cases, while RAG was more factual in 42.7% of cases, and both RAG and BART were factual in a further 17% of cases, clearly demonstrating the effectiveness of RAG on the task over a state-of-the-art generation model. Evaluators also find RAG generations to be more specific by a large margin. Table 3 shows typical generations from each model.

表 2 显示，在 Jeopardy 问题生成上 RAG-Token 优于 RAG-Sequence，两者在 Q-BLEU-1 上都超过 BART。表 5 给出人工评测结果，覆盖 BART 与 RAG-Token 的 452 组成对生成。评测者认为 BART 比 RAG 更符合事实的仅占 **7.1%**，认为 RAG 更符合事实的占 **42.7%**，另有 **17%** 认为两者都符合事实——清楚表明 RAG 在这项任务上优于当前最佳的生成模型。评测者还认为 RAG 的生成在具体性上大幅领先。表 3 给出两个模型各自的典型生成。

> Jeopardy questions often contain two separate pieces of information, and RAG-Token may perform best because it can generate responses that combine content from several documents. Figure 2 shows an example. When generating "Sun", the posterior is high for document 2 which mentions "The Sun Also Rises". Similarly, document 1 dominates the posterior when "A Farewell to Arms" is generated. Intriguingly, after the first token of each book is generated, the document posterior flattens. This observation suggests that the generator can complete the titles without depending on specific documents. In other words, the model's parametric knowledge is sufficient to complete the titles. We find evidence for this hypothesis by feeding the BART-only baseline with the partial decoding "The Sun…". BART completes the generation "'The Sun Also Rises' is a novel by this author of 'The Sun Also Rises'", indicating the title "The Sun Also Rises" is stored in BART's parameters. Similarly, BART will complete the partial decoding "'The Sun Also Rises' is a novel by this author of 'A…" with "'The Sun Also Rises' is a novel by this author of 'A Farewell to Arms'". This example shows how parametric and non-parametric memories work together—the non-parametric component helps to guide the generation, drawing out specific knowledge stored in the parametric memory.

Jeopardy 问题常包含两条彼此独立的信息，RAG-Token 表现最好，可能是因为它能生成把多个文档的内容组合起来的回答。图 2 给出一个例子：生成「Sun」时，提到《太阳照常升起》（The Sun Also Rises）的第 2 篇文档后验很高；生成《永别了，武器》（A Farewell to Arms）时，则是第 1 篇文档主导后验。有意思的是，每本书的**第一个 token** 生成之后，文档后验就变平了。这说明生成器**无需依赖特定文档**也能把书名补完——换言之，模型的**参数知识已足以完成书名**。为验证这一假设，我们给纯 BART 基线喂入不完整的解码前缀「The Sun…」，BART 补全为「'The Sun Also Rises' is a novel by this author of 'The Sun Also Rises'」，说明《太阳照常升起》这个书名就存在 BART 的参数里；同样，喂入「'The Sun Also Rises' is a novel by this author of 'A…」，BART 会补成「…of 'A Farewell to Arms'」。这个例子展示了参数记忆与非参数记忆如何协作——非参数部分**引导**生成方向，把存在参数记忆里的具体知识**拽出来**。

> Figure 2: RAG-Token document posterior $p(z_{i}|x,y_{i},y_{-i})$ for each generated token for input "Hemingway" for Jeopardy generation with 5 retrieved documents. …

**图 2**：输入「Hemingway」、检索 5 篇文档做 Jeopardy 生成时，RAG-Token 在每个生成 token 上的文档后验 $p(z_{i}|x,y_{i},y_{-i})$。生成「A Farewell to Arms」时第 1 篇文档后验高，生成「The Sun Also Rises」时第 2 篇文档后验高。

> Table 3: Examples from generation tasks. RAG models generate more specific and factually accurate responses. '?' indicates factually incorrect responses, * indicates partially correct responses.
> Table 4: Human assessments for the Jeopardy Question Generation Task.
> Table 5: Ratio of distinct to total tri-grams for generation tasks.

**表 3**：生成任务样例。RAG 生成更具体、更符合事实的回答；`?` 标事实错误，`*` 标部分正确。
**表 4**：Jeopardy 问题生成任务的人工评估结果。
**表 5**：生成任务中「去重三元组数 / 总三元组数」的比值（衡量多样性）。

### 4.4 事实核查 / Fact Verification

> Table 2 shows our results on FEVER. For 3-way classification, RAG scores are within 4.3% of state-of-the-art models, which are complex pipeline systems with domain-specific architectures and substantial engineering, trained using intermediate retrieval supervision, which RAG does not require. For 2-way classification, we compare against Thorne and Vlachos [57], who train RoBERTa [35] to classify the claim as true or false given the gold evidence sentence. RAG achieves an accuracy within 2.7% of this model, despite being supplied with only the claim and retrieving its own evidence. We also analyze whether documents retrieved by RAG correspond to documents annotated as gold evidence in FEVER. We calculate the overlap in article titles between the top $k$ documents retrieved by RAG and gold evidence annotations. We find that the top retrieved document is from a gold article in 71% of cases, and a gold article is present in the top 10 retrieved articles in 90% of cases.

表 2 给出 FEVER 上的结果。三分类时，RAG 与当前最佳模型相差在 **4.3%** 以内；而那些最佳模型是带领域专用架构、工程量巨大的复杂流水线，且训练时用了中间检索监督，RAG 并不需要。二分类时，我们与 Thorne 和 Vlachos 对比：他们用 RoBERTa 在给定金标证据句的情况下判定论断真/假；RAG 只拿到论断、自己检索证据，准确率与之相差在 **2.7%** 以内。我们还分析了 RAG 检索到的文档是否对应 FEVER 标注的金标证据：统计 RAG top-$k$ 文档与金标证据在文章标题上的重合——**71%** 的情况下排第一的文档来自金标文章，**90%** 的情况下 top-10 里含金标文章。

### 4.5 补充结果 / Additional Results

#### 生成多样性 / Generation Diversity

> Section 4.3 shows that RAG models are more factual and specific than BART for Jeopardy question generation. Following recent work on diversity-promoting decoding [33, 59, 39], we also investigate generation diversity by calculating the ratio of distinct ngrams to total ngrams generated by different models. Table 5 shows that RAG-Sequence's generations are more diverse than RAG-Token's, and both are significantly more diverse than BART without needing any diversity-promoting decoding.

§4.3 表明 RAG 在 Jeopardy 问题生成上比 BART 更符合事实、更具体。仿照近期关于多样性促进解码的工作，我们还用「去重 n-gram 数 / 总 n-gram 数」考察生成多样性。表 5 显示 RAG-Sequence 比 RAG-Token 更多样，而两者都明显比 BART 更多样——且**无需任何促进多样性的解码技巧**。

> Table 6: Ablations on the dev set. As FEVER is a classification task, both RAG models are equivalent.

**表 6（dev 集上的消融）**：由于 FEVER 是分类任务，两种 RAG 模型在此等价。

#### 检索消融 / Retrieval Ablations

> A key feature of RAG is learning to retrieve relevant information for the task. To assess the effectiveness of the retrieval mechanism, we run ablations where we freeze the retriever during training. As shown in Table 6, learned retrieval improves results for all tasks.

RAG 的一个关键特性是**为任务学习检索相关信息**。为评估检索机制的作用，我们做了「训练时冻结检索器」的消融：如表 6，可学习的检索在**所有任务**上都带来提升。

> We compare RAG's dense retriever to a word overlap-based BM25 retriever [53]. Here, we replace RAG's retriever with a fixed BM25 system, and use BM25 retrieval scores as logits when calculating $p(z|x)$. Table 6 shows the results. For FEVER, BM25 performs best, perhaps since FEVER claims are heavily entity-centric and thus well-suited for word overlap-based retrieval. Differentiable retrieval improves results on all other tasks, especially for Open-Domain QA, where it is crucial.

我们还将 RAG 的稠密检索器与基于词重叠的 **BM25** 检索器对比：把检索器换成固定的 BM25 系统，并用 BM25 分数作为 logits 计算 $p(z|x)$。结果见表 6：在 FEVER 上 BM25 表现最好，大概因为 FEVER 的论断高度以实体为中心，特别适合词重叠式检索；**可微检索**在所有其它任务上都有提升，在开放域问答上尤为关键。

**📌 伏笔（D04 BM25）**：BM25 并非「弱基线」——在实体密集的判别式任务上它可能反超稠密检索；RAGFlow 用 `MatchTextExpr` + `FusionExpr` 做加权融合，正是对「两类检索各有胜场」的工程回应。

#### 索引热替换 / Index hot-swapping

> An advantage of non-parametric memory models like RAG is that knowledge can be easily updated at test time. Parametric-only models like T5 or BART need further training to update their behavior as the world changes. To demonstrate, we build an index using the DrQA [5] Wikipedia dump from December 2016 and compare outputs from RAG using this index to the newer index from our main results (December 2018). We prepare a list of 82 world leaders who had changed between these dates and use a template "Who is {position}?" (e.g. "Who is the President of Peru?") to query our NQ RAG model with each index. RAG answers 70% correctly using the 2016 index for 2016 world leaders and 68% using the 2018 index for 2018 world leaders. Accuracy with mismatched indices is low (12% with the 2018 index and 2016 leaders, 4% with the 2016 index and 2018 leaders). This shows we can update RAG's world knowledge by simply replacing its non-parametric memory.

像 RAG 这样带非参数记忆的模型，其优势在于**知识可在测试时轻松更新**；而 T5、BART 这类纯参数模型，要随世界变化更新行为就得继续训练。为演示这一点，我们用 DrQA 提供的 **2016 年 12 月** Wikipedia dump 另建一份索引，把用它得到的结果与主实验中较新的索引（2018 年 12 月）对比。我们准备了一份在这两个时点之间**发生更替的 82 位世界领导人**名单，用模板「Who is {position}?」（如「Who is the President of Peru?」）分别以两份索引查询 NQ RAG 模型。结果：用 2016 索引答 2016 年的领导人，正确率 **70%**；用 2018 索引答 2018 年的领导人，正确率 **68%**。索引与年份错配时准确率很低（2018 索引配 2016 名单 12%，2016 索引配 2018 名单 4%）。这说明**只要替换非参数记忆，就能更新 RAG 的世界知识**。

#### 多检索文档的影响 / Effect of Retrieving more documents

> Models are trained with either 5 or 10 retrieved latent documents, and we do not observe significant differences in performance between them. We have the flexibility to adjust the number of retrieved documents at test time, which can affect performance and runtime. Figure 3 (left) shows that retrieving more documents at test time monotonically improves Open-domain QA results for RAG-Sequence, but performance peaks for RAG-Token at 10 retrieved documents. Figure 3 (right) shows that retrieving more documents leads to higher Rouge-L for RAG-Token at the expense of Bleu-1, but the effect is less pronounced for RAG-Sequence.

模型训练时使用 5 篇或 10 篇检索到的潜在文档，两者性能未见显著差异。测试时我们可以灵活调整检索文档数，它会影响性能与耗时。图 3（左）显示：测试时检索更多文档会**单调提升** RAG-Sequence 的开放域 QA 结果；而 RAG-Token 在检索 10 篇时性能达到峰值。图 3（右）显示：检索更多文档会让 RAG-Token 的 ROUGE-L 升高，但 BLEU-1 下降；RAG-Sequence 上这一效应没那么明显。

> Figure 3: Left: NQ performance as more documents are retrieved. Center: Retrieval recall performance in NQ. Right: MS-MARCO Bleu-1 and Rouge-L as more documents are retrieved.

**图 3**：左——NQ 上随检索文档数增加的性能；中——NQ 上的检索召回；右——MS-MARCO 的 BLEU-1 与 ROUGE-L 随检索文档数变化的曲线。
---

## 5 相关工作 / Related Work

### 单任务检索 / Single-Task Retrieval

> Prior work has shown that retrieval improves performance across a variety of NLP tasks when considered in isolation. Such tasks include open-domain question answering [5, 29], fact checking [56], fact completion [48], long-form question answering [12], Wikipedia article generation [36], dialogue [41, 65, 9, 13], translation [17], and language modeling [19, 27]. Our work unifies previous successes in incorporating retrieval into individual tasks, showing that a single retrieval-based architecture is capable of achieving strong performance across several tasks.

以往工作已表明，单独看时，检索能提升各类 NLP 任务的表现，包括开放域问答、事实核查、事实补全、长文本问答、Wikipedia 文章生成、对话、翻译与语言建模。我们的工作把这些「把检索塞进单个任务」的成功经验统一了起来，表明**同一个基于检索的架构**就能在多个任务上取得强性能。

### 面向 NLP 的通用架构 / General-Purpose Architectures for NLP

> Prior work on general-purpose architectures for NLP tasks has shown great success without the use of retrieval. A single, pre-trained language model has been shown to achieve strong performance on various classification tasks in the GLUE benchmarks [60, 61] after fine-tuning [49, 8]. GPT-2 [50] later showed that a single, left-to-right, pre-trained language model could achieve strong performance across both discriminative and generative tasks. For further improvement, BART [32] and T5 [51, 52] propose a single, pre-trained encoder-decoder model that leverages bi-directional attention to achieve stronger performance on discriminative and generative tasks. Our work aims to expand the space of possible tasks with a single, unified architecture, by learning a retrieval module to augment pre-trained, generative language models.

此前关于 NLP 通用架构的工作，在没有用到检索的情况下也取得了巨大成功：单一预训练语言模型微调后在 GLUE 基准的多种分类任务上表现强劲；GPT-2 进一步表明单一从左到右的预训练语言模型在判别式与生成式任务上都能做得好；BART 与 T5 则提出单一的预训练编码器-解码器模型，借助双向注意力在判别式与生成式任务上取得更好表现。我们的目标是：**通过学习一个检索模块来增强预训练的生成式语言模型**，用单一统一架构拓展可处理任务的空间。

### 可学习的检索 / Learned Retrieval

> There is significant work on learning to retrieve documents in information retrieval, more recently with pre-trained, neural language models [44, 26] similar to ours. Some work optimizes the retrieval module to aid in a specific, downstream task such as question answering, using search [46], reinforcement learning [6, 63, 62], or a latent variable approach [31, 20] as in our work. These successes leverage different retrieval-based architectures and optimization techniques to achieve strong performance on a single task, while we show that a single retrieval-based architecture can be fine-tuned for strong performance on a variety of tasks.

信息检索领域已有大量关于「学习检索文档」的工作，较近的用到了与我们类似的预训练神经语言模型。有些工作优化检索模块以辅助某个具体下游任务（如问答），手段包括搜索、强化学习，或像我们这样用**潜在变量**方法。这些成功各自借助不同的检索架构与优化技巧，在**单一**任务上取得强性能；而我们表明，**同一个**检索架构经微调即可在多种任务上取得强性能。

### 基于记忆的架构 / Memory-based Architectures

> Our document index can be seen as a large external memory for neural networks to attend to, analogous to memory networks [64, 55]. Concurrent work [14] learns to retrieve a trained embedding for each entity in the input, rather than to retrieve raw text as in our work. Other work improves the ability of dialog models to generate factual text by attending over fact embeddings [15, 13]. A key feature of our memory is that it is comprised of raw text rather distributed representations, which makes the memory both (i) human-readable, lending a form of interpretability to our model, and (ii) human-writable, enabling us to dynamically update the model's memory by editing the document index. This approach has also been used in knowledge-intensive dialog, where generators have been conditioned on retrieved text directly, albeit obtained via TF-IDF rather than end-to-end learnt retrieval [9].

我们的文档索引可以看作供神经网络做注意力（attend）的大型外部记忆，类似记忆网络。并行的工作学习为输入中的每个实体检索一个训练好的 embedding，而不是像我们这样检索原始文本；也有工作通过对事实 embedding 做注意力来提升对话模型生成事实性文本的能力。我们的记忆有一个关键特点：它由**原始文本**而非分布式表示构成——这使记忆 (i) **人可读**，为模型带来一种可解释性；(ii) **人可写**，可以靠编辑文档索引来动态更新模型记忆。这一思路也被用于知识密集型对话：生成器直接以检索到的文本为条件，只不过那里的文本由 TF-IDF 取得，而非端到端学习的检索。

### 检索-编辑方法 / Retrieve-and-Edit approaches

> Our method shares some similarities with retrieve-and-edit style approaches, where a similar training input-output pair is retrieved for a given input, and then edited to provide a final output. These approaches have proved successful in a number of domains including Machine Translation [18, 22] and Semantic Parsing [21]. Our approach does have several differences, including less of emphasis on lightly editing a retrieved item, but on aggregating content from several pieces of retrieved content, as well as learning latent retrieval, and retrieving evidence documents rather than related training pairs. This said, RAG techniques may work well in these settings, and could represent promising future work.

我们的方法与「检索-编辑」（retrieve-and-edit）类思路有相似之处：针对给定输入检索一个相似的训练输入-输出对，再编辑它得到最终输出。这类方法已在机器翻译与语义解析等领域被证明有效。我们的方法有几处不同：并不强调对检索到的条目做**轻度编辑**，而是**聚合多份检索内容**的信息；做的是**潜在检索**；检索的是**证据文档**而非相关训练对。话虽如此，RAG 技术也可能在这些场景下表现良好，是可期的后续工作。

---

## 6 讨论 / Discussion

> In this work, we presented hybrid generation models with access to parametric and non-parametric memory. We showed that our RAG models obtain state of the art results on open-domain QA. We found that people prefer RAG's generation over purely parametric BART, finding RAG more factual and specific. We conducted an thorough investigation of the learned retrieval component, validating its effectiveness, and we illustrated how the retrieval index can be hot-swapped to update the model without requiring any retraining. In future work, it may be fruitful to investigate if the two components can be jointly pre-trained from scratch, either with a denoising objective similar to BART or some another objective. Our work opens up new research directions on how parametric and non-parametric memories interact and how to most effectively combine them, showing promise in being applied to a wide variety of NLP tasks.

本文提出了可访问参数记忆与非参数记忆的混合生成模型，表明 RAG 在开放域问答上取得当前最佳；人们比起纯参数的 BART 更偏好 RAG 的生成，认为它更符合事实、更具体。我们对可学习检索组件做了彻底考察，验证了其有效性，并演示了检索索引可以**热替换**，从而无需任何再训练就更新模型知识。后续工作可以研究两个组件能否从零开始联合预训练（用类似 BART 的去噪目标或其它目标）。我们的工作开启了关于「参数记忆与非参数记忆如何交互、如何最有效地结合」的新研究方向，并显示出在广泛 NLP 任务上的应用前景。

**📌 译注｜作者自陈的局限**（散落在 §4.2/§4.4 与本节，值得单独拎出来）：

1. 只用**单一** Wikipedia dump、单一跳（single-hop）知识源，答案无法跨多文档聚合；

2. 检索是**弱监督**学出来的，缺少引用/出处（citation）能力——生成的答案指不回具体文档；

3. 生成侧把检索内容直接拼进上下文，长文档与多文档场景的上下文预算问题没有处理。

## 更广泛的影响 / Broader Impact

> This work offers several positive societal benefits over previous work: the fact that it is more strongly grounded in real factual knowledge (in this case Wikipedia) makes it "hallucinate" less with generations that are more factual, and offers more control and interpretability. RAG could be employed in a wide variety of scenarios with direct benefit to society, for example by endowing it with a medical index and asking it open-domain questions on that topic, or by helping people be more effective at their jobs.

相比以往工作，本文有几项正面的社会效益：更牢固地扎根于真实事实知识（此处为 Wikipedia），使模型「幻觉」更少、生成更符合事实，并提供更多控制与可解释性。RAG 可用于多种直接造福社会的场景，例如给它配一份**医学索引**并就该主题做开放域问答，或帮助人们提升工作效率。

> With these advantages also come potential downsides: Wikipedia, or any potential external knowledge source, will probably never be entirely factual and completely devoid of bias. Since RAG can be employed as a language model, similar concerns as for GPT-2 [50] are valid here, although arguably to a lesser extent, including that it might be used to generate abuse, faked or misleading content in the news or on social media; to impersonate others; or to automate the production of spam/phishing content [54]. Advanced language models may also lead to the automation of various jobs in the coming decades [16]. In order to mitigate these risks, AI systems could be employed to fight against misleading content and automated spam/phishing.

优势也伴随潜在风险：Wikipedia 或任何外部知识源，大概永远不会百分百符合事实、完全无偏。由于 RAG 可被当作语言模型使用，针对 GPT-2 的担忧在此同样成立（尽管程度可能更轻），包括被用来生成辱骂性内容、在新闻或社交媒体上制造虚假或误导性内容、冒充他人、或自动化生产垃圾/钓鱼内容。先进语言模型还可能在未来几十年自动化各种工作。为缓解这些风险，可以用 AI 系统去对抗误导性内容与自动化垃圾/钓鱼。

## 致谢 / Acknowledgments

> The authors would like to thank the reviewers for their thoughtful and constructive feedback … EP thanks supports from the NSF Graduate Research Fellowship. PL is supported by the FAIR PhD program.

作者感谢审稿人富有洞见与建设性的意见，感谢 HuggingFace 在开源 RAG 代码上的帮助，感谢 Kyunghyun Cho 与 Sewon Min 的有益讨论与建议。EP 受 NSF 研究生研究奖学金支持，PL 受 FAIR 博士项目支持。
