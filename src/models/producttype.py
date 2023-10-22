from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB

class ProductType(BaseModel):
    type_code:str
    description:str

class ProductTypeController():
    __tablename__="product_types"

    def create(self,productType):
        db=DB(self.__tablename__)
        result=db.create(productType)
        del db
        return result

    def update(self,productType,id):
        db=DB(self.__tablename__)
        result=db.update(productType,id)
        del db
        return result

    def delete(self,id):
        db=DB(self.__tablename__)
        result=db.delete(id)
        del db
        return result

    def get_data(self,fields,id):
        db=DB(self.__tablename__)
        result=db.get_data(fields,id)
        del db
        return result
    """
    type_code is dict
    """
    def get_type_by_code(self,type_code):
        db=DB()
        sql="SELECT type_code,description  FROM "+self.__tablename__+" WHERE type_code=%s"
        fields={"type_code","description"}
        params=(type_code,)
        result=db.get_specific_sql(sql,fields,params)
        if(len(result)>0):
            json_result={"Flag":True,"type_code":result[0]["type_code"],"description":result[0]["description"]}
            return json_result
        else:
            return {"Flag":False}

    def list_product_types(self):
        db=DB()
        sql="SELECT id,type_code,description FROM product_types "
        results=db.get_specific_sql(sql,None,None)
        return results

    def search_data(self,sql,fields,params):
        db=DB(self.__tablename__)
        results=db.search_data(sql,fields,params)
        del db
        return results
