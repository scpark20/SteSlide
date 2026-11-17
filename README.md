<p align="center">
  <img src="docs/assets/banner.svg" alt="SteSlide — Markdown in. Slides out." width="100%">
</p>

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square" alt="Python 3.10+"></a>
  <a href="https://github.com/marp-team/marp-cli"><img src="https://img.shields.io/badge/Marp-4.5.1-0284C7?style=flat-square" alt="Marp 4.5.1"></a>
  <img src="https://img.shields.io/badge/Source-Markdown-14B8A6?style=flat-square" alt="Markdown source">
</p>

<p align="center">
  <strong>Edit Markdown. Watch your slides take shape.</strong><br>
  Write with your coding assistant · Preview in your browser · Export to PDF
</p>

<p align="center">
  <a href="docs/usage.md">Getting started</a> ·
  <a href="docs/architecture.md">How it works</a> ·
  <a href="docs/maintenance.md">Updates</a> ·
  <a href="https://github.com/scpark20/SteAgent">SteAgent</a>
</p>

---

## Small files. One presentation.

| Feature | What it does |
| --- | --- |
| **Lecture → Chapter → Section** | Write in small files and preview the complete parent deck. |
| **Live preview** | See Markdown and CSS edits reflected in your browser. |
| **Reusable tooling** | Connect projects through Git submodules and maintain the shared tool in one repository. |

Keep lecture content in your project and the generator and shared theme in SteSlide. Templates start empty.

## Quick start

Requires **Python 3.10+ and Git**. Run these commands at the root of an existing Git project:

```bash
git submodule add -b main https://github.com/scpark20/SteSlide.git tools/steslide
python3 tools/steslide/scripts/setup_marp.py
python3 tools/steslide/steslide.py init
python3 tools/steslide/steslide.py preview
```

Open **[localhost:8766/lecture.md](http://localhost:8766/lecture.md)** and edit `lectures/chapter-01/section-01.md`. To edit through chat, use a coding assistant with access to your project files.

For Remote SSH, VS Code preview, PDF export, and command options, see the [usage guide](docs/usage.md).

## Documentation

- [Usage guide](docs/usage.md) — Installation, preview, and PDF/HTML export
- [Architecture](docs/architecture.md) — File hierarchy, assembly, and change detection
- [Maintenance](docs/maintenance.md) — Shared tool changes, upstream contributions, and project updates

Built with [Marp](https://github.com/marp-team/marp-cli). Used by [SteAgent](https://github.com/scpark20/SteAgent).
