from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/createPost")
def createPost(newPost: Post):
    return {"data": f"title: {newPost.title}, content: {newPost.content}, published: {newPost.published}, rating: {newPost.rating}"}
