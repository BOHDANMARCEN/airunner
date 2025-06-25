#!/usr/bin/env python
"""Reliable AI Runner autoinstaller."""
import os
import subprocess
import sys
from pathlib import Path


def find_default_path() -> Path:
    """Return D:/AI_Runner if the drive exists, otherwise a path in the home directory."""
    d_drive = Path("D:/")
    if d_drive.exists():
        return d_drive / "AI_Runner"
    return Path.home() / "AI_Runner"


DEFAULT_PATH = find_default_path()


def run(cmd: list[str]) -> None:
    """Run a command list and exit on failure."""
    print(f"[autoinstaller] Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"[autoinstaller] ERROR: {exc}")
        sys.exit(exc.returncode)


class _Paths:
    def __init__(self, base: Path):
        base = base.expanduser()
        self.base_path = base
        self.documents_path = base / "text" / "other" / "documents"
        self.ebook_path = base / "text" / "other" / "ebooks"
        self.image_path = base / "art" / "other" / "images"
        self.llama_index_path = base / "text" / "rag" / "db"
        self.webpages_path = base / "text" / "other" / "webpages"
        self.stt_model_path = base / "text" / "models" / "stt"
        self.tts_model_path = base / "text" / "models" / "tts"


def create_dirs(paths: _Paths) -> None:
    for attr in (
        "base_path",
        "documents_path",
        "ebook_path",
        "image_path",
        "llama_index_path",
        "webpages_path",
        "stt_model_path",
        "tts_model_path",
    ):
        path = getattr(paths, attr)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                print(f"[autoinstaller] Could not create {path}: {exc}")
                sys.exit(1)


def main() -> None:
    env_target = os.environ.get("AIRUNNER_BASE_PATH")
    target = (
        Path(sys.argv[1])
        if len(sys.argv) > 1
        else Path(env_target) if env_target else DEFAULT_PATH
    )
    print(f"[autoinstaller] Installing to {target}")
    try:
        target.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"[autoinstaller] Cannot create {target}: {exc}")
        sys.exit(1)
    os.environ["AIRUNNER_BASE_PATH"] = str(target)

    paths = _Paths(target)
    create_dirs(paths)

    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run([sys.executable, "-m", "pip", "install", ".[all]"])
    run(["airunner-setup"])
    print("[autoinstaller] Installation complete.")


if __name__ == "__main__":
    main()
