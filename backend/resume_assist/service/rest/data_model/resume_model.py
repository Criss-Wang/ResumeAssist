from pydantic import BaseModel, Field
from typing import List, Dict


class AddonRequest(BaseModel):
    pass


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


class ProjectRequest(BaseModel):
    pass


class Intro(BaseModel):
    content: str


class Skills(BaseModel):
    categories: List[str]
    skill_mapping: Dict[str, List[str]]


class WorkRequest(BaseModel):
    pass


class AddonResponse(BaseModel):
    pass


class ProjectResponse(BaseModel):
    pass


class IntroResponse(BaseModel):
    pass


class SkillsResponse(BaseModel):
    pass


class WorkResponse(BaseModel):
    pass
