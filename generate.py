# generate.py
from __future__ import annotations

import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).parent
PROFILE_PATH = ROOT / "profile.json"
TEMPLATES_DIR = ROOT / "templates"
DIST_DIR = ROOT / "dist"
OUTPUT_README = DIST_DIR / "README.md"


def load_profile(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing profile file: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    # Minimal defaults to avoid template errors
    data.setdefault("name", "Your Name")
    data.setdefault("headline", "")
    data.setdefault("summary", "")
    data.setdefault("location", "")
    data.setdefault("email", "")
    data.setdefault("links", [])
    data.setdefault("skills", [])
    data.setdefault("projects", [])
    return data


def render_readme(profile: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(enabled_extensions=()),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("README.md.j2")
    return template.render(**profile).strip() + "\n"


def main() -> None:
    profile = load_profile(PROFILE_PATH)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    content = render_readme(profile)
    OUTPUT_README.write_text(content, encoding="utf-8")
    print(f"Generated: {OUTPUT_README}")


if __name__ == "__main__":
    main()
