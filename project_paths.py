"""Absolute paths for GramAssist resources.

Keeping paths here makes the application independent of the directory from
which a command is launched.
"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
STRUCTURED_DATA_DIR = DATA_DIR / "structured"
MOCK_DATA_DIR = DATA_DIR / "mock"
FAISS_DIR = DATA_DIR / "faiss"

SYSTEM_PROMPT_PATH = PROJECT_ROOT / "prompts" / "advisor_agent_system_prompt.txt"
CATALOG_MARKDOWN_PATH = RAW_DATA_DIR / "GSU Catalog 2024-2026 cleaned.md"
CATALOG_INDEX_PATH = FAISS_DIR / "catalog"
CURRICULUM_PDF_PATH = RAW_DATA_DIR / "CS-Curriculum.pdf"
CURRICULUM_JSON_PATH = STRUCTURED_DATA_DIR / "cs_curriculum.json"
STUDENTS_PATH = MOCK_DATA_DIR / "students.json"
PROFESSORS_PATH = MOCK_DATA_DIR / "professors.json"
