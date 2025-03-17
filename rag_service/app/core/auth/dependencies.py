from typing import Generator, Optional
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt, JWTError

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.USER_SERVICE_URL}{settings.API_V1_STR}/auth/login"
)


class User(BaseModel):
    id: int
    email: str
    is_active: bool
    is_superuser: bool
    full_name: Optional[str] = None


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user by validating the token with the user service.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Call the user service to validate the token
        response = requests.get(
            f"{settings.USER_SERVICE_URL}{settings.API_V1_STR}/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise credentials_exception
        
        user_data = response.json()
        return User(**user_data)
    except Exception:
        raise credentials_exception


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def check_user_permission(action: str, resource: str):
    """
    Check if the user has the required permission for the requested operation.
    """
    def check_permission_dependency(
        token: str = Depends(oauth2_scheme)
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
        
        try:
            # Call the user service to check permissions
            response = requests.post(
                f"{settings.USER_SERVICE_URL}{settings.API_V1_STR}/permissions/check",
                json={"action": action, "resource": resource},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                raise credentials_exception
            
            # If the response is successful, return the user
            user_data = response.json().get("user")
            return User(**user_data)
        except Exception:
            raise credentials_exception
    
    return check_permission_dependency 