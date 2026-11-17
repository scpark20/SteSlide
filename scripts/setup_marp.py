#!/usr/bin/env python3
"""Install the official standalone Marp CLI; no Node.js installation needed."""

import hashlib
import io
import os
from pathlib import Path
import platform
import tarfile
import urllib.request
import zipfile

VERSION = "4.5.1"
CHECKSUMS = {
    "linux": "2fc36a8799450d28fe0c91194c1bc690d487051eae4b81b239b741a7a9a4b7da",
    "linux-arm64": "a360f1e37fce442ee7aa0d0e0a2f86cc239d9f431861c7f5469ccdc78ffe5fc7",
    "mac": "c012c91e2e6b130c8352522631b1597f156547a1dc961f5ce121839cf003f4b7",
    "win": "34f3eac66899c5d715bcd82248c6ceb063fa60c523931f15c4aa1e03e909cafa",
}


def main():
    system, machine = platform.system(), platform.machine().lower()
    if system == "Linux" and machine in ("x86_64", "amd64", "aarch64", "arm64"):
        target = "linux-arm64" if machine in ("aarch64", "arm64") else "linux"
    elif system == "Darwin" and machine in ("x86_64", "arm64"):
        target = "mac"
    elif system == "Windows" and machine in ("amd64", "x86_64"):
        target = "win"
    else:
        raise SystemExit(f"Unsupported platform: {system}/{machine}. Install Marp separately and set STESLIDE_MARP.")
    suffix = "zip" if target == "win" else "tar.gz"
    asset = f"marp-cli-v{VERSION}-{target}.{suffix}"
    url = f"https://github.com/marp-team/marp-cli/releases/download/v{VERSION}/{asset}"
    print(f"Downloading {url}", flush=True)
    request = urllib.request.Request(url, headers={"User-Agent": "SteSlide"})
    with urllib.request.urlopen(request, timeout=120) as response:
        archive = response.read()
    if hashlib.sha256(archive).hexdigest() != CHECKSUMS[target]:
        raise SystemExit("Marp download failed SHA-256 verification")
    name = "marp.exe" if target == "win" else "marp"
    if suffix == "zip":
        with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
            member = next(item for item in bundle.namelist() if Path(item).name == name)
            executable = bundle.read(member)
    else:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
            member = next(item for item in bundle.getmembers() if item.isfile() and Path(item.name).name == name)
            executable = bundle.extractfile(member).read()
    destination = Path(__file__).resolve().parents[1] / ".tools" / "marp" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp")
    temporary.write_bytes(executable)
    if os.name != "nt":
        temporary.chmod(0o755)
    temporary.replace(destination)
    print(f"Installed verified Marp CLI {VERSION}: {destination}")


if __name__ == "__main__":
    main()
