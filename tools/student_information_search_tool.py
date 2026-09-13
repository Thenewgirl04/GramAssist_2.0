import json


def get_student(student_id: str):
    with open("data/mock/students.json", "r") as file:
        data = json.load(file)

    for student in data["students"]:
        if student["student_id"].lower() == student_id.lower():
            return student

    return {"error": "student not found"}

