import time
import psycopg2
from fastapi import FastAPI, APIRouter
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import users, post, auth, vote
from .routers.post import router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@router.get("/")
async def root():
    return {"message": "Hello World"}

