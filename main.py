from fastapi import FastAPI

app = FastAPI()


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
def createPost():
    return {"createPost": "Succesfully created posts"}
