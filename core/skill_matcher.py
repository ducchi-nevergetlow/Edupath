import json

class SkillMatcher:
    def __init__(self, spec_folder: str):
        self.spec_folder = spec_folder

    def evaluate_suitability(self, student_grades: dict, target_spec: str) -> dict:
        filepath = f"{self.spec_folder}/{target_spec}.json"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                weights = json.load(f)
        except FileNotFoundError:
            return {"error": "Không tìm thấy dữ liệu định hướng."}

        total_weight = 0
        weighted_score = 0
        gap_courses = []

        for course_id, weight in weights.items():
            if course_id in student_grades:
                grade = student_grades[course_id]
                weighted_score += grade * weight
                total_weight += weight
                
                if weight >= 0.8 and grade < 2.5:
                    gap_courses.append(course_id)

        core_gpa = round(weighted_score / total_weight, 2) if total_weight > 0 else 0

        if core_gpa >= 3.0 and not gap_courses:
            color, msg = "green", "Phù hợp định hướng."
        elif core_gpa >= 2.5:
            color, msg = "yellow", "Cần ôn tập môn bị hổng."
        else:
            color, msg = "red", "Chưa đủ năng lực nền tảng."

        return {
            "core_gpa": core_gpa,
            "color_code": color,
            "message": msg,
            "gap_courses": gap_courses
        }