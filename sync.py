"""把 rag_study 的学习笔记同步成 MkDocs 站点内容（脱敏 + 生成首页）。

用法（在 D:\\code\\rag_study 下）：
    .\\.venv\\Scripts\\python.exe blog\\sync.py

做四件事：
1. notes\\D01..Dnn  -> blog\\docs\\D01..Dnn（md 加 front matter，png 原样复制）
2. 根目录几篇可公开的 md -> blog\\docs\\
3. papers\\*.md -> blog\\docs\\papers\\
4. 按目录里的天数重新生成 blog\\docs\\index.md

脱敏只做项目名/公司名替换，不改技术内容。改映射就改 REDACT。
"""

from __future__ import annotations

import re
import shutil
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent      # D:\code\rag_study\blog
ROOT = HERE.parent                          # D:\code\rag_study
DOCS = HERE / "docs"

DAY1 = date(2026, 11, 23)      # D01 的日期
TOTAL_DAYS = 56

# 根目录下可以上站的文档（本项目对照文档有意排除）
PUBLISH_ROOT = [
    "RAG引擎学习地图.md",
    "RAG引擎每日学习计划.md",
    "RAGFlow源码学习地图.md",
    "learning-log.md",
    "experiments.md",
    "glossary.md",
]

# 脱敏：长的先替换
REDACT = [
    ("projects/index_agent", "projects/解析服务A"),
    ("projects/rag_service", "projects/检索服务B"),
    ("index_agent", "解析服务A"),
    ("rag_service", "检索服务B"),
    ("selfrag", "检索服务B"),
    ("闪捷信息", "某公司"),
    ("闪捷", "某公司"),
    ("secsmart", "example"),
    ("BackAgain", "某数据安全产品"),
    ("鲲洺", "某一体机"),
]

# 指向「不上站文档」的链接：保留文末文字，去掉链接本身
DROP_LINKS = re.compile(r"\[([^\]]+)\]\([^)]*项目与学习计划对照[^)]*\)")
# 指向站外文件的链接（AGENTS.md、third_party 目录、notes/README）同样只留文字
DROP_FOREIGN = re.compile(
    r"\[([^\]]+)\]\([^)]*(?:AGENTS\.md|third_party/|notes/README\.md)[^)]*\)"
)


def sanitize(text: str) -> str:
    for old, new in REDACT:
        text = text.replace(old, new)
    text = DROP_LINKS.sub(r"\1", text)
    text = DROP_FOREIGN.sub(r"\1", text)
    # 笔记从 notes/D01/x.md 搬到 docs/D01/x.md，上跳一层即可到 docs 根
    text = text.replace("](../../", "](../")
    return text


def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def front_matter(text: str, title: str, day_date: date | None) -> str:
    if text.lstrip().startswith("---"):
        return text
    lines = ["---", f'title: "{title}"']
    if day_date:
        lines.append(f"date: {day_date.isoformat()}")
    lines += ["---", ""]
    return "\n".join(lines) + text


def write_page(src: Path, dst: Path, day_date: date | None = None) -> None:
    raw = src.read_text(encoding="utf-8")
    body = sanitize(raw)
    title = title_of(body, src.stem)
    dst.write_text(front_matter(body, title, day_date), encoding="utf-8")


def link_label(name: str) -> str:
    """00-今日概览.md -> 今日概览"""
    return re.sub(r"^\d+-", "", name[:-3])


def sync_days() -> list[tuple[int, date, list[str]]]:
    days: list[tuple[int, date, list[str]]] = []
    for day_dir in sorted((ROOT / "notes").glob("D[0-9][0-9]")):
        n = int(day_dir.name[1:])
        d = DAY1 + timedelta(days=n - 1)
        out = DOCS / day_dir.name
        out.mkdir(parents=True, exist_ok=True)
        pages = []
        for f in sorted(day_dir.iterdir()):
            if f.is_dir():
                continue
            if f.suffix.lower() == ".png":
                shutil.copy2(f, out / f.name)
            elif f.suffix == ".md":
                write_page(f, out / f.name, d)
                pages.append(f.name)
        if pages:
            days.append((n, d, pages))
    return days


def sync_root_docs() -> list[str]:
    done = []
    for name in PUBLISH_ROOT:
        src = ROOT / name
        if src.exists():
            write_page(src, DOCS / name)
            done.append(name)
    return done


def sync_papers() -> list[str]:
    out = DOCS / "papers"
    out.mkdir(parents=True, exist_ok=True)
    done = []
    for f in sorted((ROOT / "papers").glob("*.md")):
        write_page(f, out / f.name)
        done.append(f.name)
    return done


def sync_extra() -> list[str]:
    """手写页面（关于、首页以外的固定页）放在 blog/extra，原样上站。"""
    done = []
    for f in sorted((HERE / "extra").glob("*.md")):
        shutil.copy2(f, DOCS / f.name)
        done.append(f.name)
    return done


def build_index(days: list[tuple[int, date, list[str]]], root_docs: list[str]) -> None:
    # 未来的天数目录（提前建的模板）不算进度、不进表格
    today = date.today()
    days = [x for x in days if x[1] <= today]
    latest = days[-1][0] if days else 0
    rows = []
    for n, d, pages in days:
        links = " · ".join(f"[{link_label(p)}](D{n:02d}/{p})" for p in pages)
        rows.append(f"| D{n:02d} | {d.isoformat()} | {links} |")

    doc_links = " · ".join(f"[{Path(x).stem}]({x})" for x in root_docs)

    text = f"""---
title: 首页
hide:
  - navigation
  - toc
---

# RAG 学习日志

56 天，把 RAG 从零手写一遍。每天一记：概念怎么理解、源码在哪一行、
实验得到什么数字、卡在哪里。

**进度**：{latest} / {TOTAL_DAYS} 天（最新 D{latest:02d}，{days[-1][1].isoformat() if days else "—"}）

## 每日笔记

| 天 | 日期 | 当天写了什么 |
|---|---|---|
{chr(10).join(rows) if rows else "| — | — | — |"}

## 常逛的几篇

{doc_links if doc_links else "—"}

- 论文精读：[RAG 原论文中英对照](papers/RAG-Lewis2020-中英对照.md)

## 这个站在学什么

从「RAG 到底在解决什么问题」开始，八环链路 → Embedding 与相似度 →
向量索引（HNSW）→ 词法检索（BM25）→ 重排 → 生成与引用 → 评测与误差分析，
最后落到一个能跑、能测、知道哪里会坏的小系统。

所有笔记都是当天现写的，有大量「这里我想错了」的记录——那部分比结论有用。
"""
    (DOCS / "index.md").write_text(text, encoding="utf-8")


def main() -> None:
    # 清掉上一轮的每日目录，避免删掉文件后站点残留
    for d in DOCS.glob("D[0-9][0-9]"):
        shutil.rmtree(d)
    days = sync_days()
    root_docs = sync_root_docs()
    papers = sync_papers()
    extras = sync_extra()
    build_index(days, root_docs)
    print(f"days   : {', '.join('D%02d(%d files)' % (n, len(p)) for n, _, p in days)}")
    print(f"root   : {', '.join(root_docs)}")
    print(f"papers : {', '.join(papers)}")
    print(f"extra  : {', '.join(extras)}")
    print(f"index  : {DOCS / 'index.md'}")


if __name__ == "__main__":
    main()
