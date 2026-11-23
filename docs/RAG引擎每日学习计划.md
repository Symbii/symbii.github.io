---
title: "RAG 引擎每日学习计划（8 周 · 56 天）"
---
# RAG 引擎每日学习计划（8 周 · 56 天）

> 配套文档：[RAG 引擎学习地图](RAG引擎学习地图.md) · [RAGFlow 源码学习地图](RAGFlow源码学习地图.md)（每天 15–25 分钟源码对照，逐日锚点见该文档第 4 节） · 项目与学习计划对照（自家 解析服务A / 检索服务B 逐环落点） · 学习笔记归档
> 节奏：每周 6 个学习日 + 1 个复盘日（周日）。学习日 1.5–2h，复盘日 2–2.5h。
> 每天固定三段：**读 25min → 动手 50min → 记录 15min**。记录写进 `learning-log.md`，一天一条，不超过 10 行。
> 链接说明：文中链接均可直接点击；arXiv 点进去可切 HTML/PDF；文档站改版后个别锚点可能失效，404 时在站内搜页面标题即可。

---

## 一、开始前：环境与工具（半天，可在 Day 1 顺带完成）

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install sentence-transformers faiss-cpu rank_bm25 jieba pymupdf pdfplumber \
            python-docx python-pptx openpyxl trafilatura pandas numpy jupyter
```

- 模型：[bge-small-zh-v1.5](https://huggingface.co/BAAI/bge-small-zh-v1.5)（embedding，小、快、中文好）、[bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3)（重排，第 5 周用）。
- 向量库：先用 [FAISS](https://github.com/facebookresearch/faiss) 跑通，第 3 周再上 [Qdrant](https://qdrant.tech/documentation/quickstart/)（Docker 一条命令）或 [Milvus](https://milvus.io/docs)。
- 追踪：一个 `experiments.md` 表格（日期 / 假设 / 配置 / 指标 / 结论），所有 A/B 都记在这里。
- 术语表：`glossary.md`，每个新术语写一句自己的解释 + 一个反例。

> 材料以英文为主。读不懂的段落用 LLM 逐段对照翻译，但**术语保留英文原文**，否则后面看文档会对不上。

---

## 二、学习材料总表（全部可点击）

### 论文（12 篇）

| 编号 | 论文 | 直达链接 | 用途 |
|---|---|---|---|
| P1 | Lewis et al., *RAG* (2020) | https://arxiv.org/abs/2005.11401 | Day 1、36 |
| P2 | Reimers & Gurevych, *Sentence-BERT* (2019) | https://arxiv.org/abs/1908.10084 | Day 2 |
| P3 | Malkov & Yashunin, *HNSW* (2016) | https://arxiv.org/abs/1603.09320 | Day 3 |
| P4 | Karpukhin et al., *DPR* (2020) | https://arxiv.org/abs/2004.04906 | Day 22 |
| P5 | Thakur et al., *BEIR* (2021) | https://arxiv.org/abs/2104.08663 | Day 22 |
| P6 | Khattab & Zaharia, *ColBERT* (2020) | https://arxiv.org/abs/2004.12832 | Day 24 |
| P7 | Gao et al., *HyDE* (2022) | https://arxiv.org/abs/2212.10496 | Day 25 |
| P8 | Liu et al., *Lost in the Middle* (2023) | https://arxiv.org/abs/2307.03172 | Day 32 |
| P9 | Asai et al., *Self-RAG* (2023) | https://arxiv.org/abs/2310.11511 | Day 50 |
| P10 | Yan et al., *CRAG* (2024) | https://arxiv.org/abs/2401.15884 | Day 50 |
| P11 | Edge et al., *GraphRAG* (2024) | https://arxiv.org/abs/2404.16130 | Day 52 |
| P12 | Es et al., *RAGAS* (2023) | https://arxiv.org/abs/2309.15217 | Day 39 |

### 官方文档（按天引用）

| 工具 | 直达链接 | 用在哪天 |
|---|---|---|
| PyMuPDF 文本页 | https://pymupdf.readthedocs.io/en/latest/textpage.html | Day 8 |
| PyMuPDF 文本配方 | https://pymupdf.readthedocs.io/en/latest/recipes-text.html | Day 9 |
| pdfplumber（含可视化调试） | https://github.com/jsvine/pdfplumber#visual-debugging | Day 9 |
| Camelot 原理（lattice/stream） | https://camelot-py.readthedocs.io/en/stable/user/how-it-works.html | Day 10 |
| PaddleOCR | https://github.com/PaddlePaddle/PaddleOCR | Day 11 |
| trafilatura | https://github.com/adbar/trafilatura | Day 12 |
| Qdrant 过滤 | https://qdrant.tech/documentation/concepts/filtering/ | Day 18、31、44 |
| Qdrant 混合查询 | https://qdrant.tech/documentation/concepts/hybrid-queries/ | Day 23 |
| Qdrant 多租户 | https://qdrant.tech/documentation/guides/multiple-partitions/ | Day 45 |
| Milvus 索引 | https://milvus.io/docs/index-vector-fields.md | Day 19 |
| Milvus 过滤 | https://milvus.io/docs/boolean.md | Day 18、31 |
| Milvus 多租户 | https://milvus.io/docs/multi_tenancy.md | Day 43、45 |
| Elasticsearch RRF | https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion | Day 23 |
| RAGAS 指标 | https://docs.ragas.io/en/stable/concepts/metrics/ | Day 14、39 |
| Langfuse 追踪 | https://langfuse.com/docs/observability/get-started | Day 41 |
| LlamaIndex 节点解析 | https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/ | Day 15、16、17 |
| Anthropic 语境增强 | https://www.anthropic.com/news/contextual-retrieval | Day 16、32 |
| Keycloak 授权模型 | https://www.keycloak.org/docs/latest/authorization_services/ | Day 43 |
| OpenAI 工具调用 | https://platform.openai.com/docs/guides/function-calling | Day 51 |
| sentence-transformers | https://www.sbert.net/ | Day 2、29 |

### 源码（读目录，不通读）

| 项目 | 直达链接 | 看什么 |
|---|---|---|
| RAGFlow | https://github.com/infiniflow/ragflow | `deepdoc/parser/` 解析链路 |
| Dify | https://github.com/langgenius/dify | `api/core/rag/` 切分、索引、检索 |
| FastGPT | https://github.com/labring/FastGPT | 知识库产品化封装 |
| GraphRAG | https://github.com/microsoft/graphrag | 索引管线与查询 |
| rank_bm25 | https://github.com/dorianbrown/rank_bm25 | `BM25Okapi` 全部源码（<100 行） |
| LlamaIndex 语义切分 | https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/node_parser/text/semantic_splitter.py | 断点判定实现 |

### 可选课程

- [DeepLearning.AI 短课程列表](https://www.deeplearning.ai/short-courses/)：找《Building and Evaluating Advanced RAG Applications》（对应第 6 周）与《Advanced Retrieval for AI with Chroma》（对应第 4–5 周）。

---

## 三、第 1 周：基础底座 + 跑通朴素 RAG

### Day 1 · 周一 · 1.5h ｜ RAG 到底在解决什么问题
- **任务**：画出一张完整的 RAG 链路图，并跑通第一次 embedding 相似度计算。
- **知识点**：参数化知识 vs 非参数化知识；retriever–generator 两段式结构；索引期与查询期的分工；RAG 相对微调的成本优势与失效场景。
- **材料**：[RAG 论文 §1 与 §2.1–2.3](https://arxiv.org/abs/2005.11401)（跳过训练细节）；[bge-small-zh-v1.5 模型卡](https://huggingface.co/BAAI/bge-small-zh-v1.5)（看相似度用法与 instruction 前缀）。
- **方法**：费曼法——合上论文，用 5 句话复述"文档如何变成答案"，卡住的地方标红再回读；先画图再写代码。
- **验收**：图上有 8 个环节且能说出每环可能丢什么信息；embedding demo 能对 10 个句子两两算相似度。

### Day 2 · 周二 · 1.5h ｜ Embedding 与相似度
- **任务**：用 numpy 手写 cosine top-k，并用它检索 1000 条文本。
- **知识点**：双塔结构、对比学习目标、向量归一化、cosine / 内积 / L2 的等价条件、维度与语义分辨率、中文 tokenizer 的影响。
- **材料**：[Sentence-BERT §2 结构、§3 训练目标](https://arxiv.org/abs/1908.10084)；[bge 模型卡的相似度示例](https://huggingface.co/BAAI/bge-small-zh-v1.5)。
- **方法**：控制变量实验——同一批向量做归一化与不归一化各检索一次，记录 Top-5 差异，用差异反推公式。
- **验收**：能解释"为什么归一化后内积等于余弦"；手写实现与库结果 Top-10 重合 ≥ 9。

### Day 3 · 周三 · 1.5h ｜ 向量索引：HNSW
- **任务**：用 FAISS 建 HNSW 索引，测 `efSearch` 对召回率与延迟的影响。
- **知识点**：暴力检索的复杂度、ANN 的召回-延迟权衡；HNSW 的分层图、M / efConstruction / efSearch 三个参数；IVF 与 PQ 的取舍。
- **材料**：[HNSW 论文 §2 插入与搜索、§4 实验](https://arxiv.org/abs/1603.09320)；[FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)（找 `IndexHNSWFlat` 与参数说明）。
- **方法**：参数扫描——`efSearch ∈ {16, 32, 64, 128, 256}`，每组跑 100 次查询取 P50/P95 延迟，画召回-延迟曲线。
- **验收**：能说出"efSearch 调大，召回升、延迟升，但内存不变"；曲线拐点能解释。

### Day 4 · 周四 · 1.5h ｜ 关键词检索与 BM25
- **任务**：手写 BM25 打分函数，并与 `rank_bm25` 结果对齐。
- **知识点**：TF、IDF、文档长度归一化；k1 与 b 的物理含义；中文分词（jieba）对召回的影响；BM25 在专有名词、型号、错误码上的优势。
- **材料**：[rank_bm25 源码](https://github.com/dorianbrown/rank_bm25)（`BM25Okapi` 不到 100 行）；[jieba](https://github.com/fxsjy/jieba) 的分词模式说明。
- **方法**：源码跟读——逐行注释源码，再自己默写一遍；用同一 query 对比分词前后结果。
- **验收**：自写分数与库分数误差 < 1e-6；能举 3 个"向量检索失败但 BM25 命中"的例子。

### Day 5 · 周五 · 2h ｜ 手写 naive RAG（里程碑）
- **任务**：100 行以内实现"解析 → 切分 → 索引 → 检索 → 带引用生成"。
- **知识点**：chunk size 与 overlap 的直觉；Top-k 选择；prompt 中上下文与指令的排布；引用编号从哪来。
- **材料**：[RAG 论文 §2](https://arxiv.org/abs/2005.11401)（带着实现重读）；[LlamaIndex 从零构建 RAG](https://docs.llamaindex.ai/en/stable/understanding/rag/)（对照流程，不必照抄）。
- **方法**：先跑通再优化——允许粗糙，但**必须端到端**；代码控制在单文件，函数不超过 10 个。
- **验收**：对 20 个问题能给出带来源页码的答案；任一答案能点回原文段落。

### Day 6 · 周六 · 2h ｜ 第一次误差分析
- **任务**：对 30 条 query 做人工归因，产出错误分类表。
- **知识点**：错误分型（解析错 / 切分错 / 没召回 / 召回但排序差 / 生成不忠实 / 本就无答案）；"归因先于调参"。
- **材料**：自己 Day 5 的日志；[Lost in the Middle 摘要](https://arxiv.org/abs/2307.03172)（先建立"中间内容容易被忽略"的预感）。
- **方法**：每条错误只允许归到一个主因，写"证据"（原文在哪、召回了什么）；不允许写"效果不好"这类结论。
- **验收**：30 条全部有主因；能算出各类型占比，并指出最大的一类。

### Day 7 · 周日 · 2h ｜ 周复盘
- **任务**：写一页 AAR（预期 / 实际 / 差距 / 下周假设），补齐欠账。
- **方法**：先写"我原本以为…"，再写"实际是…"，最后写"下周只改一个变量"。
- **验收**：下周要验证的**单个**假设写清楚（例如"解析错误占错误总数 > 30%"）。

---

## 四、第 2 周：解析攻坚 + 评测起步

### Day 8 · 周一 · 1.5h ｜ PDF 的文本层与结构
- **任务**：用 PyMuPDF 提取 block/line/span，打印每块的坐标与字号。
- **知识点**：PDF 没有"段落"，只有绘制指令；文本层 vs 扫描件；字号/加粗是标题的弱信号；`get_text("dict")` 的层级。
- **材料**：[PyMuPDF TextPage 文档](https://pymupdf.readthedocs.io/en/latest/textpage.html)；[PyMuPDF 文本提取配方](https://pymupdf.readthedocs.io/en/latest/recipes-text.html)。
- **方法**：可视化——把 bbox 画回页面截图，用眼睛校验结构假设。
- **验收**：能对一份论文自动标出标题层级（至少 H1/H2 两级）。

### Day 9 · 周二 · 1.5h ｜ 双栏、阅读顺序与页眉页脚
- **任务**：让双栏 PDF 按"左栏读完再右栏"输出，并剔除页眉页脚。
- **知识点**：x 方向投影做栏检测；按 (栏, y) 排序；页面上下 5% 区域内的高频重复行判定为页眉页脚；跨栏图表打断阅读流。
- **材料**：[pdfplumber 文本提取与可视化调试](https://github.com/jsvine/pdfplumber#visual-debugging)；[PyMuPDF 文本配方](https://pymupdf.readthedocs.io/en/latest/recipes-text.html)（看 `blocks` 排序示例）。
- **方法**：先目测再编码——对 5 份双栏论文各截一张"块顺序"图，肉眼确认后再写规则。
- **验收**：5 份中 ≥ 4 份顺序正确；能说出两种误判情形（如通栏标题、脚注）。

### Day 10 · 周三 · 1.5h ｜ 表格抽取
- **任务**：把 10 份含表格的 PDF 转成 Markdown 表格。
- **知识点**：有线表（lattice）与无线表（stream）的差异；合并单元格；跨页表；表格转 Markdown 时表头保留的重要性。
- **材料**：[Camelot 原理文档](https://camelot-py.readthedocs.io/en/stable/user/how-it-works.html)；[PaddleOCR 的表格识别（PP-Structure）](https://github.com/PaddlePaddle/PaddleOCR)。
- **方法**：双工具对照——Camelot 与 PP-Structure 各跑一遍，人工比对，记录各自失败类型。
- **验收**：10 份中 ≥ 7 份结构正确；错误能归类到"无线表/合并单元格/跨页"。

### Day 11 · 周四 · 1.5h ｜ 扫描件 OCR
- **任务**：对 5 份扫描 PDF 完成 OCR，输出带置信度的文本。
- **知识点**：det / rec / cls 三阶段；图像预处理（灰度、二值化、去噪、纠偏）；置信度阈值与人工复核队列；OCR 错误对检索的连锁影响。
- **材料**：[PaddleOCR 快速开始](https://github.com/PaddlePaddle/PaddleOCR)（README 的 Quick Start 与 det/rec 说明）。
- **方法**：流水线拆解——先只跑 det 看框，再加 rec，最后加 cls，逐段确认问题出在哪。
- **验收**：5 份平均字符准确率 ≥ 95%（人工抽 100 字）；低置信度片段被单独标记。

### Day 12 · 周五 · 1.5h ｜ 其它格式与清洗
- **任务**：写一个统一入口，支持 docx / pptx / xlsx / html / md / 代码文件。
- **知识点**：docx 的段落与表格分离；pptx 的备注页；xlsx 的多 sheet；HTML 正文抽取；编码与乱码；SimHash 去重；水印与重复页眉。
- **材料**：[trafilatura](https://github.com/adbar/trafilatura)（网页正文抽取示例）；[python-docx](https://python-docx.readthedocs.io/en/latest/)、[python-pptx](https://python-pptx.readthedocs.io/en/latest/)、[openpyxl](https://openpyxl.readthedocs.io/en/stable/) 的快速入门页。
- **方法**：以终为始——先定义统一的 `Document` 结构（doc_id, page, type, text, bbox, meta），再让每个解析器往里填。
- **验收**：6 种格式都能产出同一结构；重复文档能被 SimHash 查出。

### Day 13 · 周六 · 2h ｜ 解析 pipeline 整合与失败率统计
- **任务**：跑通 50 份真实文档，产出解析质量报告。
- **知识点**：失败率按文档类型分层统计；抽检方法（分层抽样）；"解析失败"的可观测信号（空文本、字符数异常、乱码率）。
- **材料**：自己前 5 天的代码；[RAGFlow 解析模块](https://github.com/infiniflow/ragflow/tree/main/deepdoc/parser)（对照工业实现的分层设计）。
- **方法**：埋点——每个解析器记录耗时、字符数、异常类型；报告只呈现"哪类文档失败率最高"。
- **验收**：报告含每类文档的失败率与 Top-3 失败原因；抽检 20 份，人工判定与自动判定一致率 ≥ 80%。

### Day 14 · 周日 · 2.5h ｜ 建 30 题评测集（里程碑）
- **任务**：产出第一版评测集：问题、标准答案、金标片段、难度。
- **知识点**：评测集来源（真实提问、文档标题改写、跨文档问题）；金标片段的最小粒度；难度分层；"无答案题"必须占一定比例。
- **材料**：[RAGAS 指标文档](https://docs.ragas.io/en/stable/concepts/metrics/)（先知道要测什么，再决定标什么）。
- **方法**：三人独立标注再对齐（没有第三人就隔天自标一遍），分歧处讨论定规则并写进 `eval-rules.md`。
- **验收**：30 题中 ≥ 5 题为无答案题；每题都有金标片段；标注规则文档成文。

---

## 五、第 3 周：切分与索引

### Day 15 · 周一 · 1.5h ｜ 切分策略全景
- **任务**：实现固定窗口与递归切分，对比块边界。
- **知识点**：固定窗口的截断问题；递归切分按分隔符优先级（段落 → 句号 → 逗号）；中文标点与英文的差异；overlap 的作用与代价。
- **材料**：[LlamaIndex 节点解析文档](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/)；[Dify 切分实现](https://github.com/langgenius/dify/tree/main/api/core/rag)（读函数签名即可）。
- **方法**：打印边界——把每块的"首 20 字 + 尾 20 字"打出来，用眼睛判断是否切断了语义。
- **验收**：能说出递归切分在什么文档上仍会切断表格；两种策略的块长分布画成直方图。

### Day 16 · 周二 · 1.5h ｜ 语义切分
- **任务**：用相邻句 embedding 相似度做断点，实现语义切分。
- **知识点**：断点阈值；滑动窗口平滑；计算成本（每句一次 embedding）；语义切分在长文档上的收益与噪声。
- **材料**：[LlamaIndex 语义切分源码](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/node_parser/text/semantic_splitter.py)；[Anthropic 语境增强检索](https://www.anthropic.com/news/contextual-retrieval)（看它为什么给块加语境）。
- **方法**：阈值扫描——0.5 / 0.6 / 0.7 各跑一遍，观察块数与块长，选"块数合理且边界可读"的档。
- **验收**：能给出阈值-块数曲线；随机抽 10 块，8 块以上是完整语义单元。

### Day 17 · 周三 · 1.5h ｜ 结构化切分与父子块
- **任务**：按标题层级建树，检索叶子块、返回父块。
- **知识点**：文档树（章-节-段）；小块检索、大块生成（small-to-big）；父块 token 上限；表格与列表作为原子块不切分。
- **材料**：[LlamaIndex 层级解析与自动合并](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/)（找 HierarchicalNodeParser / AutoMergingRetriever）；[RAGFlow 结构化输出](https://github.com/infiniflow/ragflow/tree/main/deepdoc/parser)。
- **方法**：反推设计——先问"生成时需要多大上下文"，再决定父块大小，避免拍脑袋。
- **验收**：同一问题下，父子块方案的答案完整度明显优于纯小块（人工评 10 题）。

### Day 18 · 周四 · 1.5h ｜ 元数据与标量过滤
- **任务**：为每个块补齐元数据，并实现按部门/时间过滤检索。
- **知识点**：标题路径、页码、来源、更新时间、部门/密级标签；过滤字段的基数与索引代价；过滤与向量检索的执行顺序。
- **材料**：[Qdrant 过滤与 payload 索引](https://qdrant.tech/documentation/concepts/filtering/)；[Milvus 布尔表达式](https://milvus.io/docs/boolean.md)。
- **方法**：先设计再落库——画一张"字段-类型-是否可过滤-是否展示"的表，评审后再建索引。
- **验收**：能按"部门 = X 且 时间 > Y"过滤后检索；过滤后召回率下降幅度有量化。

### Day 19 · 周五 · 2h ｜ 向量库选型与建库
- **任务**：用 Qdrant（或 Milvus Lite）建 collection，导入 1 万个块。
- **知识点**：collection / partition / payload 的概念；HNSW 参数在库里的映射；批量写入与索引构建耗时；快照与备份。
- **材料**：[Qdrant 快速开始](https://qdrant.tech/documentation/quickstart/)与[集合配置](https://qdrant.tech/documentation/concepts/collections/)；[Milvus 索引文档](https://milvus.io/docs/index-vector-fields.md)。
- **方法**：小规模验证——先 1000 条验证写入与查询，再扩到 1 万，记录耗时曲线。
- **验收**：1 万块导入成功；查询 P95 < 100ms；能说清三者在运维上的差异。

### Day 20 · 周六 · 2h ｜ 切分 A/B 实验
- **任务**：三种切分 × 同一 30 题，产出 Recall@5 对比。
- **知识点**：控制变量（同 embedding、同 Top-k、同评测集）；Recall@k 与 MRR 的定义；块长与召回的非线性关系。
- **材料**：Day 14 的评测集；`experiments.md` 模板。
- **方法**：一次只变一个因素；每组跑 3 次取均值，记录方差。
- **验收**：报告含三组 Recall@5 / MRR / 平均块长 / 索引大小；结论能落到"选哪种、为什么"。

### Day 21 · 周日 · 2h ｜ 周复盘：写第一份实验报告
- **任务**：把 Day 20 整理成"假设-设置-结果-结论-下一步"的报告。
- **方法**：用"如果重做一次，我会先测什么"结尾，训练实验设计感。
- **验收**：报告能让别人复现；评测集修正项已回写。

---

## 六、第 4 周：混合召回

### Day 22 · 周一 · 1.5h ｜ 向量检索的失效边界
- **任务**：构造 20 条"型号/错误码/人名"query，验证 dense 与 sparse 的差异。
- **知识点**：DPR 双塔与难负例；BEIR 的核心结论（BM25 是强基线，跨域时 dense 未必赢）；OOD 查询。
- **材料**：[DPR §2–3](https://arxiv.org/abs/2004.04906)；[BEIR 摘要与结论表](https://arxiv.org/abs/2104.08663)。
- **方法**：对抗性构造——专门找 embedding 会"语义相近但答案错"的例子，形成失败案例库。
- **验收**：能给出 dense 与 sparse 各自胜出的 query 类型清单，每类 ≥ 3 例。

### Day 23 · 周二 · 1.5h ｜ RRF 融合
- **任务**：实现 RRF，对比"分数归一化加权融合"。
- **知识点**：RRF 公式 `1/(k + rank)`；k=60 的经验来源；排名融合对分数尺度不敏感的原因；加权 RRF。
- **材料**：[Elasticsearch RRF 文档](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion)；[Qdrant 混合查询](https://qdrant.tech/documentation/concepts/hybrid-queries/)。
- **方法**：消融——分别只保留向量、只保留 BM25、两者融合，看 Recall@5 增量来自谁。
- **验收**：融合后 Recall@5 相对单路提升 ≥ 5 个百分点，或能解释为何没有。

### Day 24 · 周三 · 1.5h ｜ 多向量与迟交互
- **任务**：用 bge-m3 的多向量能力（或 ColBERT 实现）做一次检索对比。
- **知识点**：ColBERT 的 late interaction 与 MaxSim；token 级向量带来的存储放大；与 cross-encoder 的区别（一个用于召回，一个用于重排）。
- **材料**：[ColBERT §2 架构图](https://arxiv.org/abs/2004.12832)；[bge-m3 模型卡](https://huggingface.co/BAAI/bge-m3)的多向量说明。
- **方法**：算成本账——估算 100 万块的存储与查询开销，再决定是否值得。
- **验收**：能说清"为什么 late interaction 比单向量贵，但比 cross-encoder 便宜"。

### Day 25 · 周四 · 1.5h ｜ Query 改写
- **任务**：实现多查询扩展与 HyDE，各测 10 题。
- **知识点**：多查询的召回增益与延迟代价；HyDE 用"假设答案"去检索的原理与风险（假设错则全错）；改写要保留实体与限定词。
- **材料**：[HyDE §2 方法](https://arxiv.org/abs/2212.10496)；[LlamaIndex 查询变换](https://docs.llamaindex.ai/en/stable/optimizing/advanced_retrieval/query_transformations/)。
- **方法**：错误注入——故意让改写漏掉年份/型号，观察召回如何崩，建立"改写禁忌"清单。
- **验收**：两种方法的 Recall 增益与延迟增量都有数字；能说出各自适用场景。

### Day 26 · 周五 · 1.5h ｜ 子问题拆解与意图路由
- **任务**：把一个复合问题拆成 2–3 个子查询，分别检索后合并。
- **知识点**：复合问题的类型（比较、聚合、多跳）；拆解 prompt 的设计；路由到不同索引（制度库 / 产品库 / 工单库）。
- **材料**：[LlamaIndex SubQuestion 查询引擎](https://docs.llamaindex.ai/en/stable/examples/query_engine/sub_question_query_engine/)（读流程即可）。
- **方法**：手工先跑——先人工拆 10 个问题验证收益，再让 LLM 拆，比较两者差距。
- **验收**：复合问题的人工评分提升可量化；拆解失败的模式被记录。

### Day 27 · 周六 · 2h ｜ 混合召回 A/B
- **任务**：四组配置（纯向量 / 纯 BM25 / RRF / 加权）跑 50 题。
- **知识点**：指标口径统一；P95 延迟测量；成本按"每次查询的 embedding + 检索调用"计。
- **材料**：前几天的实现；`experiments.md`。
- **方法**：盲评——生成结果去掉配置标签后人工打分，避免"知道是哪个方案就偏袒"。
- **验收**：四组指标表完整；结论能回答"多花的延迟买到了多少召回"。

### Day 28 · 周日 · 2h ｜ 周复盘：召回漏斗 v1
- **任务**：画出"候选 → 过滤 → 融合 → Top-k"的漏斗，标每层数量与损失。
- **方法**：用真实 query 的数字填漏斗，不接受估算。
- **验收**：能指出漏斗最窄的一层，并给出下周的单个优化假设。

---

## 七、第 5 周：重排与上下文组装

### Day 29 · 周一 · 1.5h ｜ Cross-encoder 重排
- **任务**：接入 bge-reranker-v2-m3，对 Top-50 重排取 Top-5。
- **知识点**：双塔 vs 交叉编码器（是否能看到 query-doc 交互）；输入截断长度；batch 与显存；重排的边际收益随召回质量变化。
- **材料**：[bge-reranker-v2-m3 模型卡](https://huggingface.co/BAAI/bge-reranker-v2-m3)；[sentence-transformers CrossEncoder 用法](https://www.sbert.net/docs/cross_encoder/usage/usage.html)。
- **方法**：分层测试——分别对"召回好"和"召回差"的 query 看重排收益，验证"重排救不了没召回"。
- **验收**：nDCG@10 提升有数字；能画出"重排前后 Top-5 变化"的例子。

### Day 30 · 周二 · 1.5h ｜ LLM 重排与成本
- **任务**：用 LLM 做 listwise 重排，对比 cross-encoder 的质量/延迟/成本。
- **知识点**：pointwise / pairwise / listwise 三种范式；上下文长度导致的截断；缓存与批处理；何时不值得用 LLM 重排。
- **材料**：[RankGPT 论文](https://arxiv.org/abs/2304.09542)（listwise 重排的代表工作）。
- **方法**：三角对比——同 20 题，记录质量、P95 延迟、单次成本三个数，画散点。
- **验收**：能给出"什么规模/什么延迟预算下选哪种"的决策规则。

### Day 31 · 周三 · 1.5h ｜ 过滤：预过滤 vs 后过滤
- **任务**：实现两种过滤顺序，构造"过滤后召回不足"的案例。
- **知识点**：预过滤（检索时带条件）与后过滤（检索后删）的差异；后过滤导致 Top-k 实际不足；过滤字段的选择性；权限场景必须预过滤。
- **材料**：[Qdrant 过滤的 must/should 语义](https://qdrant.tech/documentation/concepts/filtering/)；[Milvus 布尔表达式](https://milvus.io/docs/boolean.md)。
- **方法**：极端构造——把过滤条件设成只命中 1% 数据，观察后过滤的召回崩塌。
- **验收**：能量化两种顺序的召回差异；能写出"过滤下推"的检查清单。

### Day 32 · 周四 · 1.5h ｜ 上下文组装
- **任务**：实现去重、邻近块扩展、按 token 预算分配上下文。
- **知识点**：MMR 去冗余；相邻块合并；"Lost in the Middle" 的位置效应（重要内容放头尾）；token 预算按相关性分配而非平均。
- **材料**：[Lost in the Middle §3–4（U 型曲线）](https://arxiv.org/abs/2307.03172)；[Anthropic 语境增强](https://www.anthropic.com/news/contextual-retrieval)。
- **方法**：顺序实验——同一组块，正序 / 逆序 / 头尾放置三种排法，看答案差异。
- **验收**：能复现"中间位置信息被忽略"的现象；组装后的上下文长度可控。

### Day 33 · 周五 · 1.5h ｜ 引用与可追溯
- **任务**：让每个引用能定位到原文页码与 bbox，并在 UI/终端高亮。
- **知识点**：块 id 与原文坐标的映射；引用编号的稳定性；模型编造引用的检测（引用编号必须在给定集合内）；多块合并后的引用归属。
- **材料**：Day 5 的 citation 实现；[RAGFlow 的引用回溯设计](https://github.com/infiniflow/ragflow)（读接口与数据结构）。
- **方法**：反向校验——从答案里的每个引用出发，检查它是否真支持该句，统计"引用不支持"的比例。
- **验收**：引用可点击回溯；"引用不支持"比例 < 5%。

### Day 34 · 周六 · 2h ｜ 端到端 A/B（质量-延迟-成本三角）
- **任务**：四组配置跑 50 题，产出三角对比图。
- **知识点**：端到端指标（faithfulness、答案正确率）与中间指标（Recall、nDCG）的关系；延迟拆解（检索/重排/生成）；成本口径。
- **材料**：`experiments.md`；Day 14 评测集。
- **方法**：固定预算对比——在 P95 延迟 ≤ 3s 的约束下比质量，而不是无限堆算力。
- **验收**：能回答"多花 800ms 换 6 个点准确率值不值"。

### Day 35 · 周日 · 2h ｜ 周复盘：漏斗 v2 + 选型结论
- **任务**：更新漏斗，写"最终检索方案"的一页说明。
- **方法**：让一个没参与的人按文档复现，卡住的地方就是文档缺陷。
- **验收**：方案说明含参数、指标、失败边界。

---

## 八、第 6 周：生成、拒答与评测闭环

### Day 36 · 周一 · 1.5h ｜ Grounded Generation
- **任务**：重写 prompt，让答案严格基于上下文并逐句标注引用。
- **知识点**：指令/上下文/输出格式的三段式；"只依据上下文"的约束强度；few-shot 示例的作用；温度设为 0 的必要性。
- **材料**：[RAG 论文 §2 生成部分](https://arxiv.org/abs/2005.11401)；[Anthropic 引用实践](https://www.anthropic.com/news/contextual-retrieval)（看上下文如何影响答案忠实度）。
- **方法**：对抗测试——给一个上下文里没有的问题，看模型是否老实说不知道。
- **验收**：30 题中引用支持率 ≥ 95%；无答案题的编造率显著下降。

### Day 37 · 周二 · 1.5h ｜ 拒答与不确定表达
- **任务**：实现"检索分数阈值 + LLM 自评"的双重拒答。
- **知识点**：误拒与漏拒的权衡；阈值校准（用评测集画 PR 曲线）；"部分回答 + 说明缺什么"的中间态。
- **材料**：Day 14 评测集中的无答案题；[RAGAS 的 answer relevancy 定义](https://docs.ragas.io/en/stable/concepts/metrics/)。
- **方法**：阈值扫描——在 30 题上看拒答率与误拒率，选业务可接受的工作点。
- **验收**：无答案拒答率 ≥ 80%，误拒率 ≤ 10%；工作点有数据支撑。

### Day 38 · 周三 · 1.5h ｜ 多轮对话
- **任务**：实现基于历史的 query 改写（指代消解），并加会话摘要。
- **知识点**：多轮指代（"它""这个方案"）；历史过长时的压缩策略；改写引入的漂移；话题切换检测。
- **材料**：[LlamaIndex 对话式检索](https://docs.llamaindex.ai/en/stable/examples/chat_engine/chat_engine_condense_question/)；[Dify 会话变量设计](https://github.com/langgenius/dify)。
- **方法**：构造多轮脚本——每轮只改动一个指代，看改写是否跟上。
- **验收**：10 组多轮对话中，指代改写正确率 ≥ 8/10。

### Day 39 · 周四 · 1.5h ｜ 评测指标与 RAGAS
- **任务**：用 RAGAS 跑一遍现有系统，得到四个核心指标。
- **知识点**：faithfulness、answer relevancy、context precision、context recall 的计算逻辑；LLM-as-judge 的角色；指标之间的依赖关系。
- **材料**：[RAGAS §2 指标定义](https://arxiv.org/abs/2309.15217)；[RAGAS 指标文档](https://docs.ragas.io/en/stable/concepts/metrics/)。
- **方法**：手工对照——抽 5 条，自己算一遍 faithfulness，与工具结果比对，理解差异来源。
- **验收**：四个指标能解释"分别对应链路的哪一环"。

### Day 40 · 周五 · 2h ｜ 评测集扩到 100 题 + judge 校准
- **任务**：扩题并校准 LLM judge（与人工 30 题比对一致性）。
- **知识点**：题目分布（单跳/多跳/比较/无答案）；judge 的长度偏差与位置偏差；Cohen's kappa；评分 rubric 的写法。
- **材料**：Day 14 的标注规则；[RAGAS 评测流程](https://docs.ragas.io/en/stable/getstarted/evaluation/)。
- **方法**：双盲——人工先评，再让 judge 评，最后比对；分歧样本逐条讨论定规则。
- **验收**：judge 与人工一致率 ≥ 85%；分歧类型被归类记录。

### Day 41 · 周六 · 2h ｜ CI 回归与 Trace
- **任务**：把评测接进 pytest，每次改动自动跑并输出对比。
- **知识点**：评测的门禁阈值；回归基线的维护；trace 的 span 划分（检索/重排/生成）；token 与延迟归因。
- **材料**：[Langfuse 追踪入门](https://langfuse.com/docs/observability/get-started)；[pytest 参数化](https://docs.pytest.org/en/stable/how-to/parametrize.html)。
- **方法**：先手动跑通一次完整链路 trace，再自动化；报告只保留"变化了的指标"。
- **验收**：一次改动后 10 分钟内拿到指标 diff 与归因。

### Day 42 · 周日 · 2h ｜ 周复盘：归因报告模板
- **任务**：固化"改动 → 指标 → 归因 → 结论"的模板。
- **验收**：模板能套用到下一次改动，且不需要额外解释。

---

## 九、第 7 周：工程化（权限、多租户、部署）

### Day 43 · 周一 · 1.5h ｜ ACL 模型与权限同步
- **任务**：设计文档级 + 行级 ACL，画出权限数据模型。
- **知识点**：ACL / RBAC / ABAC 的取舍；文档继承目录权限；权限同步（LDAP / SCIM / 组织架构 API）；权限变更的传播延迟。
- **材料**：[Keycloak 授权服务](https://www.keycloak.org/docs/latest/authorization_services/)（RBAC/ABAC 的工业实现）；[Milvus 多租户](https://milvus.io/docs/multi_tenancy.md)。
- **方法**：从事故反推——假设"员工转岗后仍能搜到原部门文档"，倒推需要哪些字段与同步机制。
- **验收**：模型能表达"部门 + 密级 + 项目组"三种维度。

### Day 44 · 周二 · 1.5h ｜ 过滤下推与越权测试
- **任务**：把权限条件注入检索，写 10 条越权用例。
- **知识点**：检索前注入 vs 检索后删除；空结果即拒绝（fail-closed）；日志与缓存中的越权泄露；超级管理员的审计。
- **材料**：[Qdrant 过滤](https://qdrant.tech/documentation/concepts/filtering/)；Day 31 的过滤实现。
- **方法**：红队思维——自己扮演越权者，构造跨部门、跨租户、已删除文档、共享链接四类攻击。
- **验收**：10 条用例全绿；越权尝试全部被记录。

### Day 45 · 周三 · 1.5h ｜ 多租户隔离
- **任务**：实现租户隔离方案（独立 collection 或 tenant_id 过滤），并加配额。
- **知识点**：隔离级别与成本（独立库最贵、行级最便宜但最易错）；租户 id 的强约束；配额与限流；冷热数据分离。
- **材料**：[Qdrant 多租户指南](https://qdrant.tech/documentation/guides/multiple-partitions/)；[Milvus 多租户](https://milvus.io/docs/multi_tenancy.md)。
- **方法**：故障演练——故意漏传 tenant_id，看系统是否报错而不是返回全量。
- **验收**：漏传 tenant_id 时请求被拒；跨租户查询测试全绿。

### Day 46 · 周四 · 1.5h ｜ 增量同步与删除感知
- **任务**：实现基于 mtime/webhook 的增量索引与 tombstone 删除。
- **知识点**：变更捕获；幂等写入；删除的三种处理（硬删、软删、标记后重建）；索引与原文的一致性；重建 vs 增量的成本。
- **材料**：[Airbyte 同步模式](https://docs.airbyte.com/using-airbyte/core-concepts/sync-modes/)（增量同步的通用设计）。
- **方法**：一致性检查——定时比对"原文集合"与"索引集合"的差集。
- **验收**：删除文档 1 分钟内不可检索；重复同步不产生重复块。

### Day 47 · 周五 · 1.5h ｜ 部署形态与扩容
- **任务**：容器化部署，写一份私有化交付清单。
- **知识点**：CPU 推理与 GPU 推理的取舍；国产化/信创适配（embedding 模型替换）；水平扩展与无状态化；缓存（embedding 缓存、答案缓存）；限流。
- **材料**：[Qdrant 安装部署](https://qdrant.tech/documentation/guides/installation/)；[sentence-transformers 的 CPU 推理](https://www.sbert.net/)。
- **方法**：压测——用 10 并发跑 100 次查询，记录 P50/P95/错误率。
- **验收**：交付清单含依赖、端口、资源、备份、升级步骤。

### Day 48 · 周六 · 2h ｜ 成本与容量估算
- **任务**：估算 100 万文档的月度成本与所需资源。
- **知识点**：embedding 成本（token 数 × 单价）、重排成本（QPS × 单价）、存储（向量维度 × 数量 × 副本）、生成成本。
- **材料**：各模型厂商定价页（用你自己的实际单价）；[Qdrant 容量规划](https://qdrant.tech/documentation/guides/capacity-planning/)。
- **方法**：自下而上——按"文档数 → 块数 → token 数 → 调用次数"逐层推，不接受"大概"。
- **验收**：一张成本表 + 一句话结论（瓶颈在存储还是推理）。

### Day 49 · 周日 · 2h ｜ 周复盘：架构图 v2 + 风险清单
- **任务**：画出含权限、租户、增量、监控的完整架构图，列 Top-5 风险。
- **方法**：让架构图能回答"一条文档从上传到被检索，中间经过哪些组件、失败会怎样"。
- **验收**：每个组件标注了失败模式与降级策略。

---

## 十、第 8 周：进阶与收尾

### Day 50 · 周一 · 1.5h ｜ Agentic RAG
- **任务**：实现"检索 → 自评 → 再检索"的两轮循环。
- **知识点**：Self-RAG 的反思 token（是否检索/是否相关/是否支持）；CRAG 的检索评估器与查询分解；循环的停止条件与最大轮次；延迟成本。
- **材料**：[Self-RAG §2](https://arxiv.org/abs/2310.11511)；[CRAG §2](https://arxiv.org/abs/2401.15884)。
- **方法**：限定轮次——最多 2 轮，观察"第二轮是否真的救回了第一轮的错误"。
- **验收**：能给出"多一轮带来多少准确率、多少延迟"的数字。

### Day 51 · 周二 · 1.5h ｜ 检索原语工具化
- **任务**：把 search / filter / fetch / list_sources 暴露成 Agent 工具。
- **知识点**：工具描述即 prompt；参数设计（top_k、时间范围、来源过滤）；工具返回的截断与摘要；失败重试与降级。
- **材料**：[OpenAI 工具调用文档](https://platform.openai.com/docs/guides/function-calling)；[LangChain 工具定义](https://python.langchain.com/docs/how_to/custom_tools/)。
- **方法**：从调用日志反推——看模型最常传错哪个参数，就改哪个描述。
- **验收**：模型能自主选择"先 filter 再 search"，无需人工指定。

### Day 52 · 周三 · 2h ｜ GraphRAG 原理
- **任务**：跑通一个小规模 GraphRAG（100 份文档）。
- **知识点**：实体/关系抽取；社区检测（Leiden）；社区摘要；全局查询 vs 局部查询；索引成本。
- **材料**：[GraphRAG §2 索引管线、§3 查询模式](https://arxiv.org/abs/2404.16130)；[GraphRAG 官方仓库](https://github.com/microsoft/graphrag)（quickstart）。
- **方法**：先看成本再动手——估算 LLM 调用次数，决定文档规模。
- **验收**：能回答一个需要跨文档聚合的问题，并说明它为什么向量检索答不了。

### Day 53 · 周四 · 1.5h ｜ GraphRAG 的边界
- **任务**：对比 GraphRAG 与基线在 20 题上的表现与成本。
- **知识点**：增量更新困难；实体消歧；摘要漂移；适用场景（多跳、聚合、关系型问题）。
- **材料**：[GraphRAG §4 评估与成本讨论](https://arxiv.org/abs/2404.16130)。
- **方法**：算总账——索引成本 + 查询成本 + 维护成本，与收益对比。
- **验收**：能给出"什么条件下值得上 GraphRAG"的判断清单。

### Day 54 · 周五 · 1.5h ｜ 长上下文 vs RAG
- **任务**：对同一批文档，对比"全塞进上下文"与"RAG"的成本与质量。
- **知识点**：token 线性成本；注意力衰减与位置效应；prompt 缓存；"文档集合稳定且小"时才适合全塞。
- **材料**：[Lost in the Middle 结论](https://arxiv.org/abs/2307.03172)；模型厂商的上下文缓存定价页。
- **方法**：成本曲线——文档量 1/10/100 份各测一次，找交叉点。
- **验收**：能画出"文档量-成本"交叉图，并给出决策规则。

### Day 55 · 周六 · 2h ｜ 进阶 demo + 基线对比
- **任务**：选一个方向（Agentic 或 GraphRAG）做成可运行 demo，跑 100 题对比。
- **方法**：只报"相对基线的增量"，不重复报基线本身。
- **验收**：demo 可复现；对比表含质量、延迟、成本三列。

### Day 56 · 周日 · 2.5h ｜ 总复盘与作品集
- **任务**：整理 P0–P5 产出、指标对比、架构图，写成 3 页作品集。
- **知识点**：如何讲清"我解决了什么问题、用什么方法、量化结果如何"；失败实验也是资产。
- **方法**：STAR 结构（情境-任务-行动-结果），每条控制在 5 行内。
- **验收**：一个没做过 RAG 的人看完能复述你的方案与结论。

---

## 十一、每周复盘模板（复制到 `weekly-review.md`）

```markdown
## 第 N 周（日期）
- 本周假设：
- 实际结果（数字）：
- 差距与原因：
- 本周最大的认知修正：
- 下周唯一要验证的假设：
- 欠账（明确取舍，不遮掩）：
```

---

## 十二、落后了怎么办（优先级排序）

时间不够时，按此顺序砍：

1. **保**：Day 5（naive RAG）、Day 14（评测集）、Day 27/34（A/B）、Day 41（CI）、Day 44（越权测试）。
2. **可压缩**：Day 24（ColBERT）、Day 30（LLM rerank）、Day 45（多租户细节）、Day 52–53（GraphRAG）。
3. **可跳过**：Day 47（部署细节）、Day 51（工具化）——知道概念即可。

铁律：**可以少做实验，但不能没有评测集。** 没有评测集的 8 周，等于 8 天。

---

## 十三、每日打卡表（打印用）

| 周 | 一 | 二 | 三 | 四 | 五 | 六 | 日 |
|---|---|---|---|---|---|---|---|
| 1 | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
| 2 | D8 | D9 | D10 | D11 | D12 | D13 | D14 |
| 3 | D15 | D16 | D17 | D18 | D19 | D20 | D21 |
| 4 | D22 | D23 | D24 | D25 | D26 | D27 | D28 |
| 5 | D29 | D30 | D31 | D32 | D33 | D34 | D35 |
| 6 | D36 | D37 | D38 | D39 | D40 | D41 | D42 |
| 7 | D43 | D44 | D45 | D46 | D47 | D48 | D49 |
| 8 | D50 | D51 | D52 | D53 | D54 | D55 | D56 |
