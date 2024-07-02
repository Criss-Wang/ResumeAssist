from typing import List, Dict


def parse_to_bullet_pts(text: str) -> List[str]:
    if len(text) == 0:
        raise ValueError("Empty String provided. Double check agent output.")
    highlight_list = text.split("\n")
    highlight_list = [
        highlight[1:].strip() for highlight in highlight_list if highlight[0] == "-"
    ]
    return highlight_list


def parse_skill_pts(text: str) -> List[str]:
    """
    output format:
    [
        "category 1: skill1,skill2,...",
        "category 2: skill1,skill2,...",
        ....
    ]
    """
    skills_list = []
    for cat in text.split("- "):
        if "Category" in cat:
            skills_list.append(cat.strip())
    return skills_list


def build_skills_str(skills: Dict) -> str:
    skills = "\n".join(
        [
            "- " + category + ": " + ", ".join(skill_list)
            for category, skill_list in skills.items()
        ]
    )
    return skills


def build_work_str(work: List) -> str:
    work_list = []
    for w in work:
        work_str = ""
        work_str += f'work company: {w["work_company"]}\n'
        work_str += f'work role: {w["work_role"]}\n'
        work_str += f'period: {w["start_date"]} - {w["end_date"]}\n'

        highlight_str = "\n".join(["- " + h for h in w["highlights"]])
        work_str += f"highlights:\n{highlight_str}"
        work_list.append(work_str)
    return "\n\n".join(work_list)


def build_project_str(projects: List):
    project_list = []
    for p in projects:
        project_str = ""
        project_str += f'project name: {p["project_name"]}\n'
        project_str += f'period: {p["start_date"]} - {p["end_date"]}\n'

        highlight_str = "\n".join(["- " + h for h in p["highlights"]])
        project_str += f"highlights:\n{highlight_str}"
        project_list.append(project_str)
    return "\n\n".join(project_list)
