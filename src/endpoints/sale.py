from fastapi import APIRouter
from fastapi import Query
from typing import Optional
from datetime import  datetime
from src.models.sale import SaleBase,Sale,SaleController

router = APIRouter(
    prefix="/sale",
    tags=["sale"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root():
    return [{"id": 1}]

@router.get("/{id}")
async def read_sale_data(id):
    db_control=SaleController()
    fields=["id","product_code","customer_code","price","quantity","created_at","updated_at"]
    result=db_control.get_data(fields,id)
    return result

@router.get("/gen_code/")
async def gen_code():
    db_control=SaleController()
    current_date = datetime.now()
    # Format the current date to YYMM
    yymm = current_date.strftime('%y%m')
    result=db_control.gen_code(yymm)
    return result

@router.get("/update_sale_code/")
async def update_sale_code():
    db_control=SaleController()
    current_date = datetime.now()
    # Format the current date to YYMM
    yymm = current_date.strftime('%y%m')
    result=db_control.update_sale_code(yymm)
    return result

@router.post("/sale_product/")
async def sale_product(sale:Sale):
    db_control=SaleController()
    result=db_control.sale_product(sale.dict())
    return result

@router.get("/cancel_sale/{id}")
async def cancel_sale(id):
    db_control=SaleController()
    result=db_control.cancel_sale(id)
    return result

@router.get("/get_sale_transaction/{keyword}")
async def get_sale_transaction(keyword):
    db_control=SaleController()
    result=db_control.get_sale_transaction(keyword)
    return result
