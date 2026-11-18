import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("steslide", Path(__file__).resolve().parents[1] / "steslide.py")
slides = importlib.util.module_from_spec(spec)
spec.loader.exec_module(slides)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve()
        slides.initialize(self.project)
        self.lecture = self.project / "lectures"
        self.chapter = self.lecture / "chapter-01"

    def test_blank_template_has_no_content(self):
        output = slides.build(self.project)
        self.assertEqual(slides.body(output), "")
        for source in slides.source_files(self.lecture):
            self.assertEqual(slides.body(source), "")

    def test_parent_order_and_code_block_are_preserved(self):
        (self.lecture / "intro.md").write_text("# Lecture", encoding="utf-8")
        (self.chapter / "intro.md").write_text("# Chapter", encoding="utf-8")
        (self.chapter / "section-02.md").write_text("# Second", encoding="utf-8")
        code = '# First\n\n```python\nprint("---")\n```'
        (self.chapter / "section-01.md").write_text("---\nmarp: true\n---\n" + code, encoding="utf-8")
        output = slides.build(self.project)
        self.assertEqual(slides.body(output), "\n\n---\n\n".join(["# Lecture", "# Chapter", code, "# Second"]))
        self.assertEqual(slides.body(self.chapter / "chapter.md"), "\n\n---\n\n".join(["# Chapter", code, "# Second"]))

    def test_empty_intro_does_not_add_slides(self):
        (self.chapter / "section-01.md").write_text("# Only slide", encoding="utf-8")
        self.assertEqual(slides.body(slides.build(self.project)), "# Only slide")

    def test_invalid_edit_preserves_all_generated_outputs(self):
        output = slides.build(self.project)
        before = output.read_bytes()
        chapter_before = (self.chapter / "chapter.md").read_bytes()
        (self.chapter / "section-01.md").write_text("---\nmarp: true\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unclosed"):
            slides.build(self.project)
        self.assertEqual(output.read_bytes(), before)
        self.assertEqual((self.chapter / "chapter.md").read_bytes(), chapter_before)

    def test_unchanged_build_does_not_trigger_reload(self):
        output = slides.build(self.project)
        timestamp = output.stat().st_mtime_ns
        slides.build(self.project)
        self.assertEqual(output.stat().st_mtime_ns, timestamp)

    def test_deleted_chapter_is_removed_from_preview(self):
        output = slides.build(self.project)
        shutil.rmtree(self.chapter)
        slides.build(self.project)
        self.assertFalse((output.parent / "chapter-01.md").exists())

    def test_watch_signature_detects_added_and_deleted_sources(self):
        before = slides.signature(self.project)
        extra = self.chapter / "section-02.md"
        extra.write_text("# Added", encoding="utf-8")
        self.assertNotEqual(slides.signature(self.project), before)
        extra.unlink()
        self.assertEqual(slides.signature(self.project), before)

    def test_init_preserves_existing_sources_and_vscode_settings(self):
        source = self.chapter / "section-01.md"
        source.write_text("# User content", encoding="utf-8")
        settings = self.project / ".vscode/settings.json"
        settings.write_text('{"user": true}', encoding="utf-8")
        slides.initialize(self.project)
        self.assertEqual(source.read_text(), "# User content")
        self.assertEqual(settings.read_text(), '{"user": true}')

    def test_lecture_path_cannot_escape_root(self):
        with self.assertRaises(ValueError):
            slides.build(self.project, "../outside")

    def test_python_source_is_included_and_watched(self):
        source = self.chapter / "agent.py"
        source.write_text('def hello():\n    return "Hello"\n', encoding="utf-8")
        (self.chapter / "section-01.md").write_text('<!-- code: agent.py#hello -->', encoding="utf-8")
        before = slides.signature(self.project)
        self.assertIn('return "Hello"', slides.build(self.project).read_text())
        source.write_text('def hello():\n    return "Updated"\n', encoding="utf-8")
        self.assertNotEqual(before, slides.signature(self.project))
        self.assertIn('return "Updated"', slides.build(self.project).read_text())

    def test_code_include_cannot_escape_chapter(self):
        (self.chapter / "section-01.md").write_text('<!-- code: ../secret.py -->', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inside"):
            slides.build(self.project)

    def test_nested_node_and_tool_schema_can_be_included(self):
        (self.chapter / "agent.py").write_text('TOOLS = [{"type": "function"}]\ndef graph():\n    def assistant():\n        return 42\n', encoding="utf-8")
        (self.chapter / "section-01.md").write_text('<!-- code: agent.py#TOOLS -->\n<!-- code: agent.py#assistant -->', encoding="utf-8")
        content = slides.build(self.project).read_text()
        self.assertIn('TOOLS = [{"type": "function"}]', content)
        self.assertIn('```python\ndef assistant():\n    return 42', content)

    def test_explicit_multiple_lecture_layout_still_works(self):
        nested = self.lecture / "lecture-02"
        nested.mkdir()
        (nested / "intro.md").write_text('# Another lecture', encoding="utf-8")
        output = slides.build(self.project, "lecture-02")
        self.assertEqual(slides.body(output), '# Another lecture')

    def test_separate_code_directory_is_included_and_watched(self):
        folder = self.project / "code/chapter-01"
        folder.mkdir(parents=True)
        source = folder / "agent.py"
        source.write_text('def hello():\n    return 1\n', encoding="utf-8")
        (self.chapter / "section-01.md").write_text('<!-- code: @code/chapter-01/agent.py#hello -->', encoding="utf-8")
        before = slides.signature(self.project)
        self.assertIn('return 1', slides.build(self.project).read_text())
        source.write_text('def hello():\n    return 22\n', encoding="utf-8")
        self.assertNotEqual(before, slides.signature(self.project))
        self.assertIn('return 22', slides.build(self.project).read_text())
        (self.chapter / "section-01.md").write_text('<!-- code: @code/../secret.py -->', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inside"):
            slides.build(self.project)


if __name__ == "__main__":
    unittest.main()
