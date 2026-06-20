from fastapi import APIRouter, Depends, status
from app.controllers.auth import AuthController
from app.schemas.auth import LoginRequest, RefreshRequest
from app.routers.deps import get_auth_controller

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    payload: LoginRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Authenticate user credentials and issue access/refresh tokens."""
    return controller.login(payload)

@auth_router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh(
    payload: RefreshRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Exchange a valid refresh token for new access and refresh tokens."""
    return controller.refresh(payload)

@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    payload: RefreshRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Revoke a refresh token, logging the user out of the current session."""
    return controller.logout(payload)
