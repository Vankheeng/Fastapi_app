from fastapi import FastAPI, Depends
import models
from database import engine, get_db
from pydantic import BaseModel
from schemas import user
from security.hashing import Hash
from sqlalchemy.orm import Session
from routers import auth_route, user, group, member


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth_route.router)
app.include_router(user.router)
app.include_router(group.router)
# app.include_router(member.router)