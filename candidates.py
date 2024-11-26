from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from database import SessionDep
from models import *
from schemas import *
from utils import *

candidate_router = APIRouter()


@candidate_router.get("/jobs", response_model=List[Job])
async def list_jobs(session: SessionDep):
    jobs = session.exec(select(Job)).all()
    return jobs

@candidate_router.post("/apply/{job_id}")
async def apply_to_job(job_id: int, candidate_id: int, session: SessionDep):
    candidate = session.get(User, candidate_id)
    if not candidate or candidate.role != UserRole.CANDIDATE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only candidates can apply")
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    application = Application(candidate_id=candidate_id, job_id=job_id)
    session.add(application)
    session.commit()
    recruiter = session.get(User, job.recruiter_id)

    if recruiter:
        subject = "Job Application Received"
        candidate_message = f"Hello {candidate.name},\n\nYou have successfully applied for the job '{job.title}'."
        recruiter_message = f"Hello {recruiter.name},\n\nA new application has been received for the job '{job.title}' from {candidate.name}."
        send_email(subject, candidate_message, candidate.email)
        send_email(subject, recruiter_message, recruiter.email)
    return {"message": "Application submitted successfully!"}



@candidate_router.get("/applied_jobs/{candidate_id}", response_model=List[Job])
async def get_applied_jobs(candidate_id: int, session: SessionDep):
    applications = session.exec(select(Application).where(Application.candidate_id == candidate_id)).all()
    if not applications:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No applications found for this candidate")

    job_ids = [application.job_id for application in applications]
    jobs = session.exec(select(Job).where(Job.id.in_(job_ids))).all()
    if not jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No jobs found for the applications")

    return jobs