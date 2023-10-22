from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB
from src.models.Item import ItemController as Item

"""
    This class is base of deposit data by pydantic class
"""
class DepositBase(BaseModel):
    item_code:str # Code is assign to item
    created_at:datetime=None
    quantity:float#  Quantity


"""
    This class inherit from DepositBase extend from about deposit.
"""
class Deposit(DepositBase):

    price:float
    before_stock:float
    after_stock:float
    updated_at:datetime=None

class DepositController():
    __tablename__="deposits"


    # def get_data(self,id):
    #     db=DB(self.__tablename__)
    #     result=db.get_data(None,id)
    #     return result


    def is_exist(item_code):
        db=DB()
        sql="SELECT id FROM deposits WHERE item_code=%s"
        params=(item_code,)
        results=db.get_specific_sql(sql,None,params)
        Flag=True if len(results)>0 else False
        return Flag

    """
    Deposit transaction
    """
    def add_deposit_item(self,deposit):
        item_code=deposit["item_code"]
        before_stock=Item.get_qty_by_itemcode(item_code)["qty"]
        price=float(Item.get_cost_by_itemcode(item_code)["cost"])
        quantity=float(deposit["quantity"])
        after_stock=float(before_stock)-quantity
        if(after_stock>=0):
            """
                set price  before stock and after stock into dictitnary variable
            """
            deposit["price"]=price
            deposit["before_stock"]=before_stock
            deposit["after_stock"]=after_stock
            result=self.create(deposit)
            #**********************************************
            flag_deposit= Item.decrease_item(item_code,quantity)["Flag"]
            result["flag_deposit"]=flag_deposit
            result["is_enought"]=True
            return result
        else:
            result={"Flag":False,"is_enought":False}
            return result


    """
    Cancel deposit and return to stock
    """
    def cancel_deposit_item(self,id):
        result_item=  self.get_deposit_item(id)
        quantity=float(result_item["quantity"])
        item_code=result_item["item_code"]
        result=self.delete(id)
        result_cancel=Item.increase_item(item_code,quantity)["Flag"]
        result["result_cancel"] =result_cancel
        return result

    def get_deposit_item(self,id):
        db=DB()
        sql="SELECT quantity,item_code FROM deposits WHERE id=%s"
        params=(int(id),)
        result=db.get_specific_sql(sql,None,params)
        if(len(result)>0):
            return result[0]
        else:
            return {"quantity":0,"item_code":""}



    def create(self,deposit):
        db=DB(self.__tablename__)
        result=db.create(deposit)
        del db
        return result

    def update(self,deposit,id):
        db=DB(self.__tablename__)
        result=db.update(deposit,id)
        del db
        return result

    def delete(self,id):
        db=DB(self.__tablename__)
        result=db.delete(id)
        del db
        return result

    def get_data(self,id=0):
        db=DB(self.__tablename__)
        fields=["id","item_code","price","quantity","before_stock","after_stock","created_at","updated_at"]
        result=db.get_data(fields,id)
        del db
        return result


    def search_data(self,keyword):
        db=DB()
        sql="SELECT \
                    A.id,\
                    A.item_code,\
                    B.item_name,\
                    A.quantity,\
                    A.price,A.after_stock,\
                    A.quantity*A.price AS sub_total\
            FROM deposits A INNER JOIN items B\
            ON A.item_code=B.item_code \
            WHERE CONCAT(A.item_code,' ',B.item_name) LIKE %s\
            ORDER BY A.id DESC"
        keyword="%"+keyword+"%"
        params=(keyword,)
        # print(sql)
        # print(params)
        results=db.get_specific_sql(sql,None,params)
        del db
        return results
