"""Verify that the packaged VSIX contains the current theme source and assets."""

from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "release" / "nv-green-dark-0.1.1.vsix"
SOURCE_FILES = [ROOT / "package.json", ROOT / "source" / "extension.js", ROOT / "assets" / "extension-icon.png"]
SOURCE_FILES += list((ROOT / "themes").rglob("*"))
SOURCE_FILES = [path for path in SOURCE_FILES if path.is_file()]
EXTRA_FILES = {"extension/readme.md": ROOT / "README.md", "extension/LICENSE.txt": ROOT / "LICENSE"}


def main():
    with ZipFile(PACKAGE) as archive:
        names = set(archive.namelist())
        expected = set(EXTRA_FILES)
        for source in SOURCE_FILES:
            package_name = "extension/" + source.relative_to(ROOT).as_posix()
            expected.add(package_name)
            if package_name not in names:
                raise SystemExit(f"Missing VSIX file: {package_name}")
            if archive.read(package_name) != source.read_bytes():
                raise SystemExit(f"VSIX differs from source: {package_name}")
        for package_name, source in EXTRA_FILES.items():
            if package_name not in names or archive.read(package_name) != source.read_bytes():
                raise SystemExit(f"VSIX differs from source: {package_name}")
        unexpected = [name for name in names if name.startswith("extension/") and not name.endswith("/") and name not in expected]
        if unexpected:
            raise SystemExit(f"Build-only files in VSIX: {unexpected}")
    print(f"Verified {len(SOURCE_FILES) + len(EXTRA_FILES)} source files; VSIX SHA-256 {sha256(PACKAGE.read_bytes()).hexdigest().upper()}")


if __name__ == "__main__":
    main()
