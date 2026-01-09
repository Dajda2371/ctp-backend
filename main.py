import os
from fastapi import FastAPI
from api.options.auth import login

app = FastAPI()

app.include_router(login.router, prefix="/auth")