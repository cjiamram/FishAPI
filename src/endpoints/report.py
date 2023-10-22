from fastapi import APIRouter
from fastapi import Query
from typing import Optional
from src.models.report import Report



router = APIRouter(
    prefix="/report",
    tags=["report"],
    responses={404: {"description": "Not found"}},
)


@router.get("/report_sub_total_sale/{customer_code}")
async def report_sub_total_sale(customer_code):
    db_control=Report()
    start_length=90
    segment=20
    results=db_control.report_sub_total_sale(customer_code,start_length,segment)
    return results

@router.get("/report_subtotal_item/{item_code}")
async def report_subtotal_item(item_code):
    db_control=Report()
    start_length=90
    segment=10
    results=db_control.report_subtotal_item(item_code,start_length,segment)
    return results

#get_sale_pie_by_customer_code(self,customer_code,start_length)
@router.get("/get_sale_pie_by_customer_code/{customer_code}")
async def get_sale_pie_by_customer_code(customer_code):
    db_control=Report()
    start_length=90
    results=db_control.get_sale_pie_by_customer_code(customer_code,start_length)
    return results
