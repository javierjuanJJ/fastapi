import time
from random import randrange
from typing import Optional

import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status
from websockets.http11 import Response
from psycopg2 import *
from psycopg2.extras import RealDictCursor
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: True
    # rating: Optional[int] = None


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
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/createPost", status_code=status.HTTP_201_CREATED)
def createPost(newPost: Post):
    cursor.execute(
        """INSERT INTO posts
        (title, content, published)
         VALUES 
         (%s, %s, %s) RETURNING *""",
        (
            newPost.title,
            newPost.content,
            newPost.published
        )
    )

    postNew = cursor.fetchone()

    connection.commit()

    return {"data": postNew}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute(
        """SELECT * FROM posts WHERE id = %s""",
        (
            str(id)
        )
    )
    post = cursor.fetchone()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return {"post_detail": post}


def find_index_id(id: int):
    for i, p in enumerate(myPosts):
        if (p['id'] == id):
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""",
        (
            str(id)
        )
    )

    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE ID = %s RETURNING *""",
        (
            post.title,
            post.content,
            post.published,
            str(id)
        )
    )

    update_post = cursor.fetchone()
    connection.commit()

    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    return {"data": update_post}


def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


@app.get("/posts/latest")
def get_latest_post():
    return {"post_detail": findPost(len(myPosts) - 1)}
