import os
import models
from database import engine
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi


from api.get import users as get_users, sites as get_sites, tasks as get_tasks
from api.get.tasks import task_id as get_tasks_id_pkg
from api.get.tasks.task_id import get_task as get_tasks_id
from api.get.tasks.task_id import site_id as get_tasks_id_site, title as get_tasks_id_title, description as get_tasks_id_description, status as get_tasks_id_status, priority as get_tasks_id_priority, assignee as get_tasks_id_assignee, due_date as get_tasks_id_due_date, photos as get_tasks_id_photos
from api.get.auth import me as get_me

from api.post import sites as post_sites, tasks as post_tasks, users as post_users
from api.post.auth import login, register, change_password, logout
from api.post.tasks.task_id import photos as post_tasks_id_photos

from api.patch import users as patch_users, sites as patch_sites
from api.patch.tasks import task_id as patch_tasks_id

from api.delete import sites as delete_sites, users as delete_users
from api.delete.tasks import task_id as delete_tasks_id_pkg
from api.delete.tasks.task_id import delete_task as delete_tasks_id
from api.delete.tasks.task_id import assignee as delete_tasks_id_assignee, description as delete_tasks_id_description, due_date as delete_tasks_id_due_date, photos as delete_tasks_id_photos
from api.delete.tasks.task_id.photos import photo_index as delete_tasks_id_photos_item

from api.put import users as put_users, sites as put_sites
from api.put.tasks.task_id import site_id as put_tasks_id_site, title as put_tasks_id_title, description as put_tasks_id_description, status as put_tasks_id_status, priority as put_tasks_id_priority, assignee as put_tasks_id_assignee, due_date as put_tasks_id_due_date


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
app.include_router(get_me.router, prefix="/auth")
app.include_router(change_password.router, prefix="/auth")
app.include_router(logout.router, prefix="/auth")
app.include_router(get_users.router)
app.include_router(get_sites.router)
app.include_router(get_tasks.router)
app.include_router(get_tasks_id.router)
app.include_router(get_tasks_id_site.router)
app.include_router(get_tasks_id_title.router)
app.include_router(get_tasks_id_description.router)
app.include_router(get_tasks_id_status.router)
app.include_router(get_tasks_id_priority.router)
app.include_router(get_tasks_id_assignee.router)
app.include_router(get_tasks_id_due_date.router)
app.include_router(get_tasks_id_photos.router)
app.include_router(post_sites.router)
app.include_router(post_tasks.router)
app.include_router(post_tasks_id_photos.router)
app.include_router(post_users.router)
app.include_router(patch_users.router)
app.include_router(patch_sites.router)
app.include_router(patch_tasks_id.router)
app.include_router(delete_sites.router)
app.include_router(delete_tasks_id.router)
app.include_router(delete_tasks_id_assignee.router)
app.include_router(delete_tasks_id_description.router)
app.include_router(delete_tasks_id_due_date.router)
app.include_router(delete_tasks_id_photos.router)
app.include_router(delete_tasks_id_photos_item.router)
app.include_router(delete_users.router)
app.include_router(put_users.router)
app.include_router(put_tasks_id_site.router)
app.include_router(put_tasks_id_title.router)
app.include_router(put_tasks_id_description.router)
app.include_router(put_tasks_id_status.router)
app.include_router(put_tasks_id_priority.router)
app.include_router(put_tasks_id_assignee.router)
app.include_router(put_tasks_id_due_date.router)
app.include_router(put_sites.router)