import json

from fastapi import APIRouter, HTTPException, Response, Request
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Resume, Label
from resume_assist.io.db.engine import neo4j_client
from resume_assist.agent_hub.render_agent import RenderAgent
from resume_assist.agent_hub.summary_agent import SummaryAgent
from resume_assist.utilities.embedding_utils import get_indexer_embedding


resume_router = APIRouter(prefix="/api/resume", tags=["Resume: Complete"])


@resume_router.post("/save/{id}")
async def save_resume(id: UUID, request: Request):
    info_vars = await request.json()
    # assumes all data has been save to resume
    # TODO: enable on-prem (without initial saving) resume rendering

    # render the pdf
    render_agent = RenderAgent("render", use_prompt=False)
    render_agent.step(info_vars)

    # save the relationshipsx
    try:
        query = """
        MERGE (r:Resume {id: $id})
        SET r.embedding = $embedding
        SET r.label = $label

        WITH r
        MATCH (j:Job {id: $id})
        SET j.embedding = $embedding
        MERGE (r)-[:FOR_JOB]->(j)

        WITH r
        MATCH (pi:PersonalInfo {id: $id})
        SET pi.embedding = $embedding
        MERGE (r)-[:HAS_PERSONAL_INFO]->(pi)

        WITH r
        MATCH (si:SelfIntro {id: $id})
        SET si.embedding = $embedding, si.label = $label
        MERGE (r)-[:HAS_SELF_INTRO]->(si)

        WITH r
        MATCH (sk:Skills {id: $id})
        SET sk.embedding = $embedding, sk.label = $label
        MERGE (r)-[:HAS_SKILLS]->(sk)

        WITH r
        UNWIND $project_ids AS project_id
        MATCH (pr:Project {project_id: project_id})
        SET pr.embedding = $embedding, pr.label = $label
        MERGE (r)-[:HAS_PROJECT]->(pr)

        WITH r
        UNWIND $work_ids AS work_id
        MATCH (w:Work {work_id: work_id})
        SET w.embedding = $embedding, w.label = $label
        MERGE (r)-[:HAS_WORK]->(w)

        WITH r
        UNWIND $education_ids AS education_id
        MATCH (edu:Education {education_id: education_id})
        SET edu.embedding = $embedding, edu.label = $label
        MERGE (r)-[:HAS_EDUCATION]->(edu)

        WITH r
        UNWIND $research_ids AS research_id
        MATCH (resea:Research {research_id: research_id})
        SET resea.embedding = $embedding, resea.label = $label
        MERGE (r)-[:HAS_RESEARCH]->(resea)

        RETURN r
        """
        job_embedding = build_job_embedding(info_vars)
        project_ids, work_ids, education_ids, research_ids = get_group_ids(info_vars)

        # build relationships
        parameters = {
            "id": str(id),
            "project_ids": project_ids,
            "work_ids": work_ids,
            "education_ids": education_ids,
            "research_ids": research_ids,
            "embedding": job_embedding,
            "label": info_vars["label"] if "label" in info_vars else Label.PENDING,
        }
        result = neo4j_client.query(query, parameters)

        if not result:
            raise HTTPException(500, "Failed to save resume with relationships built")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@resume_router.get("/{resume_id}", response_model=Resume)
def get_resume(resume_id: UUID):
    try:
        query = """
        MATCH (r:Resume {id: $resume_id})
        OPTIONAL MATCH (r)-[:FOR_JOB]->(job_details:Job)
        OPTIONAL MATCH (r)-[:HAS_PERSONAL_INFO]->(personal_info:PersonalInfo)
        OPTIONAL MATCH (r)-[:HAS_SELF_INTRO]->(intro:SelfIntro)
        OPTIONAL MATCH (r)-[:HAS_SKILLS]->(skills:Skills)
        OPTIONAL MATCH (r)-[:HAS_PROJECT]->(pr:Project)
        OPTIONAL MATCH (r)-[:HAS_WORK]->(w:Work)
        OPTIONAL MATCH (r)-[:HAS_EDUCATION]->(edu:Education)
        OPTIONAL MATCH (r)-[:HAS_RESEARCH]->(resea:Research)
        RETURN r, job_details, personal_info, intro, skills,
            COLLECT(DISTINCT pr) as projects,
            COLLECT(DISTINCT w) as work,
            COLLECT(DISTINCT edu) as educations,
            COLLECT(DISTINCT resea) as researches,
        """
        parameters = {"resume_id": str(resume_id)}
        result = neo4j_client.query(query, parameters)
        if not result:
            raise HTTPException(404, "Full Resume not found")
        resume_data = result[0].data()
        resume_data["skills"]["skill_mapping"] = json.loads(
            resume_data["skills"]["skill_mapping"]
        )

        return Resume(**resume_data)
    except Exception as e:
        print(e)
        raise HTTPException(500, "Unexpected error")


def get_group_ids(info_vars):
    project_ids = [p["project_id"] for p in info_vars["projects"]]
    work_ids = [w["work_id"] for w in info_vars["work"]]
    education_ids = [e["education_id"] for e in info_vars["educations"]]
    research_ids = [r["research_id"] for r in info_vars["researches"]]
    return project_ids, work_ids, education_ids, research_ids


def build_job_embedding(info_vars):
    # get job summary
    job_details = info_vars["job_details"]
    summary_agent = SummaryAgent("resume")
    job_summary = summary_agent.step(
        {
            "company": job_details["company"],
            "role": job_details["position"],
            "job_description": job_details["description"],
        }
    )
    # get query embedding
    return get_indexer_embedding([job_summary])[0]
