from fastapi import APIRouter
from fastapi import Query
from src.models.deposit import DepositController,DepositBase
from src.models.Item import ItemController as Item 


from typing import Optional

router = APIRouter(
    prefix="/deposit",
    tags=["deposit"],
    responses={404: {"description": "Not found"}},
)



@router.get("/{id}")
async def read_data(id):
    db_control=DepositController()
    result=db_control.get_data(id)
    return result


@router.post("/add_deposit_item/")
async def add_item(deposit:DepositBase):
    db_control=DepositController()
    result=db_control.add_deposit_item(deposit.dict())
    # item_code=deposit.item_code
    # is_change_cost=Item.set_current_cost(item_code)
    # result["is_change_code"]=is_change_cost
    item=Item()
    is_change= item.update_item_cost(deposit.item_code) 
    result["is_change"]=is_change
    return result

@router.get("/cancel_deposit_item/{id}")
async def cancel_deposit_item(id):
    db_control=DepositController()
    result=db_control.cancel_deposit_item(id)
    return result

@router.get("/search_deposit/{keyword}")
async def search_deposit(keyword):
    db_control=DepositController()
    result=db_control.search_data(keyword)
    return result
