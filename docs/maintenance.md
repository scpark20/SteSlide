# Maintenance and updates

[← SteSlide](../README.md) · [Usage guide](usage.md) · [Architecture](architecture.md)

## Send shared tool changes to SteSlide

`tools/steslide` is a separate Git repository. Commit generator, shared theme, and installer changes there and push them to SteSlide. Fresh submodule checkouts may be detached at a pinned commit; switch to `main` before editing.

```bash
git -C tools/steslide switch main
git -C tools/steslide pull --ff-only origin main
# Edit the relevant files inside tools/steslide
python3 -m unittest discover -s tools/steslide/tests -v
git -C tools/steslide add <changed-files>
git -C tools/steslide commit -m "Describe the tool change"
git -C tools/steslide push origin main

# Record the updated tool version in the consuming project
git add tools/steslide
git commit -m "Update SteSlide version"
git push
```

Lecture edits belong in the consuming project's `lectures/` directory. Keep repository documentation, comments, CLI help, and other published text in English.

## Receive SteSlide updates

Run with no uncommitted changes inside the submodule:

```bash
git submodule update --init --remote --merge tools/steslide
git add tools/steslide
git commit -m "Update SteSlide version"
git push
```

Restart the preview to load updated Python code. To receive the tool version pinned by another contributor, run `git pull --recurse-submodules`, then `git submodule update --init --recursive`. Rerun `setup_marp.py` if an update changes the Marp version.

Saving a file does not push to GitHub automatically. Shared tool changes are committed to SteSlide; the tool version and lecture content are committed to the consuming project.

## Work on the tool directly

```bash
git clone https://github.com/scpark20/SteSlide.git
cd SteSlide
python3 -m unittest discover -s tests -v
```

The runtime consists of Python's standard library and Marp CLI. Blank sources live in `templates/`, the shared style in `theme.css`, and assembly/watch logic in `steslide.py`.
