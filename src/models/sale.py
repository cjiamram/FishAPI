from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB
from src.models.product import ProductController as Product

class SaleBase(BaseModel):
    product_code:str
    customer_code:Optional[str]
    price:float
    quantity:float
    sale_code:str='PRE-SALE-NO'

class Sale(SaleBase):
    created_at:datetime=None
    updated_at:datetime=None

class SaleController():
    __tablename__="sales"

    def gen_code(self,yymm):
        db=DB()
        sql="SELECT MAX(sale_code) AS sale_code FROM sales WHERE sale_code LIKE %s"
        params=("S"+yymm+"%",)

        results=db.get_specific_sql(sql,None,params)
        del db
        #print(len(results))
        if(len(results)>0):
            sale_code=results[0]["sale_code"]
            runno=sale_code[5:]
            runno=int(runno)+1
            # print(runno)
            formatted_number = '{:05d}'.format(runno)
            return {"sale_code":"S"+yymm+formatted_number}
        else:
            formatted_number = '{:05d}'.format(1)
            return {"sale_code":"S"+yymm+formatted_number}


    def update_sale_code(self,yymm):
        db=DB()
        sale_code=self.gen_code(yymm)["sale_code"]
        sql="UPDATE sales SET sale_code=%s WHERE sale_code='PRE-SALE-NO'"
        params=(sale_code,)
        result=db.set_specific_sql(sql,params)
        return result



    def get_price(self,product_code):
        db=DB()
        #fields=["price"]
        sql="SELECT price FROM products WHERE product_code=%s "
        params=(product_code,)
        result=db.get_specific_sql(sql,None,params)
        del db

        if(len(result)>0):
            return float(result[0]["price"])
        else:
            return 0

    def valid_product_qty(self,saleqty,product_code):
            db=DB()
            sql="SELECT quantity FROM products WHERE product_code=%s"
            params=(product_code,)
            result=db.get_specific_sql(sql,["quantity"],params)
            if(len(result)>0):
                quantity= float(result[0]["quantity"])
                Flag=True if (quantity>saleqty) else False
                return Flag
            else:
                return True

    def sale_product(self,sale_item):
        price=self.get_price(sale_item["product_code"])
        today=datetime.today
        valid=self.valid_product_qty(sale_item["quantity"],sale_item["product_code"])
        if valid==True:
            result=self.create(sale_item)
            result["valid"]=valid
            result["messsage"]="Product allowable transaction."
            return {"Flag":True,"valid":valid,"message":"Success" }
        else:
            return {"Flag":False,"valid":valid,"message":"Product is not enought" }

    def cancel_sale(self,id):
        result=self.get_sale_item(id)
        product_code=result["product_code"]
        quantity=float(result["quantity"])
        Product.increase_by_product_code(product_code,quantity)
        result=self.delete(id)
        return result

    def get_sale_item(self,id):
        db=DB()
        sql="SELECT \
            product_code,\
            quantity\
        FROM sales WHERE id=%s"
        fields=["product_code","quantity"]
        params=(id,)
        result=db.get_specific_sql(sql,fields,params)
        if(len(result)>0):
            result= result[0]
            result["Flag"]=True
            return result
        else:
            return {"Flag":False}

    def decrease_product(self,qty,product_code):
            db=DB()
            sql="UPDATE products SET \
                    quantity=quantity-%s \
            WHERE product_code=%s"
            params=(float(qty),product_code,)
            result=db.set_specific_sql(sql,params)
            #print(result)
            return result

    def create(self,sale):
        db=DB(self.__tablename__)
        today=datetime.today()
        sale["created_at"]=today
        result=db.create(sale)
        result_decrease=self.decrease_product(float(sale["quantity"]),sale["product_code"])
        flag_decrease= result_decrease["Flag"]
        result["flag_decrease"]=flag_decrease
        if flag_decrease==True:
            result["err"]=""
        else:
            result["err"]="Update data has some problem may connection not success."
        del db
        return result



    def get_data(self,fields,id):
        db=DB(self.__tablename__)
        result=db.get_data(fields,id)
        del db
        return result

    def search_data(self,sql,fields,params):
        db=DB(self.__tablename__)
        results=db.search_data(sql,fields,params)
        del db
        return results

    def get_sale_transaction(self,keyword):
        db=DB()
        sql="SELECT \
                    A.id,\
                    A.product_code,\
                    B.product,\
                    A.price,\
                    A.quantity,\
                    A.created_at,\
                    C.customer_name\
            FROM sales A \
            INNER JOIN products B \
                ON A.product_code=B.product_code \
            INNER JOIN customers C \
                ON A.customer_code=C.customer_code \
            WHERE \
            CONCAT(A.product_code,' ',B.product,' ',C.customer_name) LIKE %s\
            ORDER BY A.id DESC "
        #fields=["id","product_code","product","price","quantity","created_at","customer_name"]
        params=("%"+keyword+"%",)
        result=db.get_specific_sql(sql,None,params)
        return result
