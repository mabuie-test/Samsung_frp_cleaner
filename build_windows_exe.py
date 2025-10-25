"""Utilitário para gerar o executável Windows do FRP Cleaner via PyInstaller.

O script lê a versão a partir do pacote :mod:`cleaner` para que o executável e o
instalador mantenham o mesmo identificador semântico.
"""

from __future__ import annotations

import re
from pathlib import Path
import sys
from textwrap import dedent

try:
    import PyInstaller.__main__
except ImportError:  # pragma: no cover - feedback direto ao utilizador
    sys.stderr.write(
        "PyInstaller não está instalado. Execute 'pip install pyinstaller' no seu ambiente.\n"
    )
    raise


def main() -> None:
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    entry_point = project_root / "frp_cleaner" / "main.py"

    if not entry_point.exists():
        raise SystemExit(f"Entrada principal não encontrada: {entry_point}")

    try:
        from cleaner import __version__ as version
    except Exception as exc:  # pragma: no cover - protegemos feedback ao utilizador
        raise SystemExit(f"Não foi possível obter a versão do pacote: {exc}")

    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    dist_dir.mkdir(exist_ok=True)
    build_dir.mkdir(exist_ok=True)

    version_file = _write_temp_version_file(dist_dir, version)
    PyInstaller.__main__.run(
        [
            str(entry_point),
            "--name",
            "FRP-Cleaner",
            "--onefile",
            "--clean",
            "--distpath",
            str(dist_dir),
            "--workpath",
            str(build_dir),
            "--version-file",
            str(version_file),
        ]
    )


def _write_temp_version_file(dist_dir: Path, version: str) -> Path:
    """Gera o ficheiro de metadados consumido pelo PyInstaller."""

    cleaned_parts = []
    for chunk in re.split(r"[.-]", version):
        match = re.match(r"(\d+)", chunk)
        if match:
            cleaned_parts.append(int(match.group(1)))

    parts = cleaned_parts or [0]
    while len(parts) < 4:
        parts.append(0)
    major, minor, patch, build = parts[:4]

    content = dedent(
        f"""\
        # UTF-8\n\
        VSVersionInfo(\n\
          ffi=FixedFileInfo(\n\
            filevers=({major}, {minor}, {patch}, {build}),\n\
            prodvers=({major}, {minor}, {patch}, {build}),\n\
            mask=0x3f,\n\
            flags=0x0,\n\
            OS=0x40004,\n\
            fileType=0x1,\n\
            subtype=0x0,\n\
            date=(0, 0)\n\
          ),\n\
          kids=[\n\
            StringFileInfo([\n\
              StringTable(\"040904b0\", [\n\
                StringStruct(\"CompanyName\", \"Mestre Jorge Augusto Mabuie\"),\n\
                StringStruct(\"FileDescription\", \"FRP Cleaner Samsung\"),\n\
                StringStruct(\"FileVersion\", \"{version}\"),\n\
                StringStruct(\"InternalName\", \"FRP-Cleaner\"),\n\
                StringStruct(\"OriginalFilename\", \"FRP-Cleaner.exe\"),\n\
                StringStruct(\"ProductName\", \"FRP Cleaner Samsung\"),\n\
                StringStruct(\"ProductVersion\", \"{version}\"),\n\
              ])\n\
            ]),\n\
            VarFileInfo([VarStruct(\"Translation\", [0x0409, 1200])])\n\
          ]\n\
        )\n\
        """
    ).strip()

    version_file = dist_dir / "version_info.txt"
    version_file.write_text(content, encoding="utf-8")
    return version_file


if __name__ == "__main__":
    main()
