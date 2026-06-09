import json
import networkx as nx

class GraphEngine:
    def __init__(self, curriculum_file: str):
        with open(curriculum_file, 'r', encoding='utf-8') as f:
            self.courses = json.load(f)
        self.graph = self._build_graph()

    def _build_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()
        for course_id, data in self.courses.items():
            G.add_node(course_id, name=data['name'], credits=data['credits'])
            for prereq in data.get('prerequisites', []):
                G.add_edge(prereq, course_id)
                
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("Lỗi: Khung chương trình có chứa vòng lặp!")
        return G

    def get_available_courses(self, passed_courses: set) -> list:
        available = []
        for course_id in self.courses:
            if course_id in passed_courses:
                continue
            prereqs = self.courses[course_id].get('prerequisites', [])
            if all(p in passed_courses for p in prereqs):
                available.append({
                    "course_id": course_id,
                    "name": self.courses[course_id]["name"],
                    "credits": self.courses[course_id]["credits"]
                })
        return available