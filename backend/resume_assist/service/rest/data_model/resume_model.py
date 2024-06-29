from pydantic import BaseModel


class AddonRequest(BaseModel):
    pass


class JobDetails(BaseModel):
    company: str
    position: str
    description: str


class PersonalInfoRequest(BaseModel):
    pass


class ProjectRequest(BaseModel):
    pass


class IntroRequest(BaseModel):
    pass


class SkillsRequest(BaseModel):
    pass


class WorkRequest(BaseModel):
    pass


class AddonResponse(BaseModel):
    pass


class PersonalInfoResponse(BaseModel):
    pass


class ProjectResponse(BaseModel):
    pass


class IntroResponse(BaseModel):
    pass


class SkillsResponse(BaseModel):
    pass


class WorkResponse(BaseModel):
    pass
