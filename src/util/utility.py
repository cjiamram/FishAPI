from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware




class Util():
    def toCreate(dict):
        pass

    def dict_to_statment(fields:dict):
        stms=""
        field_count=field_count(fields)
        i=0
        for value in fields.items():
            if(i<field_count-1):
                stms+=value+","
            else:
                stms+=value
            i+=1
        return stms  