from pydantic import BaseModel
from datetime import  datetime
from src.util.dbcontroller import DBController as DB

class ProductBase(BaseModel):
    product:str
    quantity:float
    price:float
    product_type:str


class Product(ProductBase):
    product_code:str
    parent:str=""
    created_at:datetime=None
    updated_at:datetime=None

class ProductController():
    __tablename__="products"

    def gen_product_code(self):
        db=DB()
        today = datetime.today()
        year = str(today.year)
        month=today.month
        sm=f"{month:02d}"
        prefix="P"+year+sm
        sql="SELECT \
        MAX(product_code) AS product_code \
        FROM products\
        WHERE product_code LIKE %s "
        params=(prefix+"%",)
        result=db.get_specific_sql(sql,["product_code"],params)
        if(len(result)>0):
            product_code=str(result[0]["product_code"])
            suffix=product_code[7:11]
            index=int(suffix)+1
            product_code=prefix+f"{index:04d}"
            return product_code
        else:
            product_code=prefix+"0001"
            return product_code

    def add_product(self,product):
        today=datetime.today()
        product_code= self.gen_product_code()
        product["product_code"]=product_code
        product["created_at"]=today
        product["updated_at"]=today
        result=self.create(self,product)
        return result

    def create(self,product):
        db=DB(self.__tablename__)
        result=db.create(product)
        del db
        return result

    def update(self,product,id):
        db=DB(self.__tablename__)
        result=db.update(product,id)
        del db
        return result

    def increase_product(qty,product_type):
        db=DB()
        sql="UPDATE products SET \
                quantity=quantity+%s \
        WHERE product_type=%s"
        params=(float(qty),product_type,)
        result=db.set_specific_sql(sql,params)
        return result

    def increase_by_product_code(qty,product_code):
        db=DB()
        sql="UPDATE products SET \
                quantity=quantity+%s \
        WHERE product_code=%s"
        params=(float(qty),product_code,)
        result=db.set_specific_sql(sql,params)
        return result

    def decrease_by_product_type(qty,product_type):
        db=DB()
        sql="UPDATE products SET quantity=quantity-%s WHERE product_type=%s"
        params=(qty,product_type,)
        result=db.set_specific_sql(sql,params)
        return result

    def valid_product_qty(qty,product_code):
        db=DB()
        sql="SELECT quantity FROM product WHERE product_code=%s"
        params=(product_code,)
        result=db.get_specific_sql(sql,["quantity"],params)
        if(len(result)>0):
            quantity= float(result[0]["quantity"])
            Flag=True if quantity-qty>0 else False
            return Flag
        else:
            return True





    def decrease_product(qty,product_code):
        db=DB()
        sql="UPDATE products SET \
                quantity=quantity-%s \
        WHERE product_code=%s"
        params=(float(qty),product_code,)
        result=db.set_specific_sql(sql,params)
        return result

    def update_price(self,elements,product_id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,product_id)
        del db
        return result

    def update_qty(self,elements,id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,id)
        del db
        return result

    def update_qty_price(self,elements,id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,id)
        del db
        return result


    def delete(self,id):
        db=DB(self.__tablename__)
        result=db.delete(id)
        del db
        return result

    def get_data(self,id):
        db=DB(self.__tablename__)
        fields=["id","product_code","product","quantity","price","product_type"]
        result=db.get_data(fields,id)
        del db
        return result

    def update_qty(self,elements,id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,id)
        del db
        return result


    def update_price(self,elements,id):
        db=DB(self.__tablename__)
        result=db.set_elements(elements,id)
        del db
        return result

    def get_qty(self,sql,params):
        db=DB()
        fields=["quantity"]
        result=db.get_specific_sql(sql,fields,params)
        del db
        if(len(result)>0):
             return {"Flag":True,"qty":float(result[0]["quantity"])}
        else:
             return {"Flag":False}

    def get_price(self,sql,params):
        db=DB()
        fields=["price"]
        result=db.get_specific_sql(sql,fields,params)
        del db

        if(len(result)>0):
            return {"Flag":True,"cost":float(result[0]["price"])}
        else:
            return {"Flag":False}

    def get_price_by_productcode(self,product_code):
        db=DB()
        sql="SELECT product_code,product,quantity,price FROM products WHERE product_code=%s"
        params=(product_code,)
        result=db.get_specific_sql(sql,None,params)
        if(len(result)>0):
            return {"price":float(result[0]["price"]),"stock":result[0]["quantity"],"product_code":result[0]["product_code"],"product_name":result[0]["product"]}
        else:
            return{"price":0,"stock":0}

    def search_data(self,sql,fields,params):
        db=DB(self.__tablename__)
        results=db.search_data(sql,fields,params)
        del db
        return results
