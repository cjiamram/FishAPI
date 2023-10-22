from pydantic import BaseModel
from typing import Optional
from datetime import  datetime,timedelta
from src.util.dbcontroller import DBController as DB
import os

class CustomerBase(BaseModel):
    customer_name:str
    telno:Optional[str]
    email:Optional[str]
    facebook:Optional[str]
    line:Optional[str]
    farm:Optional[str]
    province:Optional[str]
    address:str
    postalcode:str
    picture:str


class Customer(CustomerBase):
    customer_code:str
    created_at:datetime=None
    updated_at:datetime=None

class CustomerUpdate(CustomerBase):
    id:int
    customer_code:str
    updated_at:datetime=None

class CustomerController():
    __tablename__="customers"

    def add_customer(self,customer):
        today=datetime.today()
        customer_code= self.gen_customer_code()
        customer["customer_code"]=customer_code
        customer["created_at"]=today
        customer["updated_at"]=today
        result=self.create(customer)
        result["customer_code"]=customer_code
        return result

    def update_customer(self,customer):

        today=datetime.today()
        customer["updated_at"]=today
        del customer["picture"]
        result=self.update(customer,int(customer["id"]))
        result["customer_code"]=customer["customer_code"]
        return result


    def gen_customer_code(self):
        db=DB()
        today = datetime.today()
        year = str(today.year)
        month=today.month
        sm=f"{month:02d}"
        prefix="C"+year+sm

        sql="SELECT \
        MAX(customer_code) AS customer_code \
        FROM customers\
        WHERE customer_code LIKE %s "
        params=(prefix+"%",)
        result=db.get_specific_sql(sql,["customer_code"],params)
        #pass

        if(len(result)>0):
            cust_code=str(result[0]["customer_code"])
            suffix=cust_code[7:11]
            index=int(suffix)+1
            customer_code=prefix+f"{index:04d}"
            return customer_code
        else:
            customer_code=prefix+"0001"
            return customer_code




    def create(self,customer):
        db=DB(self.__tablename__)
        result=db.create(customer)
        del db
        return result

    def update(self,customer,id):
        db=DB(self.__tablename__)
        result=db.update(customer,id)
        del db
        result["customer_code"]=customer["customer_code"]
        return result

    def delete(self,id):
        db=DB(self.__tablename__)
        result=db.delete(id)
        del db
        return result

    def get_picture_by_id(self,id):
        db=DB()
        sql="SELECT picture FROM customers WHERE id=%s"
        params=(int(id),)
        results=db.get_specific_sql(sql,["picture"],params)
        del db
        # print(id)
        # print(results)
        # return ""
        if(len(results)>0):
            return results[0]["picture"]
        else:
            return ""


    def delete_picture(self,picture_folder:str,picture_filename: str):
        picture_path = os.path.join(picture_folder, picture_filename)
        try:
            # Check if the file exists
            if os.path.exists(picture_path):
                os.remove(picture_path)
                return {"message": f"Picture {picture_filename} removed successfully."}
            else:
                return {"error": "Picture not found."}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}


    def get_data(self,id):
        db=DB(self.__tablename__)
        fields=["id","customer_code","customer_name","telno","email","facebook","line","farm","province","address","postalcode","picture"]
        result=db.get_data(fields,id)
        del db
        return result

    def list_customer_by_keyword(self,keyword):
        db=DB()
        sql="SELECT id,\
        customer_code,\
        customer_name\
        FROM  customers \
        WHERE  CONCAT(customer_code,' ',customer_name) LIKE %s \
        ORDER BY customer_name "
        keyword=f"%{keyword}%"
        #print(keyword)
        params=(keyword,)

        results=db.get_specific_sql(sql,None,params)
        return results

    def list_customer(self):
        db=DB()
        sql="SELECT \
                id,\
                customer_code,\
                customer_name \
        FROM  customers \
        ORDER BY\
        customer_name "
        results=db.get_specific_sql(sql,None,None)
        return results


    def query_limit(self,max):
        db=DB()
        sql ="SELECT \
                        A.id,\
                        A.customer_code,\
                        A.customer_name,\
                        A.telno,\
                        A.line,\
                        A.farm,\
                        A.address,\
                        B.province_name,\
                        A.postalcode \
            FROM customers A INNER JOIN provinces B \
            ON A.province=B.province_code \
            ORDER BY id DESC LIMIT "+max
        results=db.get_specific_sql(sql,None,None)
        del db
        return results


    def search_data(self,keyword,province):
        db=DB()
        sql ="SELECT \
                        A.id,\
                        A.customer_code,\
                        A.customer_name,\
                        A.telno,\
                        A.line,\
                        A.farm,\
                        A.address,\
                        B.province_name,\
                        A.postalcode \
            FROM customers A INNER JOIN provinces B \
            ON A.province=B.province_code \
            WHERE CONCAT(A.customer_name,' ',A.address,' ',B.province_name) LIKE %s AND A.province LIKE %s"
        province=f"%{province}%"
        keyword=f"%{keyword}%"
        params=(keyword,province,)
        results=db.get_specific_sql(sql,None,params)
        del db
        return results

    def get_sumary_by_product(self,customer_code):
        fdate = datetime.now()
        sdate= fdate + timedelta(days=90)
        db=DB()
        sql="SELECT \
            B.product,\
            SUM(A.quantity*A.price) AS subtotal \
        FROM sales \
        A INNER JOIN products B \
        ON A.product_code= B.product_code \
        WHERE A.customer_code=%s \
        AND A.created_at BETWEEN (%s AND %s) \
        GROUP BY B.product_code"
        params=(customer_code,sdate,fdate,)
        result=db.get_specific_sql(sql,None,params)
        del db
        return result

    def get_sumary_by_month(self,customer_code):
        fdate = datetime.now()
        sdate= fdate + timedelta(days=90)
        db=DB()
        sql="SELECT \
            DATE_FORMAT(A.`created_at`, '%Y-%m') AS YRMN,\
            SUM(A.quantity * A.price) AS subtotal \
        FROM sales A \
        INNER JOIN \
        products B ON A.product_code = B.product_code \
        WHERE A.customer_code = %s AND\
        A.created_at BETWEEN (%s AND %s) \
        GROUP BY DATE_FORMAT(A.`created_at`, '%Y-%m')"
        params=(customer_code,sdate,fdate,)
        result=db.get_specific_sql(sql,None,params)
        del db
        return result


    def get_last_id(self):
        db=DB()
        sql="SELECT MAX(id) AS id FROM customers"
        results=db.get_specific_sql(sql)
        return results[0]

    def get_customer_code(self,id):
        db=DB()
        sql="SELECT customer_code FROM customers WHERE id=%s"
        params=(int(id),)
        result=db.get_specific_sql(sql,None,params)
        return result[0]


    def update_picture(self,file_name,customer_code):
        db=DB()
        sql="UPDATE customers SET picture=%s WHERE customer_code=%s"
        params=(file_name,customer_code,)
        result=db.set_specific_sql(sql,params)
        #print(result)
        del db
        return result
