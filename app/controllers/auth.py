from app.interfaces.auth import AuthServiceInterface
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.utils.response import APIResponse

class AuthController:
    def __init__(self, service: AuthServiceInterface):
        self.service = service

    def login(self, payload: LoginRequest) -> APIResponse:
        user = self.service.authenticate_user(payload.email, payload.password)
        access_token, refresh_token, role = self.service.create_session(user)
        
        token_data = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=role
        )
        return APIResponse.ok(data=token_data, message="Login successful")

    def refresh(self, payload: RefreshRequest) -> APIResponse:
        access_token, refresh_token, role = self.service.refresh_session(payload.refresh_token)
        
        token_data = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=role
        )
        return APIResponse.ok(data=token_data, message="Token refreshed successfully")

    def logout(self, payload: RefreshRequest) -> APIResponse:
        self.service.revoke_session(payload.refresh_token)
        return APIResponse.ok(message="Logout successful")
