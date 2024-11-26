from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import  select
from typing import List
from database import SessionDep
from schemas import *
from models import *
from utils import *
from candidates import candidate_router
from recruiters import recruiter_router

app = FastAPI()
app.include_router(candidate_router, prefix="/candidates", tags=["candidates"])
app.include_router(recruiter_router, prefix="/recruiters", tags=["recruiters"])


@app.post("/signup")
async def signup(user_input: UserSignupInput, session: SessionDep):
 
    existing_user = session.exec(select(User).where(User.email == user_input.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_function(user_input.password)

 
    new_user = User(
        name=user_input.name,
        email=user_input.email,
        password=hashed_password,
        role=user_input.role
    )
    session.add(new_user)
    session.commit()
    return {"message": "User signed up successfully!"}


@app.post("/login")
async def login(user_input: LoginInput, session: SessionDep):
    user = session.exec(select(User).where(User.email == user_input.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    if not verify_password(user_input.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )

    return {"message": "Login successful!", "user_id": user.id, "role": user.role}












@app.post("/logout")
async def logout():
    return {"message": "You have logged out successfully. Please clear any session data on the client side."}