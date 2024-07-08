from typing import List, Dict, Tuple, Any, Callable


def parse_grading_details(text: str) -> Tuple[Any]:
    grade, remark = text.split("-" * 10)
    grade = int(grade.strip("\n"))
    return grade, remark.strip("\n")


def parse_to_bullet_pts(text: str) -> List[str]:
    if len(text) == 0:
        raise ValueError("Empty String provided. Double check agent output.")
    point_list = text.split("\n")
    point_list = [info[1:].strip() for info in point_list if info and info[0] == "-"]
    return point_list


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


def build_full_job_description(company: str, role: str, description: str) -> str:
    return f"""Company: {company}
----------
Role: {role}
----------
Job Description: {description}
"""


def build_skills_str(skills: Dict[str, List]) -> str:
    skills_str = "\n".join(
        [
            "- " + category + ": " + ", ".join(skill_list)
            for category, skill_list in skills.items()
        ]
    )
    return skills_str


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


def build_project_str(projects: List) -> str:
    project_list = []
    for p in projects:
        project_str = ""
        project_str += f'project name: {p["project_name"]}\n'
        project_str += f'period: {p["start_date"]} - {p["end_date"]}\n'

        highlight_str = "\n".join(["- " + h for h in p["highlights"]])
        project_str += f"highlights:\n{highlight_str}"
        project_list.append(project_str)
    return "\n\n".join(project_list)


def build_highlight_str(chunk: Any) -> str:
    return "\n".join(["- " + highlight for highlight in chunk.get("highlights")])


def build_reference_chunks_str(chunks: List[str], chunk_parser: Callable) -> str:
    import pdb

    pdb.set_trace()
    s = "<Examples>\nHere are a list of examples of highlights that may be relevant to this job, use them as references points if necessary.\n\n"
    s += "----------\n\n".join(
        [f"Example {i+1}: \n{chunk_parser(chunk)}\n" for i, chunk in enumerate(chunks)]
    )
    s += "\n</Examples>"
    return s


def build_previous_attempt_str(attempt_body: List[str], remark: str) -> str:
    s = "Here is a previous attempt to improve this highlight that failed. Learn from the remark and try to create a bettern one if possible:\n"
    attempt_body = "\n".join(["- " + ele for ele in attempt_body])
    s += f"<PreviousAttempt>\n{attempt_body}"
    s += "\n</PreviousAttempt>\n\n"
    s += f"<Remark>\n{remark}\n</Remark>"
    return s
