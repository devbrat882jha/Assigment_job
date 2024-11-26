from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class UserRole(str, Enum):
    CANDIDATE = "candidate"
    RECRUITER = "recruiter"


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False)
    role: UserRole
    jobs_posted: List["Job"] = Relationship(back_populates="recruiter")
    applications: List["Application"] = Relationship(back_populates="candidate")


class Job(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    recruiter_id: int = Field(foreign_key="user.id")
    recruiter: User = Relationship(back_populates="jobs_posted")
    applications: List["Application"] = Relationship(back_populates="job")


class Application(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    candidate_id: int = Field(foreign_key="user.id")
    job_id: int = Field(foreign_key="job.id")
    candidate: User = Relationship(back_populates="applications")
    job: Job = Relationship(back_populates="applications")
