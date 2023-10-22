from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB

class BoughtModel(BaseModel):
    type_code:Optional[str]
    quantity:float
    price:float
    received_date:datetime=None
    status:int=0

class Bought(BoughtModel):
    created_at:datetime=None
    updated_at:datetime=None

class BoughtController():
    __tablename__="bougth"



    def create(self,bought):
        db=DB(self.__tablename__)
        del bougth["updated_at"]
        result=db.create(bought)
        del db
        return result

    # def icrement_item(self,quantity,item_code):
    #     db=DB()
    #     sql="UPDATE items SET quantity=quantity+% WHERE item_code=%s"
    #     params=(quantity,item_code,)
    #     result=db.set_specific_sql(sql,params)
    #     return result

    def update(self,bought,id):
        db=DB(self.__tablename__)
        del bought["created_at"]
        result=db.update(bought,id)
        del db
        return result

    def cancel_bought(self,id):
        quantity=self.get_quantity(id)
        cancel_from_item(quantity,id)
        result=self.delete(id)
        return result

    def cancel_from_item(self,quantity,id):
        db=DB()
        sql="UPDATE items SET quantity=quantity-%s WHERE id=%s";
        params=(float(quantity),int(id),)
        result=db.get_specific_sql(sql,params)
        return result


    def get_bought_item(self,id):
        db=DB()
        sql="SELECT \
            quantity,\
            price\
        FROM bougth\
        WHERE id=%s"
        params=(int(id),)
        result=db.get_specific_sql(sql,None,params)
        return result


    def get_quantity(self,id):
        db=DB()
        sql="SELECT \
            quantity\
        FROM bougth\
        WHERE id=%s"
        params=(int(id),)
        fields=["quantity"]
        result=db.get_specific_sql(sql,fields,params)
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

    def get_bought_status(id):
        db=DB()
        sql="SELECT id FROM bougth WHERE id=%s AND status=0"
        params=(id,)
        fields=["id"]
        result=db.get_specific_sql(sql,fields,params)
        if(len(result)>0):
             return {"Flag":True}
        else:
            return {"Flag":False}

    def set_status(status,id):
        db=DB()
        sql="UPDATE bougth SET status=%s WHERE id=%s"
        params=(status,id,)
        result=db.set_specific_sql(sql,params)
        return result

    def set_status_by_producttype(status,type_code):
        db=DB()
        sql="UPDATE bougth SET status=%s WHERE type_code=%s"
        params=(status,type_code,)
        result=db.set_specific_sql(sql,params)
        return result





    def search_data(self,keyword,status):
        db=DB()
        sql="SELECT \
                A.id,\
                B.description AS product_type,\
                A.price,\
                A.quantity,\
                A.price*A.quantity AS sub_total,\
                A.received_date,\
                DATEDIFF(CURRENT_DATE(), A.received_date) AS duration\
        FROM bougth A\
        INNER JOIN product_types B \
        ON A.type_code=B.type_code\
        WHERE CONCAT(A.type_code+' ',B.description) LIKE %s AND A.status LIKE %s"

        fields=["id","product_type","price","quantity","sub_total","received_date","duration"]
        params=("%"+keyword+"%",status,)
        result=db.get_specific_sql(sql,fields,params)

        return result




    def search_before_migrate(self):
        db=DB()
        sql="SELECT \
                A.id,\
                B.description AS product_type,\
                A.price,\
                A.quantity,\
                A.price*A.quantity AS sub_total,\
                A.received_date,\
                DATEDIFF(CURRENT_DATE(), A.received_date) AS duration\
        FROM bougth A\
        INNER JOIN product_types B \
        ON A.type_code=B.type_code\
        WHERE  A.status LIKE %s"

        fields=["id","product_type","price","quantity","sub_total","received_date","duration"]
        params=(0,)
        result=db.get_specific_sql(sql,fields,params)

        return result
