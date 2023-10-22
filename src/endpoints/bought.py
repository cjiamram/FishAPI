from fastapi import APIRouter
from fastapi import Query
from src.models.bougth import Bought,BoughtModel,BoughtController
from typing import Optional

router = APIRouter(
    prefix="/bought",
    tags=["bought"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root():
    return [{"id": 1}]

@router.get("/{bought_id}")
async def read_bought(bought_id:int):
    return {"id":bought_id}

@router.post("/add/")
async def add_bought(bought:BoughtModel):
    db_control=BoughtController()
    result=db_control.create(bought.dict())
    return result


@router.post("/update/{id}")
async def update_bought(bought:BoughtModel,id):
    db_control=BoughtController()
    result=db_control.update(bought.dict(),id)
    return result

@router.get("/delete/{id}")
async def delete_bought(id):
    db_control=BoughtController()
    result=db_control.delete(id)
    return result

@router.get("/search_before_migrate/")
async def search_before_migrate():
    db_control=BoughtController()
    result=db_control.search_before_migrate()
    return result

@router.get("/search/{keyword}/{status}")
async def search_bought(keyword,status=0):
    db_control=BoughtController()
    result=db_control.search_data(keyword,status)
    return result
