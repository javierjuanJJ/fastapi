import time
import psycopg2
from fastapi import FastAPI, APIRouter
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import users, post

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(post.router)

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

