from fastapi import APIRouter
from fastapi import Query
from src.models.preparedSale import PreparedSale,PreparedSaleController

router = APIRouter(
    prefix="/preparedSale",
    tags=["preparedSale"],
    responses={404: {"description": "Not found"}},
)



@router.get("/")
async def read_root():
    return [{"id": 1}]


@router.get("/{id}")
async def read_prepared(id:int):
    db_control=PreparedSaleController()
    fields=["id","lot_id","quantity","prepared_sale_date"]
    result=db_control.get_data(fields,id)
    return result


@router.get("/migrate_prepared/{lot_id}")
async def migrate_prepared(lot_id):
    db_control=PreparedSaleController()
    result=db_control.migrate_prepared(lot_id)
    return result


@router.get("/cancel_prepared/{id}")
async def cancel_prepared(id):
    db_control=PreparedSaleController()
    result=db_control.cancel_prepared(id)
    return result


@router.get("/search_data/{keyword}")
async def search_data(keyword):
    db_control=PreparedSaleController()
    result=db_control.search_data(keyword)
    return result
