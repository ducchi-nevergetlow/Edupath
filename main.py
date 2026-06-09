from fastapi import FastAPI
from api.schemas import AdvisorRequest
from core.graph_engine import GraphEngine
from core.skill_matcher import SkillMatcher

app = FastAPI(title="EduPath AI")

graph_engine = GraphEngine(curriculum_file="data/curriculum_json/robotics.json")
skill_matcher = SkillMatcher(spec_folder="data/specializations")

@app.post("/api/v1/career_advisor")
async def get_career_advice(request: AdvisorRequest):
    passed_dict = {item.course_id: item.grade for item in request.passed_courses}
    passed_set = set(passed_dict.keys())

    available_courses = graph_engine.get_available_courses(passed_set)
    advisory_result = skill_matcher.evaluate_suitability(passed_dict, request.target_specialization)

    return {
        "student": request.student_name,
        "advisory_scenario": advisory_result,
        "recommended_next_courses": available_courses
    }