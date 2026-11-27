---
title: "RAGFlow 源码学习地图（配 56 天计划）"
---
# RAGFlow 源码学习地图（配 56 天计划）

> 配读文档：[RAG 引擎学习地图](RAG引擎学习地图.md) · [RAG 引擎每日学习计划](RAG引擎每日学习计划.md)
> 源码位置：`third_party/ragflow-0.27.3`（已 gitignore，不进版本库）
> 版本：v0.27.3，RAGFlow 最后一条 Python 主线

## 0. 为什么读这个版本

RAGFlow 上游主线已到 v1.0.0，整仓用 Go 重写（`internal/deepdoc`、`internal/engine`、`cmd/`）。理念没变，但代码从一个 Python 文件里的函数变成了跨包的接口实现，对第一次读 RAG 源码的人来说噪声太大。

v0.27.3 还是完整的 Python 实现，`rag/` 加 `deepdoc/` 两层结构，一个函数 30 行内能读完，适合拿来对照自己手写的 naive RAG。等 8 周跑完、想看成产级实现时，再切到 1.0 的 Go 版对照不迟。

拉取方式（已执行，需要重拉时用）：

```powershell
git clone --depth 1 --branch v0.27.3 --filter=blob:none --sparse https://gitee.com/infiniflow/ragflow.git third_party/ragflow-0.27.3
git -C third_party/ragflow-0.27.3 sparse-checkout set --no-cone /rag/ /deepdoc/ /api/ /agent/ /mcp/ /conf/ /docker/ /pyproject.toml /README.md
```

本仓总量 15.3 MB，`rag/` 251 个文件，`deepdoc/` 65 个，`api/` 164 个，`agent/` 159 个。

## 1. 五分钟建立代码地图

RAGFlow 只有两条链路，其余都是外围。

```
写入链路（离线，一次）
  文件 → 解析 deepdoc/parser/* → 版面/表格/OCR deepdoc/vision/*
       → 切分 rag/app/naive.py:chunk() → 向量化 rag/llm/embedding_model.py
       → 入库 rag/utils/*_conn.py
  调度者：rag/svr/task_executor.py:do_handle_task()

查询链路（在线，每次）
  question → 改写/分析 rag/nlp/query.py:question()
           → 混合检索 rag/nlp/search.py:search()  (BM25 + kNN)
           → 融合排序 rag/nlp/search.py:retrieval()  (rerank_by_model)
           → 拼上下文 rag/prompts/generator.py:kb_prompt()
           → 生成 + 引用 generator.py:citation_prompt() / search.py:insert_citations()
```

对应 D01 要画的 8 环链路图：解析（deepdoc）、切分（naive.chunk）、编码（embedding_model）、索引（*_conn）、查询理解（query.question）、召回（search.search）、重排（search.retrieval）、组装加生成（generator）。RAGFlow 把解析看得极重，`deepdoc/` 占了 65 个文件，这是它与论文版 RAG 最大的差别。

## 2. 读源码的三层法

第一层看调用链，30 分钟，只读签名。在整仓 grep 概念词，把谁调用谁画出来，不读函数体。

```powershell
Select-String -Path third_party/ragflow-0.27.3/rag/*/*.py -Pattern 'def retrieval|def chunk|def search'
```

第二层读单函数，每天 15–25 分钟。只读当天锚点那一个函数，读到能回答输入什么、输出什么、中间改了哪三个字段，其它一律跳过。

第三层找反例，每周一次。读完问一句它在什么情况下会错。RAGFlow 的注释和 `try/except` 里常藏着工程妥协，比如 `_is_garbled_text`、`min_match`，那才是真实世界的信号。

不要做的事：不要从 `api/` 开始读，全是参数校验；不要通读 `rag/app/naive.py`（66 KB）；不要读 `rag/utils/*_conn.py` 全量，十几个向量库适配器，选一个读即可。

## 3. 每周对应源码

| 周 | 主题 | 主要源码区 | 读它的目的 |
|---|---|---|---|
| W1 | 基础底座 + 朴素 RAG | `rag/svr/task_executor.py`、`rag/nlp/search.py`、`rag/app/naive.py` | 把论文里的两段式落到两条真实链路上 |
| W2 | 解析攻坚 | `deepdoc/parser/`、`deepdoc/vision/` | 看工业级解析怎么处理双栏/表格/扫描件 |
| W3 | 切分与索引 | `rag/app/naive.py`、`rag/nlp/__init__.py`、`rag/utils/es_conn.py` | 切分参数如何影响检索，索引怎么建 |
| W4 | 混合召回 | `rag/nlp/query.py`、`rag/nlp/search.py`、`rag/graphrag/search.py` | 向量+BM25 融合的真实权重与失效点 |
| W5 | 重排与组装 | `rag/nlp/search.py`、`rag/llm/rerank_model.py`、`rag/prompts/generator.py` | 重排怎么接、上下文怎么裁、引用怎么对齐 |
| W6 | 生成与评测 | `rag/prompts/generator.py`、`rag/benchmark.py`、`rag/prompts/sufficiency_check.md` | 拒答/忠实/评测闭环的工程写法 |
| W7 | 工程化 | `api/apps/`、`rag/nlp/search.py:get_filters`、`rag/utils/es_conn.py` | 权限过滤下推、多租户、增量同步 |
| W8 | 进阶 | `rag/advanced_rag/`、`rag/graphrag/`、`agent/tools/retrieval.py` | Agentic RAG 与 GraphRAG 的真实形态 |

## 4. 每日锚点（56 天）

行号对应 v0.27.3，读之前先 `git -C third_party/ragflow-0.27.3 log -1` 确认版本；换版本后行号会漂，用函数名 grep。

### 第 1 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D01 | RAG 解决什么问题 | `rag/svr/task_executor.py:1449 do_handle_task`；`rag/nlp/search.py:717 retrieval` | 两条链路各几步，8 环分别落在哪个函数 |
| D02 | Embedding 与相似度 | `rag/llm/embedding_model.py:225 BuiltinEmbed`、`:245 encode`；`rag/nlp/search.py:714 hybrid_similarity` | 归一化在哪做；为什么检索分数是 token 分与向量分的加权 |
| D03 | HNSW | `rag/svr/task_executor.py:744 init_kb`（只调 `create_idx`）；`rag/utils/vastbase_conn.py:482` 的 `m=16, ef_construction=50`；`rag/utils/es_conn.py:198 search` | 大多数后端把 HNSW 参数交给引擎默认值，只有自己建图的实现才写死参数；kNN 的 `knn_top_k`/`knn_num_candidates` 怎么下发 |
| D04 | BM25 | `rag/nlp/query.py:42 question`；`rag/nlp/term_weight.py`；`rag/nlp/__init__.py:423 tokenize` | 中文 query 怎么变成 term 权重，专有名词怎么保 |
| D05 | 手写 naive RAG | `rag/app/naive.py:1123 chunk` | 切分的输入输出字段（`content_with_weight`、`content_ltks`、`docnm_kwd`…），对照你的 100 行 |
| D06 | 误差分析 | `rag/nlp/search.py:431 insert_citations`；`:242 get_filters` | 引用对不上会怎样；过滤条件写错会静默返回空 |
| D07 | 周复盘 | `rag/flow/pipeline.py`；`rag/svr/task_executor_refactor/` | 工程化如何把一个函数拆成可重试的阶段 |

### 第 2 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D08 | PDF 文本层 | `deepdoc/parser/pdf_parser.py:56 RAGFlowPdfParser`、`:1633 __images__` | 它怎么把 char 级内容重组成行和块 |
| D09 | 双栏与阅读顺序 | `pdf_parser.py:905 _assign_column`、`:989 _text_merge`、`:1108 _final_reading_order_merge` | 栏检测、纵向合并、最终排序三段逻辑 |
| D10 | 表格抽取 | `pdf_parser.py:1307 _extract_table_figure`；`deepdoc/vision/table_structure_recognizer.py`；`rag/app/table.py` | 有线/无线表怎么分流，表格怎么转 Markdown |
| D11 | 扫描件 OCR | `pdf_parser.py:789 __ocr`；`deepdoc/vision/ocr.py`；`layout_recognizer.py` | det/rec/cls 三阶段的封装，版面识别输出什么 |
| D12 | 其它格式 | `deepdoc/parser/docx_parser.py`、`excel_parser.py`、`html_parser.py`、`markdown_parser.py` | 每种格式的结构信号从哪来 |
| D13 | 解析 pipeline 整合 | `rag/app/naive.py:171 by_deepdoc`、`:1123 chunk`；`deepdoc/parser/__init__.py` | 格式分派表 + 失败回退（`_is_garbled_text`） |
| D14 | 建 30 题评测集 | `rag/benchmark.py` | 它自带的评测脚本长什么样，指标怎么算 |

### 第 3 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D15 | 切分策略全景 | `rag/app/naive.py:1123 chunk` 里的 `parser_config`；`rag/nlp/delim.py` | `chunk_token_num`/`delimiter` 怎么传下去 |
| D16 | 语义切分 | `rag/nlp/__init__.py:371 bullets_category`、`:1241 title_frequency`、`:1271 tree_merge` | 它用标题频率加符号来猜层级，而不是真语义 |
| D17 | 结构化与父子块 | `rag/nlp/search.py:1101 retrieval_by_children` | 命中子块后怎么拉父块，代价是什么 |
| D18 | 元数据与过滤 | `rag/nlp/search.py:242 get_filters`；`rag/prompts/meta_filter.md` | 过滤条件的 DSL 从自然语言怎么生成 |
| D19 | 向量库选型 | `rag/utils/es_conn.py` vs `infinity_conn.py` vs `ob_conn.py`；`rag/settings.py` | 同一 `search()` 接口在不同后端的差异 |
| D20 | 切分 A/B | `rag/benchmark.py` | 怎么把 A/B 跑成可复现脚本 |
| D21 | 周复盘 | `rag/nlp/search.py:714 hybrid_similarity` | 你的权重假设与它的默认值差多少 |

### 第 4 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D22 | 向量检索失效边界 | `rag/nlp/search.py:255 search`、`rag/nlp/query.py:42 question` | `min_match` 的作用；query 太长/太短会怎样 |
| D23 | RRF 融合 | `rag/nlp/search.py:39 build_fusion_expr` | 它用的是加权融合还是 RRF，`vector_similarity_weight` 默认值 |
| D24 | 多向量与迟交互 | `rag/llm/rerank_model.py:62 similarity` | RAGFlow 用 cross-encoder 重排替代迟交互，边界在哪 |
| D25 | Query 改写 | `rag/nlp/query.py`；`rag/prompts/multi_queries_gen.md`；`rag/prompts/sca_query_rewrite.md` | 多查询生成与改写提示词的写法 |
| D26 | 子问题拆解与路由 | `rag/graphrag/search.py:139 retrieval`；`rag/advanced_rag/agentic_rag.py` | 复杂问题怎么被拆成多次检索 |
| D27 | 混合召回 A/B | `rag/nlp/search.py:717 retrieval` | 融合权重怎么进到最终排序 |
| D28 | 周复盘 | 召回漏斗相关日志字段 | 每级召回数量从哪打点 |

### 第 5 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D29 | Cross-encoder 重排 | `rag/nlp/search.py:673 rerank_by_model`；`rag/llm/rerank_model.py` | 重排分数怎么与召回分数合成 |
| D30 | LLM 重排与成本 | `rerank_model.py:58 Base`（`max_token`、批处理） | 一次重排的 token 预算怎么控制 |
| D31 | 预过滤 vs 后过滤 | `rag/nlp/search.py:242 get_filters`；`rag/utils/es_conn.py:75 _build_knn_filter_query` | 过滤条件如何进 kNN 的 filter；`vector_similarity_weight` 低于阈值时会剥掉 `query_string` 子句（性能妥协） |
| D32 | 上下文组装 | `rag/prompts/generator.py:168 kb_prompt`、`:69 message_fit_in` | 超预算时先丢谁；顺序怎么排 |
| D33 | 引用与可追溯 | `generator.py:41 chunks_format`、`:226 citation_prompt`；`search.py:431 insert_citations` | 引用编号从哪来、怎么回填到答案 |
| D34 | 端到端 A/B | `rag/benchmark.py` + 你的对比脚本 | 质量/延迟/成本三个量怎么一起记 |
| D35 | 周复盘 | `rag/prompts/generator.py` | 提示词工程在真实系统里的分量 |

### 第 6 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D36 | Grounded Generation | `rag/prompts/generator.py`（system prompt 拼装）、`rag/prompts/citation_prompt.md` | 怎么约束只能用给定材料 |
| D37 | 拒答与不确定 | `generator.py:575 _is_llm_error_answer`；`rag/prompts/sufficiency_check.md` | 它靠什么判断材料不够 |
| D38 | 多轮对话 | `generator.py:188 memory_prompt`、`:427 form_history` | 历史怎么截断、怎么与检索结果共存 |
| D39 | 评测指标与 RAGAS | `rag/benchmark.py`；`rag/prompts/structured_output_prompt.md` | 结构化输出如何让 judge 可解析 |
| D40 | 100 题 + judge 校准 | `rag/benchmark.py` | 批量评测的执行方式 |
| D41 | CI 回归与 Trace | `api/apps/langfuse_api.py`；`rag/svr/task_executor.py:211 set_progress` | 可观测性埋在哪 |
| D42 | 周复盘 | 归因报告模版 + 你自己的表 | 无 |

### 第 7 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D43 | ACL 模型与权限同步 | `api/db/` 中用户/租户表；`rag/nlp/search.py:242 get_filters` | 权限落到检索条件上的方式 |
| D44 | 过滤下推与越权测试 | `rag/utils/es_conn.py:75 _build_knn_filter_query`、`:198 search` | kNN 与 bool filter 合并成一个查询；注意它会把 `query_string` 子句从 filter 里摘掉，越权测试要专门盯这条路径 |
| D45 | 多租户隔离 | `rag/nlp/search.py:49 index_name(uid)` | 按租户分索引还是分字段，各自的代价 |
| D46 | 增量同步与删除感知 | `rag/svr/sync_data_source.py` | 变更检测、失败重试、删除传播 |
| D47 | 部署形态与扩容 | `docker/`、`rag/svr/task_executor.py:204 signal_handler` | 无状态/有状态边界在哪 |
| D48 | 成本与容量估算 | `rag/llm/model_meta.py` | 模型元数据里有没有价格/上下文长度 |
| D49 | 周复盘 | `api/apps/` 整体 | 你的架构图 v2 与它的差距 |

### 第 8 周

| Day | 主题 | 锚点 | 看什么 |
|---|---|---|---|
| D50 | Agentic RAG | `rag/advanced_rag/agentic_rag.py`、`agentic_rag_graph.py` | 检索被改成可多次调用后的控制流 |
| D51 | 检索原语工具化 | `agent/tools/retrieval.py` | 检索怎么变成 agent 的一个 tool |
| D52 | GraphRAG 原理 | `rag/graphrag/general/`（`graph_extractor.py`、`leiden.py`、`community_reports_extractor.py`） | 实体抽取、社区发现、社区摘要三步 |
| D53 | GraphRAG 边界 | `rag/graphrag/light/graph_extractor.py`、`rag/graphrag/search.py:35 KGSearch` | 轻量版砍掉了什么，为什么 |
| D54 | 长上下文 vs RAG | `rag/prompts/generator.py:69 message_fit_in` | 截断策略暴露的取舍 |
| D55 | 进阶 demo + 基线 | `rag/benchmark.py` | 用它的评测口径对齐自己的基线 |
| D56 | 总复盘 | 全仓 | 用自己的链路图逐环对照 |

## 5. 五个必读片段（信息密度最高，合计 40 分钟）

按顺序读，每个都短：

1. `rag/app/naive.py:1123 chunk()`，一个函数吃进文件、吐出带元数据的块，所有切分讨论的落点。
2. `rag/nlp/search.py:717 retrieval()`，召回、融合、重排的唯一入口，读完就懂检索在工程上是什么。
3. `rag/prompts/generator.py:168 kb_prompt()`，检索结果变成 prompt 的那 20 行，`max_tokens` 裁剪就发生在这里。
4. `rag/svr/task_executor.py:1449 do_handle_task()`，写入链路的总调度，看它如何记录进度、失败重试。
5. `deepdoc/parser/pdf_parser.py:1108 _final_reading_order_merge()`，阅读顺序的启发式规则，比任何博客都具体。

## 6. 一条规则：源码只用来验证，不用来学概念

先读论文和文档建立概念，再用源码回答它到底怎么实现的，不要反过来。

- 学 HNSW，先跑自己的 FAISS 实验，再看 `init_kb` 里参数怎么填；
- 学 BM25，先手写一遍，再看 `term_weight.py` 与 ES 查询；
- 学重排，先算一次 cross-encoder 分，再看 `rerank_by_model` 怎么合成。

反过来的结果是：记住了 RAGFlow 的字段名，却说不出原理。

## 7. 与每日计划的衔接

每天读源码的预算 15–25 分钟，只读当天锚点那一个函数。超时就停，记一句没看懂的是 X，第二天再花 5 分钟补。

记录写在 `learning-log.md`，格式：

```
源码：rag/nlp/search.py:717 retrieval
看懂：三个分数怎么加权
没懂：vector_similarity_weight 为什么 0.3
```

## 8. 版本提示

- 本文件行号对应 v0.27.3；
- 上游 v1.0.0 起改为 Go（`internal/deepdoc`、`internal/engine`、`internal/agentic_rag`），概念一一对应但代码结构不同；
- 手上的教程和博客大多基于 0.1x–0.2x，其中 0.19 之前没有 `rag/graphrag/`，0.20 之后才有 `advanced_rag/`，对照时注意。
