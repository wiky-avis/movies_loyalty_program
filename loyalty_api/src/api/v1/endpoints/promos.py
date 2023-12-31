import dpath
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from src.api.models.promo import (
    GetPromoStatusInput,
    PromoActivateInput,
    PromoRestoreInput,
)
from src.common.decode_auth_token import get_decoded_data
from src.common.responses import ApiResponse, wrap_response
from src.common.services.promos import PromosService
from src.containers import Container
from starlette import status


router = APIRouter()


@router.post(
    "/promos/activate",
    summary="Применить промокод.",
    description="Ручка для применения/использования промокода/скидки.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_activate(
    user_data=Depends(get_decoded_data),
    body: PromoActivateInput = Body(...),
    promos_service: PromosService = Depends(Provide[Container.promos_service]),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await promos_service.promo_activate(body.promo_code, user_id)


@router.post(
    "/promos/restore",
    summary="Восстановить промокод.",
    description="Ручка для восстановления промокода/скидки.",
    response_model=ApiResponse,
)
@inject
@wrap_response
async def promo_restore(
    user_data=Depends(get_decoded_data),
    body: PromoRestoreInput = Body(...),
    promos_service: PromosService = Depends(Provide[Container.promos_service]),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await promos_service.promo_restore(body.promo_code, user_id)


@router.post(
    "/promos/status",
    summary="Получить статус возможности применения промокода.",
    description="Ручка для получения статуса возможности применения промокода/скидки. "
    "Используется фронтом для отображения 'зеленой галочки'",
    response_model=ApiResponse,
    dependencies=[Depends(RateLimiter(times=20, minutes=1))],
)
@inject
@wrap_response
async def get_promo_status(
    user_data=Depends(get_decoded_data),
    body: GetPromoStatusInput = Body(...),
    promos_service: PromosService = Depends(Provide[Container.promos_service]),
):
    user_id = dpath.get(user_data, "user_id", default=None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Undefined user.",
        )

    return await promos_service.get_promo_status(body.promo_code, user_id)
