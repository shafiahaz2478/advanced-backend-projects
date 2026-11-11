from datetime import date

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_core.core_schema import DatetimeSchema

import functions

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/register")
def register(name : str, destination : str, weight : float, arrival_date: date):
    return functions.register_package(name, destination, weight, arrival_date)


@app.get("/packages/{package_id}")
def get_package(package_id):
    response = functions.get_package(package_id)
    if response["code"] == 200:
        return response["package"]
    raise HTTPException(status_code=response["code"] , detail=response["msg"])

@app.patch("/packages/{package_id}")
def update_package(package_id , name=None,destination=None,weight=None,arrival_date=None,status=None):
    response = functions.update_package(package_id,name, destination, weight, arrival_date, status)
    if response["code"] == 200:
        return response["package"]
    raise HTTPException(status_code=response["code"], detail=response["msg"])

