from typing import List
from pydantic import BaseModel

"""
Major
Classification
"""
class Course(BaseModel):
    name: str
    number: str
    credit_hrs: int
    prerequisites: List[str]

class Classification(BaseModel):
    name: str
    total_credit_required: int
    courses: List[Course]

class Electives(BaseModel):
    courses: List[Course]

class Major(BaseModel):
    name: str
    total_credit_required: int
    classifications: List[Classification]
    electives: Electives

class Department(BaseModel):
    name: str
    majors: List[Major]

