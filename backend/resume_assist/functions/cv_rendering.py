import os
import yaml
from typing import Dict


DEFAULT_MARGINS = {
    "page": {"top": "1.2 cm", "bottom": "1.2 cm", "left": "1.2 cm", "right": "1.2 cm"},
    "section_title": {"top": "0.3 cm", "bottom": "0.2 cm"},
    "entry_area": {
        "left_and_right": "0 cm",
        "vertical_between": "0.2 cm",
        "date_and_location_width": "4.5 cm",
    },
    "highlights_area": {
        "top": "0.10 cm",
        "left": "0 cm",
        "vertical_between_bullet_points": "0.10 cm",
    },
    "header": {
        "vertical_between_name_and_connections": "5 pt",
        "bottom": "5 pt",
        "horizontal_between_connections": "10 pt",
    },
}


def build_yaml(data):
    with open("output.yaml", "w") as file:
        yaml.dump(data, file, default_flow_style=False)


def build_cv(personal, education, work, skills, projects, publications, summary):
    info = {}
    info.update(personal)

    sections = {}
    if summary:
        sections.update(summary)
    sections.update(education)
    sections.update(work)
    sections.update(skills)
    if projects:
        sections.update(projects)
    if publications:
        sections.update(publications)

    info["sections"] = sections

    return info


def build_design(margins=DEFAULT_MARGINS):
    return {
        "theme": "engineeringresumes",
        "font": "Charter",
        "font_size": "10pt",
        "page_size": "a4paper",
        "header_font_size": "20 pt",
        "text_alignment": "left-aligned",
        "use_icons_for_connections": True,
        "margins": margins,
    }


def render_pdf(cv: Dict, design: Dict, resume_name: str) -> None:
    try:
        build_yaml({"cv": cv, "design": design})

        if not os.path.exists("output.yaml"):
            raise RuntimeError("Fail to generate yaml file, check formatting")

        if not os.path.exists("resume_pdfs"):
            os.makedirs("resume_pdfs")

        render_cmd = "rendercv render 'output.yaml' --dont-generate-markdown --dont-generate-html --dont-generate-png"
        render_cmd += (
            f" --output-folder-name outputs --pdf-path resume_pdfs/{resume_name}.pdf"
        )
        code = os.system(render_cmd)
        if code != 0:
            raise RuntimeError("Fail to run rendercv")
        os.system("rm output.yaml")
        os.system("rm -rf outputs")
    except Exception as e:
        print(e)
