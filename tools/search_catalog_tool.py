from rag_pipeline.retrieve_catalog import retrieve_similar_chunks

def search_catalog(query: str):
    """
       Search the Grambling State University General Catalog for university-wide
       academic policies, procedures, requirements, and regulations.

       Use this tool for questions about topics such as academic probation,
       course withdrawal and drop policies, transfer credits, repeating courses,
       graduation requirements, First Year Experience requirements, and other
       university academic policies.

       Do not use this tool for student-specific information, curriculum course
       requirements, course prerequisites, or professor information.

       Args:
           query (str): The academic policy or catalog question to search for.

       Returns:
           list[dict]: Relevant catalog sections containing content and heading
           metadata.
    """
    documents = retrieve_similar_chunks(query)
    results = []
    for doc in documents:
        results.append({
            "content": doc.page_content,
            "section": doc.metadata.get("Header 3"),
            "subsection": doc.metadata.get("Header 2"),
            "category": doc.metadata.get("Header 1")
        })

    return results







