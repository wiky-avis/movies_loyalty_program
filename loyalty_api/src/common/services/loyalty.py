import logging
from http import HTTPStatus

from fastapi import HTTPException
from src.api.models.promo import PromoInput
from src.common.exceptions import DatabaseError
from src.common.promo import get_promo_code
from src.common.repositories.loyalty import LoyaltyRepository


logger = logging.getLogger(__name__)


class LoyaltyService:
    def __init__(
        self,
        repository: LoyaltyRepository,
    ):
        self._repository = repository

    async def create_promo(self, data: PromoInput) -> dict:
        try:
            promo_code = get_promo_code()
        except Exception:
            logger.error(
                "Failed to generate a secret promo code: data",
                data.dict(),
                exc_info=True,
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to get a promo code.",
            )
        try:
            promo = await self._repository.create_promo(data, promo_code)
        except DatabaseError:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="Failed to create a new promo.",
            )
        return promo
