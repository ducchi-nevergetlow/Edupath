from pydantic import BaseModel
from typing import List

class CourseGrade(BaseModel):
    course_id: str
    grade: float

class AdvisorRequest(BaseModel):
    student_name: str
    target_specialization: str
    passed_courses: List[CourseGrade]