import os
from llama_cloud import LlamaCloud
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

LLAMA_CLOUD_KEY = os.getenv("LLAMA_CLOUD_API_KEY")

file_path = Path("../data/raw/CS-Curriculum.pdf")

def pdf_extractor(file_path: Path):
    client = LlamaCloud(api_key=LLAMA_CLOUD_KEY)

    # Upload
    file_obj = client.files.create(file=file_path, purpose="parse")

    # Submit + poll + get (parsing.parse wraps create / wait_for_completion / get)
    # Raises on FAILED or CANCELLED. Tune polling_interval=, timeout= if needed.
    result = client.parsing.parse(
        file_id=file_obj.id,
        # The parsing tier. Options: fast, cost_effective, agentic, agentic_plus,
        tier="cost_effective",
        # The version of the parsing tier to use. Use 'latest' for the most recent version,
        version="latest",
        # expand: which fields to materialize (markdown_full, text_full, items, *_content_metadata, ...),
        expand=["markdown_full", "text_full"],
    )

    return result.markdown_full or ""
