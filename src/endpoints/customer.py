from fastapi import APIRouter, UploadFile
from fastapi import Query
from fastapi.responses import FileResponse
from src.models.customer import Customer,CustomerUpdate,CustomerBase,CustomerController
import os

router = APIRouter(
    prefix="/customer",
    tags=["customer"],
    responses={404: {"description": "Not found","Access-Control-Allow-Origin": "http://localhost:8081"}},

)

UPLOAD_FOLDER = "uploads"  # Change this to your desired folder path

# @router.get("/")
# async def read_root():
#     return [{"id": 1}]

"""
Read customer data by customer id index.
return into json format
"""
@router.get("/{id}")
async def read_customer(id:int):
    db_control=CustomerController()
    result=db_control.get_data(id)
    return result

"""
List customer.
return resturn customer list
"""
@router.get("/list_customer/")
async def list_customer():
    db_control=CustomerController()
    result=db_control.list_customer()
    return result

"""
Create new customer data to customers table
"""
@router.post("/add/")
async def add_customer(customer:CustomerBase):
    db_control=CustomerController()
    result=db_control.add_customer(customer.dict())
    return result

"""
Modify data on customers table by post method from pydantic class [Customer]
"""
@router.put("/update/")
async def update_customer(customer:CustomerUpdate):
    db_control=CustomerController()
    result=db_control.update_customer(customer.dict())
    # result=db_control.update(customer.dict(),id)
    return result


"""
Delete from customers table by id

"""
@router.get("/delete/{id}")
async def delete_customer(id):
    db_control=CustomerController()

    picture=db_control.get_picture_by_id(int(id))#Get picture from id
    if(len(picture)>0):
        db_control.delete_picture(UPLOAD_FOLDER,picture)

    result=db_control.delete(id)

    return result

"""
Search customer data by keyword with [SELECT] statement.
"""
@router.get("/search/{keyword}/{province}")
async def search_customer(keyword,province):
    db_control=CustomerController()
    result=db_control.search_data(keyword,province)
    return result

"""
List customer code from keyword
"""
@router.get("/list_customer_by_keyword/{keyword}")
async def list_customer_by_keyword(keyword):
    db_control=CustomerController()
    results=db_control.list_customer_by_keyword(keyword)
    return results

"""
query data and limit.
"""
@router.get("/query_limit/{limit}")
async def query_limit(limit=100):
    db_control=CustomerController()
    result=db_control.query_limit(limit)
    return result

@router.get("/get_sumary_by_product/{customer_code}")
async def get_sumary_by_product_type(customer_code):
    db_control=CustomerController()
    result=db_control.get_sumary_by_product_type(customer_code)
    return result

@router.get("/get_sumary_by_month/{customer_code}")
async def get_sumary_by_month(customer_code):
    db_control=CustomerController()
    result=db_control.get_sumary_by_month(customer_code)
    return result

@router.post("/upload_and_rename/{new_file_name}")
async def upload_and_rename_file(file: UploadFile,new_file_name):
    try:
        # arr = new_file_name.split
        # customer_code=arr[0]
        # db_control=CustomerController()
        # result=db.update_picture(new_file_name,customer_code)

        # Create the folder if it doesn't exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        # Generate a new file name (e.g., using a timestamp or a unique ID)
        #new_file_name =new_filename  # Change this to your desired new file name
        # Combine the folder path with the new file name to create the full file path
        file_path = os.path.join(UPLOAD_FOLDER, new_file_name)
        # Save the uploaded file to a temporary location
        with open(file_path, "wb") as temp_file:
            temp_file.write(file.file.read())
        return {"message": "File uploaded and renamed successfully","file_path": file_path,"file_name":new_file_name,"is_exist":True,}
    except Exception as e:
        return {"error": str(e)}

@router.get("/update_picture/{file_name}/{customer_code}")
async def update_picture(file_name,customer_code):
    db_control=CustomerController()
    result=db_control.update_picture(file_name,customer_code)
    return result

@router.get("/get_last_id/")
async def get_last_id():
    db_control=CustomerController()
    result=db_control.get_last_id()
    return result

@router.get("/get_customer_code/{id}")
async def get_customer_code(id):
    db_control=CustomerController()
    result=db_control.get_customer_code(id)
    return result

@router.get("/get_picture/{image_name}")
async def get_picture(image_name: str):
    try:
        image_path = os.path.join(UPLOAD_FOLDER, image_name)
        #image_path = os.path.join(UPLOAD_FOLDER, "User.jpg")
        if os.path.exists(image_path):
            file_obj=FileResponse(image_path, media_type="image/jpeg")
        else:
            image_path = os.path.join(UPLOAD_FOLDER, "User.jpg")
            file_obj=FileResponse(image_path, media_type="image/jpeg")
        return file_obj
    except Exception as e:

        return {"error": str(e)}
