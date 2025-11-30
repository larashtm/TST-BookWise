from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import timedelta
from typing import Dict

from auth.users import get_user_by_username, verify_password
from auth.jwt_handler import create_access_token, create_refresh_token
from auth.deps import get_current_active_user  # ← WAJIB DITAMBAHKAN

router = APIRouter(prefix="/auth", tags=["Authentication"])

REFRESH_TOKENS: Dict[str, str] = {}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        subject=str(user.user_id),
        role=user.role,
        expires_delta=timedelta(minutes=60)
    )
    refresh_token = create_refresh_token()

    REFRESH_TOKENS[refresh_token] = user.username

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(req: RefreshRequest):
    rt = req.refresh_token
    username = REFRESH_TOKENS.get(rt)

    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token(
        subject=str(user.user_id),
        role=user.role,
        expires_delta=timedelta(minutes=60)
    )

    new_rt = create_refresh_token()
    del REFRESH_TOKENS[rt]
    REFRESH_TOKENS[new_rt] = user.username

    return TokenResponse(access_token=access_token, refresh_token=new_rt)

@router.post("/logout")
def logout(req: RefreshRequest):
    rt = req.refresh_token
    if rt in REFRESH_TOKENS:
        del REFRESH_TOKENS[rt]
    return {"message": "Refresh token revoked"}

@router.get("/me")
def me(current_user = Depends(get_current_active_user)):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "role": current_user.role,
        "disabled": current_user.disabled
    }
