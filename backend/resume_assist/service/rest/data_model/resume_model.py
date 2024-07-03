from pydantic import BaseModel, Field
from typing import List, Dict


class AddonInfo(BaseModel):
    keywords: List[str]


class JobDetails(BaseModel):
    company: str
    position: str
    description: str
    url: str


class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    github: str
    linkedin: str
    website: str = Field(default="")


class Project(BaseModel):
    project_name: str
    start_date: str
    end_date: str
    highlights: List[str]


class Intro(BaseModel):
    content: str


class Skills(BaseModel):
    categories: List[str]
    skill_mapping: Dict[str, List[str]]


class Work(BaseModel):
    company: str
    location: str
    role: str
    start_date: str
    end_date: str
    highlights: List[str]
