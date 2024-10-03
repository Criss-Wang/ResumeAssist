import logging
from typing import Dict, List

from resume_assist.agent_hub.base import Agent
from resume_assist.functions.cv_rendering import build_cv, build_design, render_pdf
from resume_assist.utilities.formatting_utils import convert_dateformat

logger = logging.getLogger(__name__)


def build_projects(projects):
    res = {}
    final_projects = []
    for project in projects:
        final_projects.append(
            {
                "name": project["project_name"],
                "date": (
                    f"[code]({project['url']})"
                    if project["url"]
                    else f"{project['start_date']} - {project['end_date']}"
                ),
            }
        )
    if final_projects:
        res["projects"] = final_projects
    return res


def build_summary(self_intro):
    res = {}
    if self_intro:
        res["Professional Summary"] = [self_intro["content"]]
    return res


def build_research(researches):
    res = {}
    final_researches = []
    for research in researches:
        final_researches.append(
            {
                "title": research["title"],
                "date": (
                    research["conference"]
                    if "conference" in research and research["conference"]
                    else convert_dateformat(research["date"])
                ),
                "authors": research["authors"].split(";"),
            }
        )
    if final_researches:
        res["publications"] = final_researches
    return res


def build_personal(personal_info):
    # pseronal info is required
    linkedin_username = personal_info["linkedin"].split(".com/")[1].rstrip("/")
    github_username = personal_info["github"].split(".com/")[1].rstrip("/")
    return {
        "name": personal_info["name"],
        "email": personal_info["email"],
        "phone": personal_info["phone"],
        "website": (
            personal_info["website"]
            if "http" in personal_info["website"]
            else "https://" + personal_info["website"]
        ),
        "social_networks": [
            {"network": "LinkedIn", "username": linkedin_username},
            {"network": "GitHub", "username": github_username},
        ],
    }


def build_educations(educations):
    res = {}
    final_educations = []
    for education in educations:
        final_educations.append(
            {
                "institution": education["institution"],
                "area": education["area"],
                "degree": education["degree"],
                "start_date": convert_dateformat(education["start_date"]),
                "end_date": (
                    convert_dateformat(education["end_date"])
                    if not education["current"]
                    else "present"
                ),
                "highlights": [f'GPA: {education["gpa"]}']
                + education["other"].split(";"),
            }
        )
    if final_educations:
        res["education"] = final_educations
    return res


def build_work(work):
    final_work = []
    for w in work:
        final_work.append(
            {
                "company": w["company"],
                "position": w["role"],
                "location": w["location"],
                "start_date": convert_dateformat(w["start_date"]),
                "end_date": (
                    convert_dateformat(w["end_date"]) if not w["current"] else "present"
                ),
                "highlights": w["highlights"],
            }
        )
    return {"experience": final_work}


def build_skills(skills):
    final_skills = []
    for cat in skills["categories"]:
        final_skills.append(
            {"label": cat, "details": ", ".join(skills["skill_mapping"][cat])}
        )
    return {"skills": final_skills}


class RenderAgent(Agent):
    def step(self, input_vars: Dict) -> List[str]:
        cv_info = {}
        try:
            cv_info["personal"] = build_personal(input_vars["personal_info"])
            cv_info["education"] = build_educations(input_vars["educations"])
            cv_info["work"] = build_work(input_vars["work"])
            cv_info["skills"] = build_skills(input_vars["skills"])
            cv_info["projects"] = build_projects(input_vars["projects"])
            cv_info["publications"] = build_research(input_vars["researches"])
            cv_info["summary"] = build_summary(input_vars["self_intro"])
            self.run_render(cv_info)
            return True
        except Exception as e:
            print(e)
            return False

    def run_render(self, cv_info, resume_name: str = "Resume") -> None:
        personal = cv_info["personal"]
        education = cv_info["education"]
        work = cv_info["work"]
        skills = cv_info["skills"]
        projects = cv_info["projects"]
        publications = cv_info["publications"]
        summary = cv_info["summary"]
        cv = build_cv(
            personal, education, work, skills, projects, publications, summary
        )
        design = build_design()
        render_pdf(cv, design, resume_name)

    def get_agent_name(self):
        return "renderer"
