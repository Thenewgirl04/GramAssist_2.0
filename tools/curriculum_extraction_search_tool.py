import json

CURRICULUM_PATH = "data/structured/cs_curriculum.json"

def get_classification_curriculum(classification: str) -> dict:
    """
        Retrieves curriculum requirements for a student classification.

        Args:
            classification: The classification to retrieve.
                Valid values are "Freshman", "Sophomore", "Junior", or "Senior".

        Returns:
            The courses and total required credit hours for the classification.
    """
    
    with open(CURRICULUM_PATH, "r") as file:
        curriculum = json.load(file)

    for level in curriculum["classifications"]:
        if level["name"].lower() == classification.lower():
            return level

    return {"error": f"Classification '{classification}' not found"}


def get_course(course_number: str) -> dict:
    """
        Retrieves curriculum information for a specific course.

        Use this tool to find a course's name, credit hours, and prerequisites.

        Args:
            course_number: The course number, for example "CS 310".

        Returns:
            The course information if found, otherwise an error message.
        """
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