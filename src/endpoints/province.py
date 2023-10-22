from fastapi import APIRouter
from fastapi import Query
from typing import Optional
from src.models.province import ProvinceController

router = APIRouter(
    prefix="/province",
    tags=["province"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_provinces/")
async def get_provinces():
    return ProvinceController.get_provinces()
