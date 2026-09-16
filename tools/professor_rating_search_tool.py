import json
from utils.name_normalizer import normalize_professor_name
from project_paths import PROFESSORS_PATH

def get_professor(professor_name: str):
    """
        Retrieves available student-rating information for a professor.

        The lookup handles supported variations in titles and capitalization,
        such as "Dr. Kane" and "Kane".

        Args:
            professor_name: The professor's name, for example "Dr. Kane".

        Returns:
            Available professor rating information if found, otherwise an
            error message.
    """
    with PROFESSORS_PATH.open(encoding="utf-8") as file:
        data = json.load(file)

    target_professor = normalize_professor_name(professor_name)

    for professor in data["professors"]:
        stored_professor = normalize_professor_name(professor["name"])
        if stored_professor == target_professor:
            return professor

    return {"error": "professor not found"}
