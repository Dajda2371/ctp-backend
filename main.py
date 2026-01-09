import os
from fastapi import FastAPI
from api.post.auth import login

app = FastAPI()

app.include_router(login.router, prefix="/auth")