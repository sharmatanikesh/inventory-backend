from fastapi import APIRouter, Depends
from app.schemas.dashboard import DashboardSummaryResponse
from app.utils.response import APIResponse
from app.controllers.dashboard import DashboardController
from app.routers.deps import get_dashboard_controller, get_current_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=APIResponse[DashboardSummaryResponse])
def get_dashboard_summary(
    controller: DashboardController = Depends(get_dashboard_controller),
    current_admin = Depends(get_current_admin)
) -> APIResponse[DashboardSummaryResponse]:
    return controller.get_summary()

