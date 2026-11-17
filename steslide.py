#!/usr/bin/env python3
"""Reusable Markdown → Lecture/Chapter → Marp live preview."""

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time

TOOL = Path(__file__).resolve().parent
DEFAULTS = {"lectures": "lectures", "theme": "steslide", "size": "16:9",
            "paginate": False, "math": "katex"}


def settings(project):
    path = project / "steslide.json"
    config = DEFAULTS | (json.loads(path.read_text(encoding="utf-8")) if path.exists() else {})
    root = (project / config["lectures"]).resolve()
    if not root.is_relative_to(project):
        raise ValueError("lectures must be inside the project")
    theme = (project / config["theme_file"]).resolve() if config.get("theme_file") else TOOL / "theme.css"
    if not theme.is_file():
        raise ValueError(f"Theme not found: {theme}")
    return config, root, theme


def lecture_path(root, name):
    path = root / name
    if Path(name).name != name or not path.is_dir():
        raise ValueError(f"Lecture not found: {name}")
    return path


def chapters(lecture):
    return sorted(path for path in lecture.glob("chapter-*") if path.is_dir())


def source_files(lecture):
    files = [lecture / "intro.md"]
    for chapter in chapters(lecture):
        files.append(chapter / "intro.md")
        files.extend(sorted(chapter.glob("section-*.md")))
    return files


def body(path):
    if not path.exists() and path.name == "intro.md":
        return ""
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return "".join(lines[index + 1:]).strip()
        raise ValueError(f"Unclosed YAML front matter: {path}")
    return text.strip()


def deck(parts, config):
    header = ["---", "marp: true"]
    for key in ("theme", "size", "paginate", "math"):
        header.append(f"{key}: {json.dumps(config[key], ensure_ascii=False)}")
    header += ["# Generated: edit intro.md / section-*.md and steslide.json.", "---"]
    return "\n".join(header) + "\n\n" + "\n\n---\n\n".join(part for part in parts if part.strip()) + "\n"


def write_changed(path, content):
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)


def build(project, name):
    config, root, _ = settings(project)
    lecture = lecture_path(root, name)
    output = root / ".build" / name
    parts = [body(lecture / "intro.md")]
    pending = {}
    expected = set()
    for chapter in chapters(lecture):
        contents = [body(chapter / "intro.md")]
        contents += [body(path) for path in sorted(chapter.glob("section-*.md"))]
        text = deck(contents, config)
        pending[chapter / "chapter.md"] = text
        target = output / f"{chapter.name}.md"
        pending[target] = text
        expected.add(target)
        parts.extend(contents)
    text = deck(parts, config)
    pending[lecture / "lecture.md"] = text
    pending[output / "lecture.md"] = text
    # Parse all sources before changing any generated file.
    for path, content in pending.items():
        write_changed(path, content)
    for stale in output.glob("chapter-*.md"):
        if stale not in expected:
            stale.unlink()
    return output / "lecture.md"


def signature(project, name):
    _, root, theme = settings(project)
    paths = [project / "steslide.json", theme, *source_files(lecture_path(root, name))]
    result = []
    for path in paths:
        stat = path.stat() if path.exists() else None
        result.append((str(path), stat.st_mtime_ns if stat else None, stat.st_size if stat else None))
    return tuple(result)


def marp_executable():
    configured = os.environ.get("STESLIDE_MARP")
    bundled = TOOL / ".tools" / "marp" / ("marp.exe" if os.name == "nt" else "marp")
    candidate = configured or (str(bundled) if bundled.is_file() else shutil.which("marp"))
    executable = shutil.which(candidate) if candidate else None
    if not executable:
        raise ValueError(f"Install Marp: python3 {TOOL / 'scripts/setup_marp.py'} (or set STESLIDE_MARP)")
    return executable


def initialize(project):
    project.mkdir(parents=True, exist_ok=True)
    config_file = project / "steslide.json"
    if not config_file.exists():
        write_changed(config_file, json.dumps(DEFAULTS, ensure_ascii=False, indent=2) + "\n")
    config, root, theme = settings(project)
    for source in (TOOL / "templates").rglob("*.md"):
        target = root / source.relative_to(TOOL / "templates")
        if not target.exists():
            write_changed(target, deck([], config).replace("# Generated: edit intro.md / section-*.md and steslide.json.\n", ""))
    relative_root = root.relative_to(project).as_posix()
    ignored = ["__pycache__/", "*.py[cod]", f"/{relative_root}/.build/",
               f"/{relative_root}/lecture-*/lecture.md",
               f"/{relative_root}/lecture-*/chapter-*/chapter.md"]
    ignore_file = project / ".gitignore"
    current = ignore_file.read_text(encoding="utf-8") if ignore_file.exists() else ""
    missing = [line for line in ignored if line not in current.splitlines()]
    if missing:
        write_changed(ignore_file, current.rstrip() + "\n\n# SteSlide generated files\n" + "\n".join(missing) + "\n")
    vscode = project / ".vscode"
    for filename, defaults in {
        "settings.json": {"markdown.marp.themes": [os.path.relpath(theme, project).replace(os.sep, "/")],
                          "remote.portsAttributes": {"8766": {"label": "SteSlide", "onAutoForward": "openBrowser"}}},
        "extensions.json": {"recommendations": ["marp-team.marp-vscode"]},
    }.items():
        target = vscode / filename
        if not target.exists():
            write_changed(target, json.dumps(defaults, indent=2) + "\n")
    build(project, "lecture-01")
    print(f"Initialized blank slides in {root}. Existing sources and VS Code settings were preserved.")


def stop_process(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def interrupt(*_):
    raise KeyboardInterrupt


def watch(project, name, port, serve):
    output = build(project, name)
    previous = signature(project, name)
    process = None
    active_theme = None
    old_handler = signal.signal(signal.SIGTERM, interrupt)
    try:
        while True:
            try:
                current = signature(project, name)
                if current != previous:
                    output = build(project, name)
                    previous = current
                    print(f"Rebuilt {name}", flush=True)
                _, _, theme = settings(project)
                if serve and (process is None or theme != active_theme):
                    if process:
                        stop_process(process)
                    process = subprocess.Popen(
                        [marp_executable(), "--no-config-file", "--server", str(output.parent),
                         "--html", "--theme-set", str(theme)], env=dict(os.environ, PORT=str(port)))
                    active_theme = theme
                    print(f"Preview: http://localhost:{port}/lecture.md", flush=True)
                if process is not None and process.poll() is not None:
                    return process.returncode
            except (OSError, ValueError) as error:
                if process is None and serve:
                    raise
                print(f"Waiting for a valid source edit: {error}", file=sys.stderr, flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        return 0
    finally:
        if process:
            stop_process(process)
        signal.signal(signal.SIGTERM, old_handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Consumer project root (default: cwd)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Create blank sources; preserve existing source files")
    for command in ("build", "watch", "preview", "export"):
        sub = commands.add_parser(command)
        sub.add_argument("--lecture", default="lecture-01")
        if command == "preview":
            sub.add_argument("--port", type=int, default=8766)
        if command == "export":
            sub.add_argument("--format", choices=("html", "pdf"), default="pdf")
            sub.add_argument("--output", type=Path)
            sub.add_argument("--browser", choices=("auto", "chrome", "edge", "firefox"), default="auto")
            sub.add_argument("--browser-path")
    args = parser.parse_args()
    project = args.project.resolve()
    try:
        if args.command == "init":
            initialize(project)
        elif args.command == "build":
            print(build(project, args.lecture))
        elif args.command in ("watch", "preview"):
            return watch(project, args.lecture, getattr(args, "port", None), args.command == "preview")
        else:
            source = build(project, args.lecture)
            _, _, theme = settings(project)
            output = args.output or source.with_suffix("." + args.format)
            output.parent.mkdir(parents=True, exist_ok=True)
            command = [marp_executable(), "--no-config-file", str(source), "--html", "--theme-set", str(theme),
                       "--output", str(output.resolve())]
            if args.format == "pdf":
                command += ["--pdf", "--browser", args.browser]
                if args.browser_path:
                    command += ["--browser-path", args.browser_path]
            subprocess.run(command, check=True)
            print(output)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"SteSlide: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
