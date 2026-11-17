# Working on SteSlide

- Keep this repository focused on reusable slide tooling and blank templates.
- Store lecture content in the consuming project's `lectures/` directory. Add only content requested by the user; do not invent lectures or outlines.
- Write all published documentation, comments, CLI help, and other repository text in English.
- Treat `lecture.md`, `chapter.md`, and `.build/` as generated output. Edit `intro.md` and `section-*.md` instead.
- Make shared generator, theme, and installer changes in SteSlide. Do not copy the tool or create a competing implementation inside the consuming project.
- When working through a submodule, inspect its Git status and branch first. When publication is requested, commit and push SteSlide changes before recording the new submodule version in the consuming project. Preserve unrelated changes.
- After generator changes, run `python3 -m unittest discover -s tests -v`. Verify browser reloads when preview behavior changes.
