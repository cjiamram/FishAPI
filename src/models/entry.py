from pydantic import BaseModel
from typing import Optional
from datetime import  datetime
from src.util.dbcontroller import DBController as DB
from src.models.Item import ItemController as Item
from dateutil.relativedelta import relativedelta


class EntryBase(BaseModel):
    item_code:str
    quantity:float
    price:float
    supplier:str
    receive_date:datetime=None

class Entry(EntryBase):
    before_stock:float
    after_stock:float
    created_at:datetime=None
    updated_at:datetime=None



class EntryController():
    __tablename__="entries"

    def is_exist(item_code):
        db=DB()
        sql="SELECT id FROM entries WHERE item_code=%s"
        params=(item_code,)
        results=db.get_specific_sql(sql,None,params)
        Flag=True if len(results)>0 else False
        return Flag


    def receive_item_trans(self,entry):
        item_code=entry["item_code"]
        quantity=float(entry["quantity"])
        before_stock=Item.get_qty_by_itemcode(item_code)["qty"]
        after_stock=float(before_stock)+quantity
        current_date=datetime.today()
        entry["before_stock"]=before_stock
        entry["after_stock"]=after_stock
        entry["created_at"]=current_date
        result=self.create(entry)
        flag_intry= Item.increase_item(item_code,quantity)["Flag"]
        result["flag_entry"]=flag_intry
        return result



    def cancel_item_trans(self,id):
        item_result=Item.get_some_item(id)[0]
        flag_cancel=Item.decrease_item(item_result["item_code"],float(item_result["quantity"]))["Flag"]
        result=self.delete(id)
        result["flag_cancel"]=flag_cancel
        return result

    def create(self,entry):
        db=DB(self.__tablename__)
        result=db.create(entry)
        del db
        return result

    def update(self,entry,id):
        db=DB(self.__tablename__)
        result=db.update(entry,id)
        del db
        return result

    def delete(self,id):
        db=DB(self.__tablename__)
        result=db.delete(id)
        del db
        return result

    def get_data(self,fields=None,id=0):
        db=DB(self.__tablename__)
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
                    A.price,\
                    A.quantity*A.price AS sub_total,\
                    A.after_stock \
            FROM entries A INNER JOIN items B \
            ON A.item_code=B.item_code \
            WHERE CONCAT( A.item_code,' ',B.item_name) LIKE %s\
            ORDER BY A.id DESC"
        keyword="%"+keyword+"%"
        params=(keyword,)
        fields=["id","item_code","item_name","quantity","price","sub_total","stock"]
        results=db.get_specific_sql(sql,fields,params)
        del db
        return results


class EntryReport():
    def get_report_entry_by_duration(self,item_code,start_length,segment):
        db=DB()
        finish_date=datetime.today()
        start_date=finish_date-relativedelta(days=start_length)
        difference_in_days = (finish_date - start_date).days
        day_length=round(difference_in_days/segment)
        durations=[]
        cdate=start_date
        for i in range(0,segment-1,1):
            if(i<segment-1):
                fdate=cdate + relativedelta(days=day_length)
                T=self.get_sumary_date_range(db,item_code,cdate,fdate)
                day_criteria={"sdate":cdate,"fdate":fdate,"sub_total":T}
                cdate=fdate+ relativedelta(days=1)
                durations.append(day_criteria)
            else:
                if(i==segment-1):
                    T=self.get_sumary_date_range(db,item_code,cdate,fdate)
                    fdate=finish_date
                    T=self.get_sumary_date_range(db,item_code,cdate,fdate)
                    day_criteria={"sdate":cdate,"fdate":fdate,"sub_total":T}
                    cdate=fdate+ relativedelta(days=1)
                    durations.append(day_criteria)
        del db
        return durations

    def get_sumary_date_range(self,db,item_code,sdate,fdate):

        sql="SELECT SUM(price*quantity) AS T\
        FROM entries \
        WHERE item_code=%s AND \
        receive_date BETWEEN %s AND %s"
        params=(item_code,sdate.strftime('%Y-%m-%d %H:%M:%S'),fdate.strftime('%Y-%m-%d %H:%M:%S'),)
        results=db.get_specific_sql(sql,None,params)
        if(len(results)>0):
            return results[0]["T"]
        return 0
