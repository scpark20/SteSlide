# Usage guide

[← SteSlide](../README.md) · [Architecture](architecture.md) · [Maintenance](maintenance.md)

## Install in a project

Requires Python 3.10+ and Git. From your project's Git repository root:

```bash
git submodule add -b main https://github.com/scpark20/SteSlide.git tools/steslide
python3 tools/steslide/scripts/setup_marp.py
python3 tools/steslide/steslide.py init
python3 tools/steslide/steslide.py preview
```

Open <http://localhost:8766/lecture.md>. Saving a source file updates the presentation. Press `Ctrl+C` to stop.

The installer downloads the official standalone Marp CLI 4.5.1 and verifies its SHA-256 checksum. No separate Node.js installation or Python packages are required. The installer selects an official release for Linux x64/ARM64, macOS, or Windows x64; runtime verification has been performed on Linux x64.

If Marp is already installed, skip the installer. Executable resolution is: `STESLIDE_MARP` environment variable → SteSlide's `.tools/marp/` directory → `marp` on PATH.

## Clone an existing project

```bash
git clone --recurse-submodules <project-repository-url>
cd <project-directory>
python3 tools/steslide/scripts/setup_marp.py
python3 tools/steslide/steslide.py preview
```

After a regular clone, initialize the submodule with `git submodule update --init --recursive`.

## Commands

Run from the consuming project's root:

```bash
# Assemble once; Marp is not required
python3 tools/steslide/steslide.py build

# Keep parent Markdown decks updated for VS Code
python3 tools/steslide/steslide.py watch

# Start the browser preview
python3 tools/steslide/steslide.py preview --lecture lecture-01 --port 8766

# Export
python3 tools/steslide/steslide.py export --format html
python3 tools/steslide/steslide.py export --format pdf
```

Exports default to `lectures/.build/lecture-01/lecture.html` or `lecture.pdf`. Change the destination with `--output <path>`.

PDF export requires Chrome, Edge, or Firefox. If detection fails, specify a browser explicitly with `--browser firefox --browser-path /path/to/firefox`.

To run from another working directory, place `--project` before the command:

```bash
python3 /path/to/steslide.py --project /path/to/project preview
```

`init` creates missing source and configuration files without replacing existing sources or VS Code settings. If `.vscode/settings.json` already exists, merge the theme configuration below manually.

## VS Code and Remote SSH

Install [Marp for VS Code](https://github.com/marp-team/marp-vscode). Keep `watch` or `preview` running, open `lecture.md` or `chapter.md`, and run **Markdown: Open Preview to the Side**. The parent deck includes its child files.

Shortcut: `Cmd+K`, then `V` on macOS; `Ctrl+K`, then `V` on Windows/Linux.

```json
{
  "markdown.marp.themes": ["tools/steslide/theme.css"],
  "remote.portsAttributes": {
    "8766": {"label": "SteSlide", "onAutoForward": "openBrowser"}
  }
}
```

For Remote SSH, forward remote port `8766` from VS Code's **Ports** panel, then open the local browser URL. If the port is occupied, use `--port 8767` and forward that port instead.

Browser routes: `/lecture.md` for the full lecture and `/chapter-01.md` for an individual chapter.
