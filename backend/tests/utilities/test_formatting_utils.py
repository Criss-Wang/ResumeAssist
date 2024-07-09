import pytest
from resume_assist.utilities.formatting_utils import (
    parse_grading_details,
    parse_to_bullet_pts,
    parse_skill_pts,
    build_full_job_description,
    build_skills_str,
    build_work_str,
    build_project_str,
    build_highlight_str,
    build_reference_chunks_str,
    build_previous_attempt_str,
)


def test_parse_grading_details():
    text = "85\n----------\nGood work overall."
    expected_output = (85, "Good work overall.")
    assert parse_grading_details(text) == expected_output

    text = "70\n----------\nNeeds improvement."
    expected_output = (70, "Needs improvement.")
    assert parse_grading_details(text) == expected_output

    with pytest.raises(ValueError):
        parse_grading_details("Invalid format")


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


def test_build_full_job_description():
    company = "ABC Corp"
    role = "Software Engineer"
    description = "Develop and maintain software."
    expected_output = (
        "Company: ABC Corp\n"
        "----------\n"
        "Role: Software Engineer\n"
        "----------\n"
        "Job Description: Develop and maintain software."
    )
    assert build_full_job_description(company, role, description) == expected_output


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


def test_build_highlight_str():
    chunk = {"highlights": ["Achieved X", "Implemented Y"]}
    expected_output = "- Achieved X\n- Implemented Y"
    assert build_highlight_str(chunk) == expected_output

    chunk = {"highlights": []}
    expected_output = ""
    assert build_highlight_str(chunk) == expected_output


def test_build_reference_chunks_str():
    chunks = [
        {"highlights": ["Highlight 1", "Highlight 2"]},
        {"highlights": ["Highlight A", "Highlight B"]},
    ]
    expected_output = (
        "<Examples>\nHere are a list of examples of highlights that may be relevant to this job, use them as references points if necessary.\n\n"
        "----------\nExample 1: \n- Highlight 1\n- Highlight 2\n"
        "----------\n"
        "Example 2: \n- Highlight A\n- Highlight B\n\n"
        "</Examples>"
    )
    assert build_reference_chunks_str(chunks, build_highlight_str) == expected_output


def test_build_previous_attempt_str():
    attempt_body = ["Attempted improvement 1", "Attempted improvement 2"]
    remark = "Needs more work."
    expected_output = (
        "Here is a previous attempt to improve this highlight that failed. Learn from the remark and try to create a bettern one if possible:\n"
        "<PreviousAttempt>\n"
        "- Attempted improvement 1\n"
        "- Attempted improvement 2\n"
        "</PreviousAttempt>\n\n"
        "<Remark>\nNeeds more work.\n</Remark>"
    )
    assert build_previous_attempt_str(attempt_body, remark) == expected_output
