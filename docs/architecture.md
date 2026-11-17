# Architecture

[← SteSlide](../README.md) · [Usage guide](usage.md) · [Maintenance](maintenance.md)

## Editing to preview

```text
Chat request or manual edit
        ↓
intro.md / section-*.md / theme.css
        ↓ change detection
Generated chapter.md and lecture.md
        ↓
Marp → live browser preview
```

A coding assistant must have access to the project files to edit them through chat. SteSlide assembles Markdown; it does not execute Python agent code or automatically embed `.py` files.

```text
project/
├── tools/steslide/                   # Git submodule: shared tool
├── steslide.json                     # Project slide configuration
└── lectures/
    ├── lecture-01/
    │   ├── intro.md                  # Editable lecture introduction
    │   ├── lecture.md                # Generated: all chapters
    │   └── chapter-01/
    │       ├── intro.md              # Editable chapter introduction
    │       ├── section-01.md         # Editable section content
    │       └── chapter.md            # Generated: all sections
    └── .build/lecture-01/            # Browser preview and exports
```

## Assembly rules

Sources are assembled in filename order. Use zero-padded names such as `chapter-01`, `chapter-02`, `section-01.md`, and `section-02.md`.

Empty sources do not add pages. An entirely empty deck displays one blank slide. Separate slides inside Markdown with `---`. Source YAML front matter is removed during assembly; the combined deck uses `steslide.json`. Slide-specific Marp directives such as `<!-- _class: cover -->` remain intact.

To add a chapter, create `chapter-02/intro.md` and its `section-*.md` files. To add a lecture, create `lecture-02/intro.md` and select it with `--lecture lecture-02`. Add only the content requested by the author.

## Generation and watching

`steslide.py` uses the Python standard library. It reads and parses all sources before replacing generated files. Changed files are written through temporary files. If a source has invalid front matter, the previous generated deck remains available.

`watch` and `preview` inspect source, configuration, and theme changes every 0.5 seconds. Newly added sections and deleted chapters are reflected in the next build. `preview` also starts Marp's server, which handles browser reloads. The child server is stopped when the command exits.

## Configuration and ownership

| Location | Purpose | Repository |
| --- | --- | --- |
| `intro.md`, `section-*.md` | Lecture source | Consuming project |
| `steslide.json` | Theme, slide size, pagination, and math settings | Consuming project |
| `steslide.py`, `theme.css` | Shared generator and theme | SteSlide |
| `lecture.md`, `chapter.md`, `.build/` | Generated previews | Excluded from Git |

Combined decks use global settings from `steslide.json`. A source file previewed individually uses its own YAML front matter. Keep these settings aligned when using both preview paths.

For a project-specific theme, add a CSS file to the consuming project and set `theme_file` to its relative path in `steslide.json`. Set `theme` to the CSS `@theme` name and update the VS Code theme path accordingly.
