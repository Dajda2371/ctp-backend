import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.options.auth import login

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/auth")