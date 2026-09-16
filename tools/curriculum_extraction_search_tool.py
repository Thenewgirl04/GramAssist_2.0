import json
from project_paths import CURRICULUM_JSON_PATH

def get_classification_curriculum(classification: str) -> dict:
    """
        Retrieves curriculum requirements for a student classification.

        Args:
            classification: The classification to retrieve.
                Valid values are "Freshman", "Sophomore", "Junior", or "Senior".

        Returns:
            The courses and total required credit hours for the classification.
    """
    
    with CURRICULUM_JSON_PATH.open(encoding="utf-8") as file:
        curriculum = json.load(file)

    for level in curriculum["classifications"]:
        if level["name"].lower() == classification.lower():
            return level

    return {"error": f"Classification '{classification}' not found"}


def get_courses(course_numbers: list[str]) -> list[dict]:
    """
    Retrieves curriculum information for one or more specific courses.

    Use this tool to find course names, credit hours, and prerequisites.
    When information is needed for multiple courses, provide all course
    numbers in a single call instead of calling this tool separately.

    Args:
        course_numbers: A list of course numbers, for example
            ["CS 310", "PHYS 111", "PHYS 112"].

    Returns:
        A list containing the information for each requested course.
        Courses that are not found are returned with an error message.
    """
    with CURRICULUM_JSON_PATH.open(encoding="utf-8") as file:
        curriculum = json.load(file)

    all_courses = []

    for level in curriculum["classifications"]:
        all_courses.extend(level["courses"])

    all_courses.extend(curriculum["electives"]["courses"])

    results = []

    for course_number in course_numbers:
        course_found = None

        for course in all_courses:
            if course["number"].lower() == course_number.lower():
                course_found = course
                break

        if course_found:
            results.append(course_found)
        else:
            results.append({
                "error": f"Course '{course_number}' not found"
            })

    return results