from pydantic import BaseModel

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str
