from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
from auth.jwt_handler import decode_access_token
from auth.users import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_active_user(token: str = Depends(oauth2_scheme)):
    """
    Return user object if token valid. Otherwise raise 401.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User disabled")
    # attach role available in payload too if needed
    return user

def require_role(role: str) -> Callable:
    """
    Dependency generator: require_role('peminjam') -> use as Depends(require_role('peminjam'))
    """
    def role_checker(user = Depends(get_current_active_user)):
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: insufficient role")
        return user
    return role_checker

def allow_roles(*roles: str):
    """
    Dependency generator that allows any of listed roles
    """
    def checker(user = Depends(get_current_active_user)):
        if user.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden: insufficient role")
        return user
    return checker
