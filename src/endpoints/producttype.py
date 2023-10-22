from fastapi import APIRouter
from fastapi import Query
from typing import Optional
from src.models.producttype import ProductTypeController,ProductType

router = APIRouter(
    prefix="/productiontype",
    tags=["productiontype"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_type_by_code/{type_code}")
async def get_type_by_code(type_code):
    db_control=ProductTypeController()
    result=db_control.get_type_by_code(type_code)
    return result


@router.get("/get_data/{id}")
async def get_data(id):
    db_control=ProductTypeController()
    fields={"description"}
    result=db_control.get_data(fields,id)
    return result



@router.get("/list_product_types/")
async def list_product_types():
    db_control=ProductTypeController()
    results=db_control.list_product_types()
    return results

@router.get("/{product_type_id}")
async def read_bought(product_type_id:int):

    return {"id":product_type_id}

@router.post("/add/")
async def add_type(productType:ProductType):
    db_control=ProductTypeController()
    result=db_control.create(productType.dict())
    return result

@router.post("/update/{id}")
async def update_type(productType:ProductType,id):
    db_control=ProductTypeController()
    result=db_control.update(productType.dict(),id)
    return result
# def get_type_by_code(self,type_code):
