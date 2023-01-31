import time
from random import randrange
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from websockets.http11 import Response
from psycopg2 import *
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine, SessionLocal, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: True
    # rating: Optional[int] = None


@app.get("/sqlalchemy")
def test_posts(do: Session = Depends(get_db)):

    posts = do.query(models.Post).all()

    return {"status": posts}

while True:
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='password123',
            cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database connection was succesfully")
        break
    except Exception as error:
        print("Connection to database failed")
        print(f"Error {error} ")
        time.sleep(2)

myPosts = [
    {"title": "title 1", "content": "content 1", "id": 1},
    {"title": "title 2", "content": "content 2", "id": 2}
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/posts")
def get_posts(do: Session = Depends(get_db)):
    posts = do.query(models.Post).all()
    return {"data": posts}


@app.post("/createPost", status_code=status.HTTP_201_CREATED)
def createPost(newPost: Post, do: Session = Depends(get_db)):
    # postNew = models.Post(title = newPost.title, content = newPost.content,published = newPost.published)
    postNew = models.Post(**newPost.dict())

    do.add(postNew)
    do.commit()
    do.refresh(postNew)

    return {"data": postNew}


@app.get("/posts/{id}")
def get_posts(id: int, do: Session = Depends(get_db)):
    post = do.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return {"post_detail": post}


def find_index_id(id: int):
    for i, p in enumerate(myPosts):
        if (p['id'] == id):
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, do: Session = Depends(get_db)):

    deleted_post =do.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    deleted_post.delete(synchronize_session=False)
    do.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, do: Session = Depends(get_db)):
    update_post = do.query(models.Post).filter_by(models.Post.id == id)
    post = update_post.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    update_post.update(post.__dict__, synchronize_session=False)
    do.commit()
    return {"data": update_post.first()}


def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


@app.get("/posts/latest")
def get_latest_post():
    return {"post_detail": findPost(len(myPosts) - 1)}
