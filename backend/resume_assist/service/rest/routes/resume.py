import json

from fastapi import APIRouter, HTTPException, Response
from uuid import UUID

from resume_assist.service.rest.data_model.resume_model import Resume
from resume_assist.io.db.engine import neo4j_client
from resume_assist.utilities.embedding_utils import get_indexer_embedding

from resume_assist.agent_hub.render_agent import RenderAgent
from resume_assist.agent_hub.summary_agent import SummaryAgent


resume_router = APIRouter(prefix="/api/resume", tags=["Resume: Complete"])


@resume_router.post("/save/{id}")
def save_resume(id: UUID, request: Resume):
    # save all elements in the resume
    # render the pdf
    render_agent = RenderAgent("render", use_prompt=False)
    render_agent.step(request)
    # save the relationships
    try:
        query = """
        MERGE (r:Resume {id: $id})
        SET r.embedding = $embedding

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
        MATCH (pr:Project {id: project_id})
        SET pr.embedding = $embedding, pr.label = $label
        MERGE (r)-[:HAS_PROJECT]->(pr)

        WITH r
        UNWIND $work_ids AS work_id
        MATCH (w:Work {id: work_id})
        SET w.embedding = $embedding, w.label = $label
        MERGE (r)-[:HAS_WORK]->(w)

        RETURN r
        """

        # get job summary
        job_details = request.job_details
        summary_agent = SummaryAgent("resume")
        job_summary = summary_agent.step(
            {
                "company": job_details.company,
                "role": job_details.position,
                "job_description": job_details.description,
            }
        )
        # get query embedding
        indexer_embedding = get_indexer_embedding([job_summary])[0]
        parameters = {
            "id": str(id),
            "project_ids": request.project_ids,
            "work_ids": request.work_ids,
            "embedding": indexer_embedding,
            "label": request.label,
        }
        result = neo4j_client.query(query, parameters)

        if not result:
            raise HTTPException(500, "Failed to save resume with relationships built")
        return Response(status_code=200)
    except Exception as e:
        # logger.exception(e)
        print(e)
        raise HTTPException(500, "Unexpected error")


@resume_router.get("/{id}", response_model=Resume)
def get_resume(id: UUID):
    try:
        query = """
        MATCH (r:Resume {id: $id})
        OPTIONAL MATCH (r)-[:FOR_JOB]->(job_details:Job)
        OPTIONAL MATCH (r)-[:HAS_PERSONAL_INFO]->(personal_info:PersonalInfo)
        OPTIONAL MATCH (r)-[:HAS_SELF_INTRO]->(intro:SelfIntro)
        OPTIONAL MATCH (r)-[:HAS_SKILLS]->(skills:Skills)
        OPTIONAL MATCH (r)-[:HAS_PROJECT]->(pr:Project)
        OPTIONAL MATCH (r)-[:HAS_WORK]->(w:Work)
        RETURN r, job_details, personal_info, intro, skills,
            COLLECT(DISTINCT pr) as projects,
            COLLECT(DISTINCT w) as works
        """
        parameters = {"id": str(id)}
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
