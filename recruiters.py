from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from database import SessionDep
from models import *
from schemas import *
from utils import *

recruiter_router = APIRouter()


@recruiter_router.post("/jobs/{recruiter_id}")
async def create_job(job_input: JobCreate, recruiter_id: int, session: SessionDep):
    recruiter = session.get(User, recruiter_id)
    if not recruiter or recruiter.role != UserRole.RECRUITER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only recruiters can post jobs")
    job = Job(title=job_input.title, description=job_input.description, recruiter_id=recruiter_id)
    session.add(job)
    session.commit()
    return {"message": "Job posted successfully!"}


@recruiter_router.get("/jobs/{job_id}/applicants", response_model=List[Application])
async def view_applicants(job_id: int, recruiter_id: int, session: SessionDep):
    job = session.get(Job, job_id)
    if not job or job.recruiter_id != recruiter_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view applicants")
    applications = session.exec(select(Application).where(Application.job_id == job_id)).all()
    return applications