# RAG 学习日志（站点源码）

用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 生成的学习日志站点。
内容从私有学习仓库 `rag_study` 同步过来，同步时做脱敏（内部项目名换成代号）。

## 目录

```
mkdocs.yml      站点配置
sync.py         同步脚本：拉笔记 → 脱敏 → 加 front matter → 生成首页
extra/          手写页面（关于）
docs/           ← 生成物，不要手改（sync.py 会覆盖 D01..Dnn、index.md）
site/           ← 构建产物（gitignore）
```

## 本地流程

```powershell
cd D:\code\rag_study

# 1) 同步内容（每次写完笔记都跑一次）
.\.venv\Scripts\python.exe blog\sync.py

# 2) 本地预览  http://127.0.0.1:8000
.\.venv\Scripts\python.exe -m mkdocs serve -f blog\mkdocs.yml

# 3) 构建检查（报 WARNING 说明有死链或缺文件）
.\.venv\Scripts\python.exe -m mkdocs build -f blog\mkdocs.yml

# 4) 发布到 gh-pages
.\.venv\Scripts\python.exe -m mkdocs gh-deploy -f blog\mkdocs.yml
```

## 首次发布（仓库建好后做一次）

```powershell
cd D:\code\rag_study\blog
git init -b main
git config user.email "你的GitHub数字ID+用户名@users.noreply.github.com"   # 别用公司邮箱
git add -A
git commit -m "init: MkDocs Material 学习日志站点"
git remote add origin git@github.com:<用户名>/rag-study.git
$env:GIT_SSH='C:\Windows\System32\OpenSSH\ssh.exe'
git push -u origin main
```

然后到仓库 Settings → Pages，把来源设成 **Deploy from a branch → gh-pages / (root)**。
`mkdocs gh-deploy` 会把构建好的静态站推到 `gh-pages` 分支。

## 换地址

建好仓库后，把 `mkdocs.yml` 里两处 `USERNAME` 换成真实用户名（`site_url` /
`repo_url`），否则 sitemap 和页头仓库链接会指向不存在的地址。

## 加一天笔记怎么做

在 `rag_study\notes\` 下新建 `D03` 目录、写完笔记，然后重跑 `sync.py` +
`gh-deploy`。天数、日期、首页表格、侧边栏都是自动的，配置不用动。

## 脱敏规则

见 `sync.py` 顶部的 `REDACT`。要加新词就改那一处，重跑同步即可。
`项目与学习计划对照.md` 这类文档默认不上站（`PUBLISH_ROOT` 白名单控制）。
