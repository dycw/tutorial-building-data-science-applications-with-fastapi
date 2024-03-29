from chapter03.project.routers import posts
from chapter03.project.routers import users
from fastapi import FastAPI


app = FastAPI()
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(users.router, prefix="/users", tags=["users"])
