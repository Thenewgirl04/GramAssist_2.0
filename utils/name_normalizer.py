def normalize_professor_name(name: str) -> str:
    name = name.lower().strip()

    titles = ["dr.", "dr", "prof.", "prof", "professor"]

    for title in titles:
        if name.startswith(title + " "):
            name = name[len(title):].strip()

    return name