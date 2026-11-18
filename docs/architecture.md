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
├── tools/steslide/                   # Shared tool submodule
├── code/chapter-01/agent.py          # Runnable source, separate from slides
├── steslide.json                     # Slide configuration
└── lectures/                        # One lecture
    ├── intro.md                     # Editable introduction
    ├── lecture.md                   # Generated full deck
    ├── chapter-01/
    │   ├── intro.md                 # Chapter introduction
        │   ├── section-01.md            # Section content
    │   └── chapter.md               # Generated chapter deck
    └── .build/                      # Browser preview and exports
```

## Assembly rules

Sources are assembled in filename order. Use zero-padded names such as `chapter-01`, `chapter-02`, `section-01.md`, and `section-02.md`.

Empty sources do not add pages. An entirely empty deck displays one blank slide. Separate slides inside Markdown with `---`. Source YAML front matter is removed during assembly; the combined deck uses `steslide.json`. Slide-specific Marp directives such as `<!-- _class: cover -->` remain intact.

To add a chapter, create `chapter-02/intro.md` and its `section-*.md` files. For multiple lectures, use separate subdirectories such as `lectures/lecture-02/` and select one with `--lecture lecture-02`. The default layout uses `lectures/` itself as the single lecture. Existing `lecture-01/` projects remain supported. Add only the content requested by the author.

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

## Include real Python code in slides

Add a directive to a section Markdown file:

```html
<!-- code: @code/chapter-02/agent.py#call_model -->
```

The generator extracts the named function, class, or assignment, including nested node functions, and renders it as a Python code block. Omit `#call_model` to include the whole file. `@code/` resolves inside the separate code directory configured by the `code` setting (default: `code/`). Plain relative paths remain supported inside the section directory. References cannot escape their allowed directory. Python source edits also trigger rebuilds, so slides stay synchronized with runnable code.

Use `<!-- _class: code -->` on code-heavy slides. Edit the Markdown directives and Python source; generated parent decks contain the expanded code for both browser and VS Code previews.
