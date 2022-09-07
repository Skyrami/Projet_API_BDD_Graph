from fastapi import APIRouter

router = APIRouter(
    prefix="/datascientest/lifeproject",
    tags=["status"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ping")
async def ping():
    return 1


@router.get("/healthcheck")
async def healthcheck():
    return 1
