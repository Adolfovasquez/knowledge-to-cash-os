# scripts/convert_to_md.py

```python
from __future__ import annotations

import argparse
import re
from pathlib import Path


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def extract_title(source: Path, content: str) -> str:
    first_line = next((line.strip() for line in content.splitlines() if line.strip()), "")
    if first_line and len(first_line) <= 120:
        return first_line
    return source.stem.replace("_", " ").replace("-", " ").title()


def to_markdown(source: Path, content: str) -> str:
    title = extract_title(source, content)
    body = clean_text(content)
    return (
        f"---\n"
        f"title: {title}\n"
        f"source: {source.name}\n"
        f"type: fuente\n"
        f"---\n\n"
        f"# {title}\n\n"
        f"{body}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert plain text documents to Markdown.")
    parser.add_argument("input", help="Path to the source text file.")
    parser.add_argument("-o", "--output", help="Path to the output .md file.")
    args = parser.parse_args()

    source = Path(args.input)
    if not source.exists():
        raise FileNotFoundError(f"Input file not found: {source}")

    content = source.read_text(encoding="utf-8", errors="ignore")
    markdown = to_markdown(source, content)

    output = Path(args.output) if args.output else source.with_suffix(".md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")

    print(f"Markdown created: {output}")


if __name__ == "__main__":
    main()
```

# scripts/ingest_docs.py

```python
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from convert_to_md import to_markdown

SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".html", ".htm"}


def ensure_dirs(vault: Path) -> None:
    for folder in [
        "00_inbox",
        "01_fuentes",
        "02_notas",
        "03_prompts",
        "04_plantillas",
        "05_productos",
        "06_clientes",
        "07_automatizaciones",
        "08_publicacion",
        "assets",
    ]:
        (vault / folder).mkdir(parents=True, exist_ok=True)


def ingest_file(source: Path, vault: Path) -> Path:
    target_dir = vault / "01_fuentes"
    target_dir.mkdir(parents=True, exist_ok=True)

    if source.suffix.lower() == ".md":
        destination = target_dir / source.name
        shutil.copy2(source, destination)
        return destination

    content = source.read_text(encoding="utf-8", errors="ignore")
    markdown = to_markdown(source, content)
    destination = target_dir / f"{source.stem}.md"
    destination.write_text(markdown, encoding="utf-8")
    return destination


def ingest_path(input_path: Path, vault: Path) -> list[Path]:
    created: list[Path] = []

    if input_path.is_file():
        if input_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            created.append(ingest_file(input_path, vault))
        return created

    for file_path in input_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            created.append(ingest_file(file_path, vault))

    return created


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into the Knowledge-to-Cash vault.")
    parser.add_argument("input", help="File or folder to ingest.")
    parser.add_argument(
        "--vault",
        default="vault",
        help="Vault root folder (default: vault).",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    vault = Path(args.vault)

    if not input_path.exists():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    ensure_dirs(vault)
    created = ingest_path(input_path, vault)

    if not created:
        print("No supported documents were found.")
        return

    print("Ingest completed:")
    for path in created:
        print(f"- {path}")


if __name__ == "__main__":
    main()
```

## Notes

* `convert_to_md.py` funciona bien para textos simples y como base inicial.
* `ingest_docs.py` deja los archivos en `vault/01_fuentes/` y crea la estructura mínima si aún no existe.
* En una siguiente iteración conviene añadir soporte para PDF, DOCX, HTML enriquecido y una capa de indexación.
