import re
from pathlib import Path
from project_paths import CATALOG_MARKDOWN_PATH


def remove_page_numbers(file_path: Path):
    markdown = file_path.read_text()

    cleaned_markdown = re.sub(
        r"\n[ \t]*\d{1,3}[ \t]*\n",
        "\n",
        markdown
    )

    file_path.write_text(cleaned_markdown)

    print(f"[+] Removed page numbers from {file_path}")


if __name__ == "__main__":
    remove_page_numbers(
        CATALOG_MARKDOWN_PATH
    )
