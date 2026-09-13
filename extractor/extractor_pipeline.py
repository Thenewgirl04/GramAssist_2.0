from pathlib import Path
from extractor.curriculum_llm_extractor import extract_curriculum
from extractor.pdf_extractor import pdf_extractor



markdown_file = pdf_extractor(Path("data/raw/CS-Curriculum.pdf"))

Json_generated = extract_curriculum(markdown_file)

output_path = Path("data/structured/cs_curriculum.json")

output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_text(
    Json_generated.model_dump_json(indent=2)
)

