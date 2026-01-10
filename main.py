import os
import models
from database import engine
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from api.post.auth import login, register, me
from api.post import sites as post_sites, tasks as post_tasks, users as post_users
from api.get import users as get_users, sites as get_sites, tasks as get_tasks
from api.patch import users as patch_users, sites as patch_sites, tasks as patch_tasks
from api.delete import sites as delete_sites, tasks as delete_tasks, users as delete_users
from api.put import users as put_users, tasks as put_tasks

app = FastAPI()

METHOD_ORDER = {
    "get": 0,
    "post": 1,
    "patch": 2,
    "put": 3,
    "delete": 4,
}

def use_first_path_segment_as_tag(app: FastAPI):
    for route in app.routes:
        if isinstance(route, APIRoute):
            path = route.path.lstrip("/")
            if not path:
                continue

            first_segment = path.split("/")[0]
            route.tags = route.tags or [first_segment]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    ordered_paths = {}

    # 1. Sort paths alphabetically
    for path in sorted(schema["paths"].keys()):
        methods = schema["paths"][path]

        # 2. Sort methods by explicit HTTP priority
        ordered_methods = dict(
            sorted(
                methods.items(),
                key=lambda item: METHOD_ORDER.get(item[0], 99)
            )
        )

        ordered_paths[path] = ordered_methods

    schema["paths"] = ordered_paths
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi

@app.on_event("startup")
def configure_swagger_tags():
    use_first_path_segment_as_tag(app)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/auth")
app.include_router(register.router, prefix="/auth")
app.include_router(me.router, prefix="/auth")
app.include_router(get_users.router)
app.include_router(get_sites.router)
app.include_router(get_tasks.router)
app.include_router(post_sites.router)
app.include_router(post_tasks.router)
app.include_router(post_users.router)
app.include_router(patch_users.router)
app.include_router(patch_sites.router)
app.include_router(patch_tasks.router)
app.include_router(delete_sites.router)
app.include_router(delete_tasks.router)
app.include_router(delete_users.router)
app.include_router(put_users.router)
app.include_router(put_tasks.router)