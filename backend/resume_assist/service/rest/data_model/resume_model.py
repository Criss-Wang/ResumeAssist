from enum import Enum
from typing import List, Dict, Literal, Optional
from pydantic import BaseModel, Field


class Label(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


class AddonInfo(BaseModel):
    keywords: List[str]


class JobDetails(BaseModel):
    company: str
    position: str
    description: str
    url: str


class Education(BaseModel):
    education_id: str
    institution: str = Field(default="")
    area: str = Field(default="")
    degree: str = Field(default="")
    current: bool = Field(default=False)
    gpa: str = Field(default="")
    courses: str = Field(default="")
    other: str = Field(default="")
    start_date: str = Field(default="")
    end_date: str = Field(default="")


class Research(BaseModel):
    research_id: str
    title: str = Field(default="")
    authors: str = Field(default="")
    conference: str = Field(default="")
    date: str = Field(default="")


class PersonalInfo(BaseModel):
    name: str = Field(default="")
    email: str = Field(default="")
    phone: str = Field(default="")
    github: str = Field(default="")
    linkedin: str = Field(default="")
    website: str = Field(default="")


class Project(BaseModel):
    project_id: str
    project_name: str
    start_date: str
    end_date: str
    highlights: List[str]
    current: bool
    url: str


class Intro(BaseModel):
    content: str
    title: str


class Skills(BaseModel):
    categories: List[str]
    skill_mapping: Dict[str, List[str]]


class Work(BaseModel):
    work_id: str
    company: str
    location: str
    role: str
    start_date: str
    end_date: str
    current: bool
    highlights: List[str]


class Resume(BaseModel):
    job_details: JobDetails
    personal_info: PersonalInfo
    researches: List[Research]
    educations: List[Education]
    self_intro: Intro
    skills: Skills
    work: List[Work]
    projects: List[Project]
    addtional_info: Optional[AddonInfo] = Field(default=None)
    label: Label


class ResumeRequest(BaseModel):
    job_details: JobDetails
    work_ids: List[str]
    project_ids: List[str]
    label: Literal["success", "fail", "unlabeled"] = Field(
        default="unlabeled", description="outcome of the application using this resume"
    )
