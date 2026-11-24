# 我的博客（站点源码）

用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 生成的个人站点，
**一个站、多个集合**，左侧栏按集合分组。站点根地址 <https://symbii.github.io/>。

内容从私有学习仓库 `rag_study` 同步过来，同步时做脱敏（项目名换成代号）。

## 结构

```
mkdocs.yml      站点配置（nav 由 sync.py 生成，见文件里的 NAV 标记）
sync.py         同步脚本：拉笔记 → 脱敏 → 加 front matter → 生成首页与 nav
publish.py      构建 + 推到 gh-pages（替代会崩的 mkdocs gh-deploy）
extra/          站点级手写页面（about.md）
docs/           ← 生成物，不要手改
  index.md              站点首页（集合总览）
  about.md              关于本站
  rag-study/            集合：RAG 学习 56 天
    index.md            集合首页（进度表）
    D01/ D02/ …         每日笔记
    papers/             论文译文
    *.md                几篇长文档
site/           ← 构建产物（gitignore）
```

URL 就是目录结构：`docs/rag-study/D01/00-今日概览.md` → `/rag-study/D01/00-今日概览/`。
所以集合加进 `docs/<集合名>/` 之后，老链接不需要重定向就还在。

## 加一个集合

1. 在 `sync.py` 的 `COLLECTIONS` 里加一行（目录名 → 标题 / 一句话介绍）；
2. 写一个 `sync_xxx()` 把内容放进 `docs/<目录名>/`；
3. 重跑 `sync.py` —— 站点首页的集合卡片、侧栏分组、nav 标记区都会自动更新。

## 本地流程

```powershell
cd D:\code\rag_study

# 1) 同步内容（每次写完笔记都跑一次）
.\.venv\Scripts\python.exe blog\sync.py

# 2) 本地预览  http://127.0.0.1:8000
.\.venv\Scripts\python.exe -m mkdocs serve -f blog\mkdocs.yml

# 3) 构建 + 发布到 gh-pages
.\.venv\Scripts\python.exe blog\publish.py
```

`publish.py` 用 `--strict` 构建：死链、找不到的图片都会让它停下，不会发布半成品。
它也不用 `mkdocs gh-deploy`——那个命令会调 msys 的 `sh.exe`，在这台机器上崩
（`fatal error - couldn't create signal pipe, Win32 error 5`）。

## 一次性设置（已完成）

- 仓库名必须是 **`<用户名>.github.io`**（本项目是 `Symbii/symbii.github.io`），
  GitHub 才会把它发布到根路径 `https://symbii.github.io/`；
- Settings → Pages → Source 选 **Deploy from a branch → `gh-pages` / (root)**；
- 站点能打开，但 `gh-pages` 分支是 `publish.py` 强推的，**别手动编辑那个分支**。

## 加一天笔记怎么做

在 `rag_study\notes\` 下新建 `D03` 目录、写完笔记，然后：
`sync.py` → `publish.py`。天数、日期、集合首页表格、侧栏分组都是自动的。

## 脱敏规则

见 `sync.py` 顶部的 `REDACT`（公司名、产品名、私有项目路径都在里面）。
要加新词就改那一处，重跑同步即可。
`项目与学习计划对照.md` 这类文档默认不上站（`PUBLISH_ROOT` 白名单控制）。
