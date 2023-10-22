from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB

class ProvinceController():
    def get_provinces():
        db=DB()
        sql="SELECT id,\
            province_code,\
            province_name \
        FROM provinces ORDER BY province_name "
        results=db.get_specific_sql(sql,None,None)
        return results
