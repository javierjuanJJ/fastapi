from typing import List

import psycopg2
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
from starlette import status
from websockets.http11 import Response
from psycopg2 import *
from psycopg2.extras import RealDictCursor

from app import models, utils
from app.database import get_db
from app.main import app
from app.routers import post
from app.schemas import UserCreate, UserOut
router = APIRouter(
    prefix="/users"
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[UserOut])
def create_user(user: UserCreate, do: Session = Depends(get_db)):
    new_user = models.Post(**user.dict())

    user.password = utils.hash(user.password)

    do.add(new_user)
    do.commit()
    do.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=List[UserOut])
def get_user(id: int, do: Session = Depends(get_db)):
    user = do.query(models.User).filter_by(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id : {id} not found")
    return user

