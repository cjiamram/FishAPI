from mysql.connector import Error
import mysql.connector
import json

class DBController():
    def __init__(self,table_name=None):
        self.tablename=table_name
        self.conn=self.get_connection()

    def get_connection(self):
        file = open('././config/config.json')
        data = json.load(file)
        config=data["mysql_config"]
        try:
            conn = mysql.connector.connect(**config)
            return conn
        except Error as e:
            print("Error while connecting to MySQL", e)
            return None


    def create(self,objects):
        cursor = self.conn.cursor()

        sql = f"INSERT INTO {self.tablename}("
        sql_param = "VALUES("
        params = ()

        for i, (field_name, field_value) in enumerate(objects.items()):
            params+=(field_value,)
            sql += f"{field_name},\n"
            sql_param += "%s,"

        sql = sql.rstrip(",\n") + ")\n"
        sql_param = sql_param.rstrip(",") + ")\n"
        sql+=sql_param


        cursor.execute(sql, params)
        # print(sql)
        # print(params)
        cursor.close()
        self.conn.commit()
        Flag=True if cursor.rowcount>0 else False
        return {"Flag":Flag}

    """
        objects come from pydantic CLASS relate data table schema database.
        id is index of database.
    """
    def update(self,objects,id):
        cursor = self.conn.cursor()

        sql = f"UPDATE {self.tablename} SET "
        params = ()
        update_parts = []

        for field_name, field_value in objects.items():
            update_parts.append(f"{field_name} = %s")
            params+=(field_value,)

        sql += ", ".join(update_parts)

        sql+=" WHERE id=%s"
        params += (int(id),)
        cursor.execute(sql, params)

        self.conn.commit()
        # # Fetch the updated result
        sql = f"SELECT id FROM {self.tablename} WHERE id = %s"
        params = (int(id),)  # Replace with your actual value

        cursor.execute(sql, params)
        update_result = cursor.fetchall()

        # # Close the cursor and connection
        cursor.close()
        Flag=True if len(update_result)>0 else False
        return {"Flag":Flag}


    """
    id is index
    """
    def delete(self,id):
       cursor = self.conn.cursor()
       sql=f"DELETE FROM {self.tablename} WHERE id=%s"
       params = (int(id),)  # Replace with your actual value
       cursor.execute(sql, params)
       cursor.close()
       self.conn.commit()
       return {"Flag":True}

    """
    element is dict type {"name":"fieldname","value":value}
    id is index
    """
    def set_elements(self,element,id):
        cursor = self.conn.cursor()
        sql = f"UPDATE {self.tablename} SET "
        params = ()
        update_parts = []

        for field_name, field_value in element.items():
            update_parts.append(f"{field_name} = %s")
            params+=(field_value,)

        sql += ", ".join(update_parts)
        sql +=" WHERE id=%s"
        params+=(int(id),)

        cursor.execute(sql, params)
        self.conn.commit()
        row_update=cursor.rowcount
        Flag=True if row_update>0 else False
        json_obj={"Flag":Flag}
        return json_obj

    """
        fields:type SET ["a","b","c"]
        id is integer index of data table
    """

    def get_data(self,fields,id):
        cursor = self.conn.cursor()
        sql = f"SELECT {', '.join(fields)} FROM {self.tablename} WHERE id = %s"
        cursor = self.conn.cursor()
        params = (int(id),)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        json_result = [
            {field: value for field, value in zip(fields, row)}
            for row in result
        ]
        if(len(json_result)>0):
            result=json_result[0]
            result["Flag_found"]=True
            return result
        else:
            return {"Flag_found":False}


    """
        sql :string is SQL Statement query
        fields:type SET ["a","b","c"]
        params is tupple params=('a','b','c') params=('a',)
    """
    def search_data(self,sql,fields=None,params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        result = cursor.fetchall()

        if(result[0][0]!=None):
            json_result = [
                {field: value for field, value in zip(fields, row)}
                for row in result
            ]
            return json_result
        else:
            return []

    """
        sql :string is SQL Statement query
        fields:type SET ["a","b","c"] or none
        params is tupple params=('a','b','c') params=('a',)
    """
    def get_specific_sql(self,sql):
        return self.get_specific_sql(sql,None,None)

    def get_specific_sql(self,sql,fields):
        return self.get_specific_sql(sql,fields,None)    

    def get_specific_sql(self,sql,fields=None,params=None):
        cursor = self.conn.cursor()
        if(params!=None):
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        results = cursor.fetchall()
        #print(results)
        if fields==None :
            fields = [column[0] for column in cursor.description]

        if(len(results)>0):
            if(results[0][0]!=None):
                json_result = [
                    {field: value for field, value in zip(fields, row)}
                    for row in results
                ]
                return json_result
            else:
                return []
        else:
            return []


    """
        sql :string is SQL Statement query
        fields:type SET ["a","b","c"] or none
        params is tupple params=('a','b','c') params=('a',)
    """

    def set_specific_sql(self,sql,params):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)

        self.conn.commit()
        row_update=cursor.rowcount
        Flag=True if row_update>0 else False
        cursor.close()
        self.conn.commit

        result={"Flag":Flag}
        return result
