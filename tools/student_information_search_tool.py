import json
from project_paths import STUDENTS_PATH


def get_student(student_id: str):
    """
        Retrieves a student's academic profile by student ID.

        Use this tool when student-specific information is needed, such as
        the student's major, classification, or completed courses.

        Args:
            student_id: The unique student ID, for example "S004".

        Returns:
            The student's academic profile if found, otherwise an error message.
        """
    with STUDENTS_PATH.open(encoding="utf-8") as file:
        data = json.load(file)

    for student in data["students"]:
        if student["student_id"].lower() == student_id.lower():
            return student

    return {"error": "student not found"}
