"""
Strategy: Pure Semantic Chunking

Chunks: 161
Average size: 3,580 chars
Minimum: 2 chars
Maximum: 32,313 chars

Observed issues:
- Extremely inconsistent chunk sizes
- Very small fragment chunks
- Very large chunks containing multiple topics
- Lost document heading metadata
- Existing Markdown structure is not being exploited
"""

from pathlib import Path
import json

from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

markdown = Path(
    "data/raw/GSU Catalog 2024-2026 cleaned.md"
).read_text()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

semantic_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
)

chunks = semantic_splitter.create_documents([markdown])

lengths = [len(chunk.page_content) for chunk in chunks]

print("Final chunks:", len(chunks))
print("Minimum characters:", min(lengths))
print("Maximum characters:", max(lengths))
print("Average characters:", sum(lengths) / len(lengths))

search_terms = [
    "TRANSFER CREDITS",
    "ACADEMIC PROBATION",
    "REPEATING COURSES",
    "COURSE WITHDRAWAL",
]

for term in search_terms:
    print(f"\n\n{'#' * 80}")
    print(f"SEARCHING FOR: {term}")
    print("#" * 80)

    matches = [
        (i, chunk)
        for i, chunk in enumerate(chunks)
        if term.lower() in chunk.page_content.lower()
    ]

    for i, chunk in matches[:5]:
        print(f"\nCHUNK {i}")
        print("Metadata:", chunk.metadata)
        print("Characters:", len(chunk.page_content))
        print("-" * 70)
        print(chunk.page_content)

results = {
    "strategy": "semantic",
    "config": {
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "breakpoint_threshold_type": "percentile",
    },
    "stats": {
        "final_chunks": len(chunks),
        "min_characters": min(lengths),
        "max_characters": max(lengths),
        "avg_characters": sum(lengths) / len(lengths),
    },
    "chunks": [
        {
            "content": chunk.page_content,
            "metadata": chunk.metadata,
            "characters": len(chunk.page_content),
        }
        for chunk in chunks
    ],
}

output_path = Path(
    "experimentation/results/semantic_percentile_default.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_text(
    json.dumps(results, indent=2)
)