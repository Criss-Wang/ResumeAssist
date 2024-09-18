import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from resume_assist.service.rest.routes.addon import addon_info_router
from resume_assist.service.rest.routes.job_details import job_details_router
from resume_assist.service.rest.routes.personal import personal_info_router
from resume_assist.service.rest.routes.project import project_router
from resume_assist.service.rest.routes.self_intro import self_intro_router
from resume_assist.service.rest.routes.skills import skills_router
from resume_assist.service.rest.routes.work import work_experience_router
from resume_assist.service.rest.routes.education import education_router
from resume_assist.service.rest.routes.resume import resume_router


def create_fastapi_application() -> FastAPI:
    enable_docs = bool(os.environ.get("SHOW_DOCS", True))

    docs_args = {}
    if enable_docs is False:
        docs_args = {"docs_url": None, "redoc_url": None}

    api = FastAPI(**docs_args)

    api.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routers(api)
    return api


def register_routers(api: FastAPI):
    api.include_router(addon_info_router)
    api.include_router(job_details_router)
    api.include_router(personal_info_router)
    api.include_router(project_router)
    api.include_router(self_intro_router)
    api.include_router(skills_router)
    api.include_router(work_experience_router)
    api.include_router(education_router)
    api.include_router(resume_router)
