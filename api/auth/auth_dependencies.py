from fastapi import Depends, FastAPI, HTTPException, status

from .auth_models import TokenData, User
from . import auth_helpers
from .auth_service import get_user

async def get_current_user(token_data: TokenData = Depends(auth_helpers.verify_access_token)):
    user = await get_user(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user details",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient access priviledges")
    return current_user