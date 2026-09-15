from pathlib import Path
import json

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings


markdown = Path(
    "data/raw/GSU Catalog 2024-2026 cleaned.md"
).read_text()

headers_to_split = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
    ("####", "Header 4"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split,
    strip_headers=False,
)

sections = markdown_splitter.split_text(markdown)

print("Heading sections:", len(sections))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

semantic_splitter = SemanticChunker(
    embeddings,
    breakpoint_threshold_type="percentile",
)

MAX_SECTION_SIZE = 2500

chunks = []

for section in sections:

    if len(section.page_content) <= MAX_SECTION_SIZE:
        chunks.append(section)

    else:
        semantic_chunks = semantic_splitter.create_documents(
            [section.page_content]
        )

        # Preserve heading metadata
        for chunk in semantic_chunks:
            chunk.metadata.update(section.metadata)

        chunks.extend(semantic_chunks)


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
    "strategy": "heading_semantic",
    "config": {
        "max_section_size": MAX_SECTION_SIZE,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "breakpoint_threshold_type": "percentile",
    },
    "stats": {
        "sections": len(sections),
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
    "experimentation/results/heading_hybrid_chunking_2500.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_text(
    json.dumps(results, indent=2)
)