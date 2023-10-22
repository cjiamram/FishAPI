from fastapi import APIRouter
from fastapi import Query
from src.models.product import Product,ProductBase,ProductController

router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root():
    return [{"id": 1}]


@router.get("/{id}")
async def read_product(id:int):
    db_control=ProductController()

    result=db_control.get_data(id)
    return result


@router.post("/add/")
async def add_product(product:ProductBase):
    db_control=ProductController()
    result=db_control.add_product(product.dict())
    return result

@router.put(" /update/{id}")
async def update_product(product:Product,id):
    db_control=ProductController()
    result=db_control.update(product.dict(),id)
    return result

@router.post("/update_price/{product_id}")
async def update_price(elements:dict,product_id):
    db_control=ProductController()
    result=db_control.update_price(elements,product_id)
    return result


@router.post("/update_qty/{product_id}")
async def update_price(elements:dict,product_id):
    db_control=ProductController()
    result=db_control.update_qty(elements,product_id)
    return result

@router.get("/get_qty/{id}")
async def get_qty(id):
    db_control=ProductController()
    sql="SELECT quantity \
        FROM products WHERE id=%s"
    params=(int(id),)
    result=db_control.get_qty(sql,params)

    return result

@router.get("/get_price/{id}")
async def get_price(id):
    db_control=ProductController()
    sql="SELECT price FROM products WHERE id=%s"
    params=(int(id),)
    result=db_control.get_price(sql,params)
    return result

@router.get("/get_price_by_productcode/{product_code}")
async def get_price_by_productcode(product_code):
    db_control=ProductController()
    sql="SELECT price FROM products WHERE product_code=%s"
    result=db_control.get_price_by_productcode(product_code)
    return result


@router.get("/delete/{id}")
async def delete_product(id):
    db_control=ProductController()
    result=db_control.delete(id)
    return result

@router.get("/search/{keyword}")
async def search_product(keyword):
    fields=["id","product_code","product","quantity","price"]
    params=('%'+keyword+'%',)
    sql="SELECT \
            id,\
            product_code,\
            product,\
            quantity,\
            price \
        FROM products \
        WHERE \
        CONCAT(product_code,' ',product) LIKE %s"
    db_control=ProductController()
    result=db_control.search_data(sql,fields,params)
    return result
