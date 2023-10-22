from fastapi import APIRouter
from fastapi import Query
from src.models.Item import Item
from src.models.Item import Item,ItemBase,ItemController

router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root():
    return [{"id": 1}]

@router.get("/{id}")
async def read_item(id:int):
    db_control=ItemController()
    #fields=["id","item_code","item_name","quantity","cost","status"]
    result=db_control.get_data(id)
    return result

@router.get("/get_data_by_itemcode/{item_code}")
async def get_data_by_itemcode(item_code):
    db_control=ItemController()
    result=db_control.get_data_by_itemcode(item_code)
    return result


@router.post("/add/")
async def add_item(item:ItemBase):
    db_control=ItemController()
    result=db_control.add_item(item.dict())
    return result

@router.put("/update/{id}")
async def update_item(item:Item,id):
    db_control=ItemController()
    result=db_control.update_item(item.dict(),id)
    return result

@router.get("/delete/{id}")
async def delete_item(id):
    db_control=ItemController()
    result=db_control.delete(id)
    return result

@router.put("/update_cost/{id}")
async def update_price(elements:dict,id):
    db_control=ItemController()
    result=db_control.update_cost(elements,id)
    return result

@router.get("/get_qty/{id}")
async def get_qty(id):
    db_control=ItemController()
    sql="SELECT quantity FROM items WHERE id=%s"
    params=(int(id),)
    result=db_control.get_qty(sql,params)

    return result

@router.get("/get_cost/{id}")
async def get_cost(id):
    db_control=ItemController()
    sql="SELECT cost FROM items WHERE id=%s"
    params=(int(id),)
    result=db_control.get_cost(sql,params)
    return result

@router.put("/update_qty/{id}")
async def update_qty(elements:dict,id):
    db_control=ItemController()
    result=db_control.update_qty(elements,id)
    return result

@router.put("/update_cost/{id}")
async def update_cost(elements:dict,id):
    db_control=ItemController()
    result=db_control.update_cost(elements,id)
    return result


@router.get("/search_item/{keyword}")
async def search_item(keyword):
    db_control=ItemController()
    results=db_control.search_item(keyword)
    return results

@router.get("/get_unit/")
async def get_unit():
    db_control=ItemController()
    results=db_control.get_unit()
    return results
