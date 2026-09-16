"""
An experiment to determine what kind of chunking strategy to use.
After converting the pdf into a markdown file,a lot of the structure from the original pdf was preserved,
This experiment is to determine the adequate chunking strategy needed to split the text in a way that preserves the information.
First chunk size: 1500, overlap: 200
Second chunk size: 2500, overlap: 250
"""

from pathlib import Path
import json
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

markdown = Path("data/raw/GSU Catalog 2024-2026 cleaned.md").read_text()

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

print("Sections:", len(sections))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)

chunks = text_splitter.split_documents(sections)

print("Final chunks:", len(chunks))

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

lengths = [len(chunk.page_content) for chunk in chunks]
results = {
    "strategy": "heading_recursive",
    "config": {
        "chunk_size": 1500,
        "chunk_overlap": 200,
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
    "experimentation/results/heading_recursive_1500_200.json"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

output_path.write_text(
    json.dumps(results, indent=2)
)