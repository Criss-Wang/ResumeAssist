import pytest
from resume_assist.utilities.formatting_utils import (
    parse_to_bullet_pts,
    parse_skill_pts,
    build_skills_str,
    build_work_str,
    build_project_str,
)


def test_parse_to_bullet_pts():
    text = "- Point 1\n- Point 2\n- Point 3"
    expected_output = ["Point 1", "Point 2", "Point 3"]
    assert parse_to_bullet_pts(text) == expected_output

    text = "No bullet points\nJust text\n- Bullet point"
    expected_output = ["Bullet point"]
    assert parse_to_bullet_pts(text) == expected_output

    text = ""
    with pytest.raises(
        ValueError,
        match="Empty String provided. Double check agent output.",
    ):
        parse_to_bullet_pts(text)


def test_parse_skill_pts():
    # Test input text
    input_text = """
    - Category 1: skill1,skill2
    - Category 2: skill3,skill4
    """

    # Expected output
    expected_output = ["Category 1: skill1,skill2", "Category 2: skill3,skill4"]

    # Call the function
    result = parse_skill_pts(input_text)

    # Assert the result matches the expected output
    assert result == expected_output


def test_build_skills_str():
    skills = {"Programming": ["Python", "Java"], "Data Science": ["Pandas", "NumPy"]}
    expected_output = "- Programming: Python, Java\n- Data Science: Pandas, NumPy"
    assert build_skills_str(skills) == expected_output

    skills = {}
    expected_output = ""
    assert build_skills_str(skills) == expected_output


def test_build_work_str():
    work = [
        {
            "work_company": "Company A",
            "work_role": "Developer",
            "start_date": "Jan 2020",
            "end_date": "Dec 2020",
            "highlights": ["Developed feature X", "Improved performance"],
        },
        {
            "work_company": "Company B",
            "work_role": "Manager",
            "start_date": "Feb 2021",
            "end_date": "Present",
            "highlights": ["Managed team Y", "Delivered project Z"],
        },
    ]
    expected_output = (
        "work company: Company A\n"
        "work role: Developer\n"
        "period: Jan 2020 - Dec 2020\n"
        "highlights:\n- Developed feature X\n- Improved performance\n\n"
        "work company: Company B\n"
        "work role: Manager\n"
        "period: Feb 2021 - Present\n"
        "highlights:\n- Managed team Y\n- Delivered project Z"
    )
    assert build_work_str(work) == expected_output

    work = []
    expected_output = ""
    assert build_work_str(work) == expected_output


def test_build_project_str():
    projects = [
        {
            "project_name": "Project A",
            "start_date": "Jan 2020",
            "end_date": "Dec 2020",
            "highlights": ["Feature X", "Performance Y"],
        },
        {
            "project_name": "Project B",
            "start_date": "Feb 2021",
            "end_date": "Present",
            "highlights": ["Team Y", "Project Z"],
        },
    ]
    expected_output = (
        "project name: Project A\n"
        "period: Jan 2020 - Dec 2020\n"
        "highlights:\n- Feature X\n- Performance Y\n\n"
        "project name: Project B\n"
        "period: Feb 2021 - Present\n"
        "highlights:\n- Team Y\n- Project Z"
    )
    assert build_project_str(projects) == expected_output

    projects = []
    expected_output = ""
    assert build_project_str(projects) == expected_output
