from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB
from src.models.bougth import BoughtController as Bought
from src.models.product import ProductController as Product 

class PreparedSale(BaseModel):
    lot_id:int
    quantity:float 
    prepared_sale_date:datetime=None 


class PreparedSaleController():
    __tablename__="prepared_sale"
    def get_lot(self,lot_id):
        db=DB()
        sql="SELECT \
                B.type_code,\
                B.quantity \
        FROM prepared_sale A \
        INNER JOIN bougth B \
        ON A.lot_id=B.id \
        WHERE A.lot_id=%s "
        params=(lot_id,)
       
        fields=["type_code","quantity"]
        result=db.get_specific_sql(sql,fields,params)
        #print(result)
        
        return result[0]
    
    def migrate_prepared(self,lot_id):
        result=Bought.get_bought_status(lot_id)
        result=Bought.get_quantity(lot_id)
        quantity=float(result[0]["quantity"])
        today =datetime.today()      
        prepared={"lot_id":lot_id,"quantity":quantity,"prepared_sale_date":today}
        result=self.create(prepared)

        return result

    def cancel_prepared(self,id):
        db=DB()
        sql="SELECT  \
                A.id,\
                A.quantity,\
                B.type_code \
        FROM prepared_sale A \
        INNER JOIN \
        bougth B ON A.lot_id=B.id \
        WHERE A.id=%s"
        fields=["id","quantity","type_code"]
        params=(id,)
        result=db.get_specific_sql(sql,fields,params) 
        if(len(result)>0):
            result=result[0]
            product_type=result["type_code"]
            quantity=float(result["quantity"])
            decrease_flag=Product.decrease_by_product_type(quantity,product_type)["Flag"]
            cancel_bougth_flag=Bought.set_status_by_producttype(0,product_type)["Flag"]
            delete_flag=self.delete(id)["Flag"]

            result = {
                "Flag": True,
                "decrease_flag": decrease_flag,
                "cancel_bought_flag": cancel_bougth_flag,
                "delete_flag":delete_flag,
                "message": "Completely cancel prepared sale."
            }
            return result 
        else:
           return {"Flag":False,"message":"Not allow cancel prepared sale."}  
    
    
    def create(self,prepared):
        db=DB(self.__tablename__)
        lot_id=int(prepared["lot_id"])
        result=db.create(prepared)
        status_result= Bought.set_status(1,lot_id)
        lot_result=self.get_lot(lot_id)
        increase_result=Product.increase_product(float(lot_result["quantity"]),lot_result["type_code"])
        del db
        result["Bougth_status"]=status_result["Flag"]
        result["Increase_status"]=increase_result["Flag"]
        return result

    def update(self,prepared,id):
        db=DB(self.__tablename__)
        lot_id=prepared.lot_id
        result=db.update(prepared,id)
        Bought.set_status(1,lot_id)
        del db
        return result

    def get_lod_id(self,id):
        db=DB()
        sql="SELECT \
            lot_id \
        FROM prepared_sale \
        WHERE id=%s"
        fields=["lot_id"]
        params=(id,)
        result=db.get_specific_sql(sql,fields,params)
        return result 


    def delete(self,id):
        db=DB(self.__tablename__)
        result=db.delete(id)
        del db
        return result
    

    
    def search_data(self,keyword):
        db=DB()
        sql="SELECT \
                    A.id,\
                    C.description,\
                    B.received_date,\
                    A.prepared_sale_date,\
                    A.quantity,\
                    DATEDIFF(CURRENT_DATE(), B.received_date) AS duration\
        FROM prepared_sale \
        A INNER JOIN bougth B\
        ON A.lot_id=B.id \
        INNER JOIN product_types C \
        ON B.type_code=C.type_code \
        WHERE  C.description LIKE %s \
        ORDER BY ID DESC"
        fields=["id","produc_type","received_date","prepared_sale_date","quantity","duration"]
        params=('%'+keyword+'%',)
        result=db.get_specific_sql(sql,None,params)
        return result 
        
