"""把 rag_study 的学习笔记同步成 MkDocs 站点内容（脱敏 + 生成首页 + 生成侧栏导航）。

用法（在 D:\\code\\rag_study 下）：
    .\\.venv\\Scripts\\python.exe blog\\sync.py

站点是「单站多集合」结构，一个集合一个目录：

    docs/index.md              站点首页（集合总览，自动生成）
    docs/about.md              关于本站（手写，放 blog/extra/about.md）
    docs/rag-study/index.md    RAG 集合首页（进度表，自动生成）
    docs/rag-study/D01..Dnn/   每日笔记（从 notes/ 同步）
    docs/rag-study/papers/     论文译文
    docs/rag-study/*.md        几篇可公开的长文档

同步做五件事：
1. notes\\D01..Dnn      -> docs\\<集合>\\D01..Dnn（md 加 front matter，png 原样复制）
2. 根目录几篇可公开的 md -> docs\\<集合>\\
3. papers\\*.md         -> docs\\<集合>\\papers\\
4. 重生成 docs/index.md（站点首页）与 docs\\<集合>\\index.md（集合首页）
5. 重写 mkdocs.yml 里 `# >>> NAV` 与 `# <<< NAV` 之间的导航

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
MKDOCS_YML = HERE / "mkdocs.yml"

DAY1 = date(2026, 11, 23)      # D01 的日期
TOTAL_DAYS = 56
# 实际执行日期与计划日不一致时在这里覆盖（2026-11-25 用户定：D02 改 11-25）
DAY_DATE_OVERRIDES = {2: date(2026, 11, 25)}

SITE_NAME = "Void_Liao 的博客"
SITE_TAGLINE = "学习笔记与工程记录"

# 集合：目录名 -> 显示标题 / 一句话介绍。
# 以后加第二个集合（比如「论文精读」），在这里加一行 + 写对应的 sync 函数即可。
COLLECTIONS = {
    "rag-study": {
        "title": "RAG 学习 56 天",
        "desc": "56 天把 RAG 从零手写一遍：八环链路 → Embedding 与相似度 → HNSW → "
                "BM25 → 重排 → 生成与引用 → 评测与误差分析。",
    },
}

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
    ("projects/解析服务A/", "项目A/"),
    ("projects/检索服务B/", "项目B/"),
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

NAV_BEGIN = "# >>> NAV（由 blog/sync.py 生成，勿手改）"
NAV_END = "# <<< NAV"


def sanitize(text: str) -> str:
    for old, new in REDACT:
        text = text.replace(old, new)
    text = DROP_LINKS.sub(r"\1", text)
    text = DROP_FOREIGN.sub(r"\1", text)
    # 笔记从 notes/D01/x.md 搬到 docs/rag-study/D01/x.md，层级没变：
    # 上跳两级仍然是「集合根」，所以 ../../papers/ -> ../papers/ 照旧成立
    text = text.replace("](../../", "](../")
    # 站点只展示知识内容，不显示「[AI] / [本人]」来源标记（2026-11-25 用户要求）
    text = text.replace("（[AI] 绘制，2026-11-23）", "（2026-11-23）")
    text = text.replace("（[本人] 2026-11-23 14:47）", "（2026-11-23 14:47）")
    text = re.sub(r"（\[(?:AI|本人)\]([^）]*)）", r"（\1）", text)
    text = re.sub(r"\[(?:AI|本人)\]\s*", "", text)
    text = re.sub(r"^> \*\*来源标记.*\n?", "", text, flags=re.M)
    return text


def title_of(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def note_date(day_dir: Path) -> date | None:
    """从当天笔记标题里取实际学习日日期（`# D02 · 2026-11-25 周三 · 第 1 周`）。

    学习日不连续（2026-11-25 用户定），所以日期以笔记标题为准，不按日历推算。
    """
    for name in ("00-今日概览.md", "README.md"):
        f = day_dir / name
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
                return date.fromisoformat(m.group(1)) if m else None
    return None


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
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(front_matter(body, title, day_date), encoding="utf-8")


def link_label(name: str) -> str:
    """00-今日概览.md -> 今日概览"""
    return re.sub(r"^\d+-", "", name[:-3])


def day_label(n: int) -> str:
    """D00 是复习总结，不占学习日编号。"""
    return "复习" if n == 0 else f"D{n:02d}"


def collection_dir(slug: str) -> Path:
    return DOCS / slug


def sync_days(slug: str) -> list[tuple[int, date | None, list[str]]]:
    out_root = collection_dir(slug)
    days: list[tuple[int, date | None, list[str]]] = []
    for day_dir in sorted((ROOT / "notes").glob("D[0-9][0-9]")):
        n = int(day_dir.name[1:])
        if n == 0:
            # D00 是跨天累积的复习总结，没有学习日日期，也不算进度
            d = None
        else:
            d = note_date(day_dir) or DAY_DATE_OVERRIDES.get(n) or (DAY1 + timedelta(days=n - 1))
        out = out_root / day_dir.name
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
        # 笔记改名/删除后，docs 里会留下旧页；旧页不清掉就会一直发布过期内容
        for stale in out.glob("*.md"):
            if stale.name not in pages:
                stale.unlink()
        if pages:
            days.append((n, d, pages))
    return days


def sync_root_docs(slug: str) -> list[str]:
    done = []
    for name in PUBLISH_ROOT:
        src = ROOT / name
        if src.exists():
            write_page(src, collection_dir(slug) / name)
            done.append(name)
    return done


def sync_papers(slug: str) -> list[str]:
    out = collection_dir(slug) / "papers"
    out.mkdir(parents=True, exist_ok=True)
    done = []
    for f in sorted((ROOT / "papers").glob("*.md")):
        write_page(f, out / f.name)
        done.append(f.name)
    return done


def sync_extra() -> list[str]:
    """站点级手写资源（blog/extra）：*.md 原样上站，stylesheets/ 跟着复制。"""
    done = []
    for f in sorted((HERE / "extra").glob("*.md")):
        shutil.copy2(f, DOCS / f.name)
        done.append(f.name)

    css_src = HERE / "extra" / "stylesheets"
    if css_src.is_dir():
        css_out = DOCS / "stylesheets"
        css_out.mkdir(parents=True, exist_ok=True)
        for f in sorted(css_src.glob("*.css")):
            shutil.copy2(f, css_out / f.name)
            done.append(f"stylesheets/{f.name}")
    return done


def write_legacy_pages(slug: str) -> None:
    """旧站把「关于本站」放在 /rag-study/about/，搬成站点级 /about/ 后补一页保住老链接。"""
    (collection_dir(slug) / "about.md").write_text(
        "---\ntitle: 关于本站\n---\n\n# 关于本站\n\n这一页搬到了 [站点首页的关于页](../about.md)。\n",
        encoding="utf-8",
    )


def build_collection_index(
    slug: str, days: list[tuple[int, date | None, list[str]]], root_docs: list[str]
) -> int:
    meta = COLLECTIONS[slug]
    # 未来的天数目录（提前建的模板）不算进度、不进表格；D00 复习总结永远进表格但不计进度
    today = date.today()
    days = [x for x in days if x[0] == 0 or (x[1] is not None and x[1] <= today)]
    learning = [x for x in days if x[0] >= 1]
    latest = learning[-1][0] if learning else 0
    rows = []
    for n, _d, pages in days:
        links = " · ".join(f"[{link_label(p)}](D{n:02d}/{p})" for p in pages)
        rows.append(f"| {day_label(n)} | {links} |")

    text = f"""---
title: {meta["title"]}
hide:
  - toc
---

# {meta["title"]}

**进度**：{latest} / {TOTAL_DAYS} 天（最新 D{latest:02d}）

## 每日笔记

| 天 | 当天写了什么 |
|---|---|
{chr(10).join(rows) if rows else "| — | — |"}
"""
    (collection_dir(slug) / "index.md").write_text(text, encoding="utf-8")
    return latest


def build_home(progress: dict[str, int]) -> None:
    cards = []
    for slug, meta in COLLECTIONS.items():
        done = progress.get(slug, 0)
        cards.append(
            f"-   **{meta['title']}**\n\n"
            f"    ---\n\n"
            f"    [进入 →]({slug}/index.md) · 进度 {done} / {TOTAL_DAYS} 天\n\n"
        )
    text = f"""---
title: 首页
hide:
  - toc
---

<div class="hero" markdown>
<div class="bubbles">
<span></span><span></span><span></span><span></span><span></span>
</div>

# {SITE_NAME}

</div>

<div class="grid cards" markdown>
{chr(10).join(cards)}</div>
"""
    (DOCS / "index.md").write_text(text, encoding="utf-8")


def yq(value: str) -> str:
    """nav 里的值：含冒号空格、井号或首字符特殊时加引号。"""
    if re.search(r":\s|#|^[-?*&!|>@`\"'%{}\[\],]", value):
        return '"' + value.replace('"', '\\"') + '"'
    return value


def build_nav(
    per_collection: dict[str, tuple[list[tuple[int, date | None, list[str]]], list[str], list[str]]]
) -> None:
    lines = ["nav:", "  - 首页: index.md"]
    for slug, meta in COLLECTIONS.items():
        days, root_docs, papers = per_collection.get(slug, ([], [], []))
        lines.append(f"  - {yq(meta['title'])}:")
        lines.append(f"      - 概述: {slug}/index.md")
        for n, d, pages in days:
            head = day_label(n) if d is None else f"{day_label(n)} · {d.isoformat()}"
            lines.append(f"      - {head}:")
            for p in pages:
                lines.append(f"          - {yq(link_label(p))}: {slug}/D{n:02d}/{p}")
        if root_docs:
            lines.append("      - 参考:")
            for name in root_docs:
                lines.append(f"          - {yq(Path(name).stem)}: {slug}/{name}")
        if papers:
            lines.append("      - 论文:")
            for name in papers:
                lines.append(f"          - {yq(Path(name).stem)}: {slug}/papers/{name}")
    lines.append("  - 关于: about.md")
    nav = "\n".join(lines)

    text = MKDOCS_YML.read_text(encoding="utf-8")
    new, count = re.subn(
        re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END),
        NAV_BEGIN + "\n" + nav + "\n" + NAV_END,
        text,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f"mkdocs.yml 里没找到 NAV 标记（{NAV_BEGIN} / {NAV_END}）")
    MKDOCS_YML.write_text(new, encoding="utf-8")


def main() -> None:
    for slug in COLLECTIONS:
        # 清掉上一轮的每日目录，避免删掉文件后站点残留
        for d in collection_dir(slug).glob("D[0-9][0-9]"):
            shutil.rmtree(d)
        collection_dir(slug).mkdir(parents=True, exist_ok=True)

    extras = sync_extra()
    progress: dict[str, int] = {}
    per_collection = {}
    for slug in COLLECTIONS:
        write_legacy_pages(slug)
        days = sync_days(slug)
        root_docs = sync_root_docs(slug)
        papers = sync_papers(slug)
        progress[slug] = build_collection_index(slug, days, root_docs)
        per_collection[slug] = (days, root_docs, papers)
        print(f"{slug} days    : {', '.join('%s(%d files)' % (day_label(n), len(p)) for n, _, p in days)}")
        print(f"{slug} root    : {', '.join(root_docs)}")
        print(f"{slug} papers  : {', '.join(papers)}")

    build_home(progress)
    build_nav(per_collection)
    print(f"extra  : {', '.join(extras)}")
    print(f"home   : {DOCS / 'index.md'}")
    print(f"nav    : {MKDOCS_YML}")


if __name__ == "__main__":
    main()
