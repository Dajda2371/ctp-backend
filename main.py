import os
import models
from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.post.auth import login, register
from api.post import sites as post_sites, tasks as post_tasks
from api.get import users as get_users, sites as get_sites, tasks as get_tasks
from api.patch import users as patch_users

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/auth")
app.include_router(register.router, prefix="/auth")
app.include_router(get_users.router)
app.include_router(get_sites.router)
app.include_router(get_tasks.router)
app.include_router(post_sites.router)
app.include_router(post_tasks.router)
app.include_router(patch_users.router)