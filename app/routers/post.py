import time
from typing import List

import psycopg2
from fastapi import HTTPException, APIRouter
from fastapi.openapi.models import Response
from fastapi.params import Depends
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from starlette import status

from app import models
from app.database import get_db
from app.main import app
from app.models import Post
from app.schemas import PostCreate

router = APIRouter(
    prefix="/posts"
)
@router.get("/sqlalchemy")
def test_posts(do: Session = Depends(get_db)):

    posts = do.query(models.Post).all()

    return {"status": posts}

router = APIRouter()

myPosts = [
    {"title": "title 1", "content": "content 1", "id": 1},
    {"title": "title 2", "content": "content 2", "id": 2}
]


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/")
def get_posts(do: Session = Depends(get_db), response_model=List[Post]):
    posts = do.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[Post])
def createPost(newPost: PostCreate,currentUser: int, do: Session = Depends(get_db)):
    # postNew = models.Post(title = newPost.title, content = newPost.content,published = newPost.published)
    postNew = models.Post(**newPost.dict())

    do.add(postNew)
    do.commit()
    do.refresh(postNew)

    return {"data": postNew}


@router.get("/{id}", response_model=List[Post])
def get_posts(id: int, currentUser: int, do: Session = Depends(get_db)):
    post = do.query(models.Post).filter_by(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return post


def find_index_id(id: int):
    for i, p in enumerate(myPosts):
        if (p['id'] == id):
            return i


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, currentUser: int, do: Session = Depends(get_db)):

    deleted_post =do.query(models.Post).filter_by(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    deleted_post.delete(synchronize_session=False)
    do.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=List[Post])
def update_posts(id: int,currentUser: int,updatedPost: PostCreate, do: Session = Depends(get_db)):
    update_post = do.query(models.Post).filter_by(models.Post.id == id)
    post = update_post.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    update_post.update(updatedPost.dict(), synchronize_session=False)
    do.commit()
    return update_post.first()


def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


@router.get("/posts/latest")
def get_latest_post():
    return {"post_detail": findPost(len(myPosts) - 1)}

