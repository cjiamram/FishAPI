
from datetime import  datetime
from dateutil.relativedelta import relativedelta
from src.util.dbcontroller import DBController as DB

class Report():
    def report_subtotal_item(self,item_code,start_length,segment):
        db=DB()
        finish_date=datetime.today()
        start_date=finish_date-relativedelta(days=start_length)
        difference_in_days = (finish_date - start_date).days
        day_length=round(difference_in_days/segment)
        subtotal_by_durations=[]
        cdate=start_date
        for i in range(0,segment-1,1):
            if(i<segment-1):
                fdate=cdate + relativedelta(days=day_length)
                entry_T=self.get_subtotal_entry_date_range(db,item_code,cdate,fdate)
                deposit_T=self.get_subtotal_deposit_date_range(db,item_code,cdate,fdate)
                if entry_T>0 or deposit_T>0:
                    t_date=fdate.strftime('%Y-%m-%d')
                    day_criteria={"trans_date":t_date,"entry_sub_total":entry_T,"deposit_sub_total":deposit_T}
                    subtotal_by_durations.append(day_criteria)
                cdate=fdate+ relativedelta(days=1)
            else:
                if(i==segment-1):
                    fdate=finish_date
                    entry_T=self.get_subtotal_entry_date_range(db,item_code,cdate,fdate)
                    deposit_T=self.get_subtotal_deposit_date_range(db,item_code,cdate,fdate)
                    if entry_T>0 or deposit_T>0:
                        t_date=fdate.strftime('%Y-%m-%d')
                        day_criteria={"trans_date":t_date,"entry_sub_total":entry_T,"deposit_sub_total":deposit_T}
                        subtotal_by_durations.append(day_criteria)
                    cdate=fdate+ relativedelta(days=1)
        del db
        return subtotal_by_durations

    def report_sub_total_sale(self,customer_code,start_length,segment):
        db=DB()
        finish_date=datetime.today()
        start_date=finish_date-relativedelta(days=start_length)
        difference_in_days = (finish_date - start_date).days
        day_length=round(difference_in_days/segment)
        subtotal_by_durations=[]
        cdate=start_date

        for i in range(0,segment-1,1):
            if(i<segment-1):
                fdate=cdate + relativedelta(days=day_length)
                sub_total=self.get_subtotal_sale_date_range(db,customer_code,cdate,fdate)
                if sub_total>0:
                    t_date=fdate.strftime('%Y-%m-%d')
                    day_criteria={"trans_date":t_date,"sub_total":sub_total}
                    subtotal_by_durations.append(day_criteria)
                cdate=fdate+ relativedelta(days=1)
            else:
                if(i==segment-1):
                    fdate=finish_date
                    sub_total=self.get_subtotal_sale_date_range(db,customer_code,cdate,fdate)
                    if sub_total>0:
                        t_date=fdate.strftime('%Y-%m-%d')
                        day_criteria={"trans_date":t_date,"sub_total":sub_total}
                        subtotal_by_durations.append(day_criteria)
                    cdate=fdate+ relativedelta(days=1)
        del db
        return subtotal_by_durations


    def get_subtotal_sale_date_range(self,db,customer_code,sdate,fdate):
        sql="SELECT SUM(price*quantity) AS T\
        FROM sales \
        WHERE customer_code=%s AND \
        created_at BETWEEN %s AND %s"
        params=(customer_code,sdate.strftime('%Y-%m-%d %H:%M:%S'),fdate.strftime('%Y-%m-%d %H:%M:%S'),)
        results=db.get_specific_sql(sql,None,params)
        if(len(results)>0):
            return results[0]["T"]
        return 0

    def get_subtotal_entry_date_range(self,db,item_code,sdate,fdate):
        sql="SELECT SUM(price*quantity) AS T\
        FROM entries \
        WHERE item_code=%s AND \
        receive_date BETWEEN %s AND %s"
        params=(item_code,sdate.strftime('%Y-%m-%d %H:%M:%S'),fdate.strftime('%Y-%m-%d %H:%M:%S'),)
        results=db.get_specific_sql(sql,None,params)
        if(len(results)>0):
            return results[0]["T"]
        return 0


    def get_subtotal_deposit_date_range(self,db,item_code,sdate,fdate):

            sql="SELECT SUM(price*quantity) AS T\
            FROM deposits \
            WHERE item_code=%s AND \
            created_at BETWEEN %s AND %s"
            params=(item_code,sdate.strftime('%Y-%m-%d %H:%M:%S'),fdate.strftime('%Y-%m-%d %H:%M:%S'),)
            results=db.get_specific_sql(sql,None,params)
            if(len(results)>0):
                return results[0]["T"]
            return 0

    def get_sale_pie_by_customer_code(self,customer_code,start_length):
        db=DB()
        finish_date=datetime.today()
        start_date=finish_date-relativedelta(days=start_length)
        sql="SELECT SUM(A.quantity*A.price) AS amount,\
        B.product \
        FROM Sales A INNER JOIN products B\
        ON A.product_code=B.product_code\
        WHERE A.customer_code=%s \
        AND A.created_at BETWEEN %s AND %s\
        GROUP BY B.product"
        params=(customer_code,start_date.strftime('%Y-%m-%d %H:%M:%S'),finish_date.strftime('%Y-%m-%d %H:%M:%S'),)
        results=db.get_specific_sql(sql,None,params)
        return results
