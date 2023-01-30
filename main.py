from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status
from websockets.http11 import Response

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: True
    rating: Optional[int] = None


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
    return {"data": myPosts}


@app.post("/createPost", status_code=status.HTTP_201_CREATED)
def createPost(newPost: Post):
    post_dict = newPost.dict()
    post_dict['id'] = randrange(1, 100000)
    myPosts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_posts(id: int):
    post = findPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return {"post_detail": post}


def find_index_id(id: int):
    for i, p in enumerate(myPosts):
        if (p['id'] == id):
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_index_id(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    myPosts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    index = find_index_id(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    myPosts[index] = post_dict

    return {"data": post_dict}


def findPost(id):
    for p in myPosts:
        if p["id"] == id:
            return p


@app.get("/posts/latest")
def get_latest_post():
    return {"post_detail": findPost(len(myPosts) - 1)}
