from pathlib import Path
from utils.extractor.curriculum_llm_extractor import extract_curriculum
from utils.extractor.pdf_extractor import pdf_extractor

input_path = Path("data/raw/CS-Curriculum.pdf")
output_path = Path("data/structured/cs_curriculum.json")

def pipeline(input_path):
    markdown_file = pdf_extractor(input_path)
    json_generated = extract_curriculum(markdown_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json_generated.model_dump_json(indent=2) )
    return json_generated


