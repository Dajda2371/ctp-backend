import os
import http
import models
from database import engine
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import logging
import time
from starlette.responses import Response


from api.get import users as get_users, sites as get_sites, tasks as get_tasks
from api.get.auth import me as get_me
from api.get.tasks import task_id as get_tasks_id_pkg, my_tasks as get_tasks_my
from api.get.tasks.task_id import get_task as get_tasks_id
from api.get.tasks.task_id import site_id as get_tasks_id_site, title as get_tasks_id_title, description as get_tasks_id_description, status as get_tasks_id_status, priority as get_tasks_id_priority, assignee as get_tasks_id_assignee, due_date as get_tasks_id_due_date, latitude as get_tasks_id_latitude, longitude as get_tasks_id_longitude, photos as get_tasks_id_photos
from api.get.tasks.task_id.photos import photo_index as get_tasks_id_photos_item

from api.get.sites import site_id as get_sites_id_pkg
from api.get.sites.site_id import get_site as get_sites_id
from api.get.sites.site_id import name as get_sites_id_name, address as get_sites_id_address, latitude as get_sites_id_latitude, longitude as get_sites_id_longitude, property_manager as get_sites_id_property_manager, facility_manager as get_sites_id_facility_manager

from api.get.users import user_id as get_users_id_pkg
from api.get.users.user_id import get_user as get_users_id
from api.get.users.user_id import email as get_users_id_email, name as get_users_id_name, role as get_users_id_role
from api.get.users import possible_facility_managers as get_users_possible_fm, possible_property_managers as get_users_possible_pm

from api.post import sites as post_sites, tasks as post_tasks, users as post_users
from api.post.auth import login, register, change_password, logout
from api.post.tasks.task_id import photos as post_tasks_id_photos

from api.patch.users import user_id as patch_users_id
from api.patch.sites import site_id as patch_sites_id
from api.patch.tasks import task_id as patch_tasks_id

from api.delete.sites import site_id as delete_sites_id
from api.delete.users import user_id as delete_users_id
from api.delete.tasks import task_id as delete_tasks_id_pkg
from api.delete.tasks.task_id import delete_task as delete_tasks_id, assignee as delete_tasks_id_assignee, description as delete_tasks_id_description, due_date as delete_tasks_id_due_date, photos as delete_tasks_id_photos
from api.delete.tasks.task_id.photos import photo_index as delete_tasks_id_photos_item

from api.put.users import user_id as put_users_id_pkg
from api.put.users.user_id import role as put_users_id_role, name as put_users_id_name, email as put_users_id_email
from api.put.sites import site_id as put_sites_id_pkg
from api.put.sites.site_id import name as put_sites_id_name, address as put_sites_id_address, property_manager as put_sites_id_property_manager, facility_manager as put_sites_id_facility_manager, latitude as put_sites_id_latitude, longitude as put_sites_id_longitude
from api.put.tasks.task_id import site_id as put_tasks_id_site, title as put_tasks_id_title, description as put_tasks_id_description, status as put_tasks_id_status, priority as put_tasks_id_priority, assignee as put_tasks_id_assignee, due_date as put_tasks_id_due_date, latitude as put_tasks_id_latitude, longitude as put_tasks_id_longitude


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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Silence uvicorn access logger to avoid duplicates
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Determine if we should skip body logging (for binary data or photo endpoints)
    content_type = request.headers.get("content-type", "")
    is_binary_request = "multipart" in content_type or "image" in content_type
    is_photo_path = "/photos" in request.url.path

    body = b""
    if not (is_binary_request or is_photo_path):
        # Only read body for small, non-binary requests
        body = await request.body()
    
    # Replace the receive function so following handlers can read the body again
    async def receive():
        return {"type": "http.request", "body": body}
    
    if not (is_binary_request or is_photo_path):
        request._receive = receive

    # Process request
    response = await call_next(request)
    
    # Log Request Line
    status_code = response.status_code
    try:
        status_phrase = http.HTTPStatus(status_code).phrase
    except ValueError:
        status_phrase = ""
    
    COLOR_RESET = "\033[0m"
    COLOR_METHOD = "\033[94m"
    COLOR_PATH = "\033[97m"
    COLOR_STATUS = "\033[92m" if status_code < 300 else "\033[93m" if status_code < 400 else "\033[91m"
    
    client_host = request.client.host if request.client else "unknown"
    client_port = request.client.port if request.client else "0"
    relative_path = request.url.path + (f"?{request.url.query}" if request.url.query else "")
    
    logger.info(f"{client_host}:{client_port} - \"{COLOR_METHOD}{request.method}{COLOR_RESET} {COLOR_PATH}{relative_path}{COLOR_RESET} HTTP/{request.scope.get('http_version', '1.1')}\" {COLOR_STATUS}{status_code} {status_phrase}{COLOR_RESET}")

    # Log Request Body
    if not (is_binary_request or is_photo_path):
        request_body_str = body.decode('utf-8', errors='ignore') if body else "<no request body>"
        logger.info(f"{request_body_str}")
    else:
        logger.info(f"<binary or multipart data omitted from log>")

    # Handle Response Body logging (Skip for photos/binary to prevent freezing)
    response_content_type = response.headers.get("content-type", "")
    if "image" in response_content_type or is_photo_path:
        logger.info(f"Response Body: <binary photo content omitted from log>")
        return response
    
    # For normal JSON/Text responses, we still log the body
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    
    if response_body:
        logger.info(f"Response Body: {response_body.decode('utf-8', errors='ignore')}")
    
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

@app.on_event("startup")
def configure_swagger_tags():
    from migration import migrate_db
    migrate_db()
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
app.include_router(get_users_possible_fm.router)
app.include_router(get_users_possible_pm.router)
app.include_router(get_users_id.router)
app.include_router(get_users_id_email.router)
app.include_router(get_users_id_name.router)
app.include_router(get_users_id_role.router)

app.include_router(get_sites.router)
app.include_router(get_sites_id.router)
app.include_router(get_sites_id_name.router)
app.include_router(get_sites_id_address.router)
app.include_router(get_sites_id_latitude.router)
app.include_router(get_sites_id_longitude.router)
app.include_router(get_sites_id_property_manager.router)
app.include_router(get_sites_id_facility_manager.router)

app.include_router(get_tasks.router)
app.include_router(get_tasks_my.router)
app.include_router(get_tasks_id.router)
app.include_router(get_tasks_id_site.router)
app.include_router(get_tasks_id_title.router)
app.include_router(get_tasks_id_description.router)
app.include_router(get_tasks_id_status.router)
app.include_router(get_tasks_id_priority.router)
app.include_router(get_tasks_id_assignee.router)
app.include_router(get_tasks_id_due_date.router)
app.include_router(get_tasks_id_latitude.router)
app.include_router(get_tasks_id_longitude.router)
app.include_router(get_tasks_id_photos.router)
app.include_router(get_tasks_id_photos_item.router)
app.include_router(post_sites.router)
app.include_router(post_tasks.router)
app.include_router(post_tasks_id_photos.router)
app.include_router(post_users.router)
app.include_router(patch_users_id.router)
app.include_router(patch_sites_id.router)
app.include_router(patch_tasks_id.router)
app.include_router(delete_sites_id.router)
app.include_router(delete_tasks_id.router)
app.include_router(delete_tasks_id_assignee.router)
app.include_router(delete_tasks_id_description.router)
app.include_router(delete_tasks_id_due_date.router)
app.include_router(delete_tasks_id_photos.router)
app.include_router(delete_tasks_id_photos_item.router)
app.include_router(delete_users_id.router)
app.include_router(put_users_id_role.router)
app.include_router(put_users_id_name.router)
app.include_router(put_users_id_email.router)
app.include_router(put_tasks_id_site.router)
app.include_router(put_tasks_id_title.router)
app.include_router(put_tasks_id_description.router)
app.include_router(put_tasks_id_status.router)
app.include_router(put_tasks_id_priority.router)
app.include_router(put_tasks_id_assignee.router)
app.include_router(put_tasks_id_due_date.router)
app.include_router(put_tasks_id_latitude.router)
app.include_router(put_tasks_id_longitude.router)
app.include_router(put_sites_id_name.router)
app.include_router(put_sites_id_address.router)
app.include_router(put_sites_id_property_manager.router)
app.include_router(put_sites_id_facility_manager.router)
app.include_router(put_sites_id_latitude.router)
app.include_router(put_sites_id_longitude.router)