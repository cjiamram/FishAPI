from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB

class ItemBase(BaseModel):
    item_name:Optional[str]
    quantity:float
    cost:float
    status:int
    unit:str


class Item(ItemBase):
    item_code:str
    created_at:datetime=None
    updated_at:datetime=None


class ItemController():
    __tablename__="items"

    def add_item(self,item):
        today=datetime.today()
        item_code= self.gen_item_code()
        item["item_code"]=item_code
        item["created_at"]=today
        item["updated_at"]=today
        result=self.create(item)
        result["item_code"]=item_code
        return result

    def update_item(self,item,id):
        today=datetime.today()
        del item["created_at"]
        item["updated_at"]=today
        result =self.update(item,id)
        result["item_code"]=item["item_code"]
        return result


    def get_unit(self):
        db=DB()
        sql="SELECT id,code,unit FROM units "
        results=db.get_specific_sql(sql)
        return results




    def gen_item_code(self):
        db=DB()
        today = datetime.today()
        year = str(today.year)
        month=today.month
        sm=f"{month:02d}"
        prefix="I"+year+sm
        sql="SELECT \
        MAX(item_code) AS item_code \
        FROM items\
        WHERE item_code LIKE %s "
        params=(prefix+"%",)
        result=db.get_specific_sql(sql,["item_code"],params)
        if(len(result)>0):
            item_code=str(result[0]["item_code"])
            suffix=item_code[7:11]
            index=int(suffix)+1
            item_code=prefix+f"{index:04d}"
            return item_code
        else:
            item_code=prefix+"0001"
            return item_code

    def create(self,items):
        db=DB(self.__tablename__)
        result=db.create(items)
        del db
        return result

    def update(self,items,id):
        db=DB(self.__tablename__)
        result=db.update(items,id)
        del db
        return result

    def get_item_code_by_id(self,id):
        db=DB()
        sql="SELECT item_code FROM items WHERE id=%s"
        params=(int(id),)
        results=db.get_specific_sql(sql,None,params)
        if len(results)>0:
            return results[0]["item_code"]
        return ""

    def is_exist_entry(self,item_code):
            db=DB()
            sql="SELECT id FROM entries WHERE item_code=%s"
            params=(item_code,)
            results=db.get_specific_sql(sql,None,params)
            Flag=True if len(results)>0 else False
            return Flag

    def is_exist_deposit(self,item_code):
            db=DB()
            sql="SELECT id FROM deposits WHERE item_code=%s"
            params=(item_code,)
            results=db.get_specific_sql(sql,None,params)
            Flag=True if len(results)>0 else False
            return Flag

    def delete(self,id):
        item_code=self.get_item_code_by_id(id)
        flag_Exist=self.is_exist_deposit(item_code) or self.is_exist_entry(item_code)
        if(not flag_Exist):
            db=DB(self.__tablename__)
            result=db.delete(id)
            del db
            result["message"]="This item deleted."
            return result
        else:
            return {"Flag":False,"message":"This item already in use."}


    def get_data(self,id):
        db=DB(self.__tablename__)
        fields=["id","item_code","item_name","quantity","cost","status","unit"]
        result=db.get_data(fields,id)
        del db
        return result

    def get_data_by_itemcode(self,item_code):
        db=DB()
        sql="SELECT id,\
                        item_code,\
                        item_name,\
                        quantity,\
                        cost,\
                        status,\
                        unit \
        FROM items WHERE item_code=%s "
        params=(item_code,)
        result=db.get_specific_sql(sql,None,params)
        return result[0]

    def update_cost(self,elements,id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,id)
        del db
        return result

    def update_qty(self,elements,id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,id)
        del db
        return result

    def increase_item(item_code,qty):
        db=DB()
        sql="UPDATE items\
        SET quantity=quantity+%s\
        WHERE item_code=%s"
        params=(qty,item_code,)
        result=db.set_specific_sql(sql,params)
        return result

    def decrease_item(item_code,qty):
        db=DB()
        sql="UPDATE items\
        SET quantity=quantity-%s\
        WHERE item_code=%s"
        params=(qty,item_code,)
        result=db.set_specific_sql(sql,params)
        return result


    def update_cost(self,elements,item_id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,item_id)
        del db
        return result


    def get_qty(id):
        db=DB()
        sql="SELECT quantity FROM items WHERE id=%s"
        params=(int(id),)
        result=db.get_specific_sql(sql,None,params)
        del db
        if(len(result)>0):
             return {"Flag":True,"qty":float(result[0]["quantity"])}
        else:
             return {"Flag":False}

    def update_item_cost(self, item_code):
        # Get the current cost based on quantity
        quantity=self.get_quantity_by_itemcode(item_code)["cost"]
        result_cost=self.get_current_cost(item_code, quantity)
        if(result_cost["set"]==True):
            current_cost = result_cost["cost"]

            if current_cost > 0:
                # Set the current cost in the database
                result = self.set_current_cost(item_code, current_cost)
                result["cost"] = current_cost
                result["item_code"] = item_code
                return True
            else:
                return False
        else:
            return False

    def set_current_cost(self, item_code, cost): #set current cost
        if cost > 0:
            db=DB()
            sql = "UPDATE items SET cost=%s WHERE item_code=%s"
            params = (cost, item_code,)
            result = db.set_specific_sql(sql, params)
            result["cost"] = cost
            result["item_code"] = item_code
            del db
            return result
        return {"error": "Invalid cost"}

    def get_current_cost(self, item_code, quantity):#get current cost
        db=DB()
        sql = "SELECT quantity, price FROM entries WHERE item_code=%s ORDER BY id DESC LIMIT 50"
        params = (item_code,)
        results = db.get_specific_sql(sql, None, params)
        price = 0

        if len(results) > 0:
            for p in results:
                qty=float(p["quantity"])
                cost=p["price"]
                if quantity <qty:
                    del db
                    return {"set":True,"cost":cost}
                else:
                    quantity =quantity- qty
        del db
        return {"set":False,"cost":0}

    def get_quantity_by_itemcode(self, item_code): #get quantity from items
        db=DB()
        sql = "SELECT quantity FROM items WHERE item_code=%s"
        params = (item_code,)
        result = db.get_specific_sql(sql, None, params)
        del db

        if len(result) > 0:
            return {"Flag": True, "cost": float(result[0]["quantity"])}
        else:
            return {"Flag": False}


    def get_qty_by_itemcode(item_code):
        db=DB()
        sql="SELECT quantity FROM items WHERE item_code=%s"
        params=(item_code,)
        result=db.get_specific_sql(sql,None,params)
        del db
        if(len(result)>0):
             return {"Flag":True,"qty":float(result[0]["quantity"])}
        else:
             return {"Flag":False,"qty":0}



    def get_cost_by_itemcode(item_code):
        db=DB()
        sql="SELECT cost FROM items WHERE item_code=%s"
        params=(item_code,)
        result=db.get_specific_sql(sql,None,params)
        del db
        if(len(result)>0):
             return {"Flag":True,"cost":float(result[0]["cost"])}
        else:
             return {"Flag":False}



    def get_cost(id):
        db=DB()
        sql="SELECT cost FROM items WHERE id=%s"
        params=(int(id),)
        result=db.get_specific_sql(sql,None,params)
        del db
        if(len(result)>0):
             return {"Flag":True,"qty":float(result[0]["cost"])}
        else:
             return {"Flag":False}



    def search_item(self,keyword):
        db=DB()
        sql="SELECT \
                A.id,\
                A.item_code,\
                A.item_name,\
                A.quantity,\
                A.status, \
                A.cost,\
                B.unit\
        FROM items A INNER JOIN units B\
        ON A.unit=B.code \
        WHERE \
        CONCAT(A.item_code,' ',A.item_name) LIKE %s "
        keyword=f"%{keyword}%"
        params=(keyword,)
        results=db.get_specific_sql(sql,None,params)
        return results
