import json

CURRICULUM_PATH = "data/structured/cs_curriculum.json"

def get_classification_curriculum(classification: str) -> dict:
    with open(CURRICULUM_PATH, "r") as file:
        curriculum = json.load(file)

    for level in curriculum["classifications"]:
        if level["name"].lower() == classification.lower():
            return level

    return {"error": f"Classification '{classification}' not found"}


def get_course(course_number: str) -> dict:
    with open(CURRICULUM_PATH, "r") as file:
        curriculum = json.load(file)

    for level in curriculum["classifications"]:
        for course in level["courses"]:
            if course["number"].lower() == course_number.lower():
                return course

    for course in curriculum["electives"]["courses"]:
        if course["number"].lower() == course_number.lower():
            return course

    return {"error": f"Course '{course_number}' not found"}