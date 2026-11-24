"""构建站点并发布到 gh-pages 分支。

为什么不用 `mkdocs gh-deploy`：它会调 msys 的 sh.exe，在这台机器的 Git Bash 里
`couldn't create signal pipe, Win32 error 5` 崩掉。这里改用纯 git 命令自己推。

用法（先把站点源码改动 commit 掉，再跑）：

    .\\.venv\\Scripts\\python.exe blog\\publish.py

做的事：
    1. mkdocs build --strict（有死链/WARNING 就停，不发布半成品）
    2. 把 site/ 复制到临时目录，补 .nojekyll
    3. 在临时目录 git init 成 gh-pages 单提交，force push 到 origin/gh-pages
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent      # blog/
SITE = HERE / "site"
TMP = HERE / ".publish"


def run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> None:
    print("$", " ".join(args))
    subprocess.run(args, cwd=str(cwd), check=True, env=env)


def main() -> None:
    py = sys.executable

    # 1) 构建（strict：死链、找不到的图片都会让构建失败）
    run([py, "-m", "mkdocs", "build", "--strict", "--clean"], HERE)
    if not (SITE / "index.html").exists():
        raise SystemExit("构建后没有 site/index.html，检查 mkdocs.yml")

    # 2) 拷到临时目录
    if TMP.exists():
        shutil.rmtree(TMP)
    shutil.copytree(SITE, TMP)
    (TMP / ".nojekyll").write_text("", encoding="utf-8")

    # 3) 推 gh-pages
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=str(HERE), capture_output=True, text=True, check=True,
    ).stdout.strip()

    # 沙箱里 git 走 ssh wrapper（外面普通终端不需要，有 GIT_SSH 就透传）
    env = dict(os.environ)

    run(["git", "init", "-b", "gh-pages"], TMP, env)
    run(["git", "add", "-A"], TMP, env)
    run(["git", "-c", "user.name=site-bot", "-c", "user.email=site-bot@users.noreply.github.com",
         "commit", "-m", "deploy: 构建产物"], TMP, env)
    run(["git", "remote", "add", "origin", remote], TMP, env)
    run(["git", "push", "--force", "origin", "gh-pages"], TMP, env)

    shutil.rmtree(TMP)
    print(f"\n已发布：{remote} 的 gh-pages 分支")


if __name__ == "__main__":
    main()
