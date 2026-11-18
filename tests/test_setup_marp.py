import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("setup_marp", Path(__file__).resolve().parents[1] / "scripts/setup_marp.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_intel_mac_does_not_download_an_arm_binary(self):
        with patch.object(installer.platform, "system", return_value="Darwin"):
            with patch.object(installer.platform, "machine", return_value="x86_64"):
                with patch.object(installer.urllib.request, "urlopen") as download:
                    with self.assertRaisesRegex(SystemExit, "npm install"):
                        installer.main()
                    download.assert_not_called()
