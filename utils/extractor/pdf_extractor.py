import os
from llama_cloud import LlamaCloud
from dotenv import load_dotenv
from pathlib import Path
from project_paths import CURRICULUM_PDF_PATH

load_dotenv()

LLAMA_CLOUD_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

file_path = CURRICULUM_PDF_PATH

def pdf_extractor(file_path: Path):
    client = LlamaCloud(api_key=LLAMA_CLOUD_KEY)


    file_obj = client.files.create(file=file_path, purpose="parse")

    result = client.parsing.parse(
        file_id=file_obj.id,
        tier="cost_effective",
        version="latest",
        expand=["markdown_full", "text_full"],
    )

    return result.markdown_full or ""
