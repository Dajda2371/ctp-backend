from pydantic import BaseModel

class UserAuth(BaseModel):
    email: str
    password: str
    name: str = None
    role: str = "technician"
