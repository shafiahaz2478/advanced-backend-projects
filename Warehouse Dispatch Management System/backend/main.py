from datetime import date

from fastapi import FastAPI, HTTPException, Body, Header
from fastapi.middleware.cors import CORSMiddleware

import functions

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["http://localhost:5173"],
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/register")
def register(name : str, destination : str, weight : float, arrival_date: date,token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.register_package(name, destination, weight, arrival_date)["package"]


@app.get("/packages/{packageId}")
def get_package(packageId,token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    response = functions.get_package(packageId)
    if response["code"] == 200:
        return response["package"]
    raise HTTPException(status_code=response["code"] , detail=response["msg"])

@app.patch("/packages/{packageId}")
def update_package(packageId , name=None,destination=None,weight=None,arrival_date=None,status=None,batchId = None,token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    response = functions.update_package(packageId,name, destination, weight, arrival_date, status,batch_id = batchId)
    if response["code"] == 200:
        return response["package"]
    raise HTTPException(status_code=response["code"], detail=response["msg"])


@app.delete("/packages/{packageId}")
def del_package(packageId,token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    response = functions.del_package(packageId)
    if response["code"] == 200:
        return response["msg"]
    raise HTTPException(status_code=response["code"], detail=response["msg"])


@app.get("/packages")
def get_packages(destination=None,arrival_date=None,status=None, token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or expired token")

    return functions.get_packages(destination, arrival_date, status)["packages"]

@app.get("/dispatch")
def get_dispatches(destination=None,vehicle=None,status=None,token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_dispatch(destination, vehicle, status)["dispatches"]

@app.post("/dispatch")
def add_dispatch( destination,vehicle,status="transporting",token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    response = functions.add_dispatch(destination, vehicle, status)
    if response["code"] == 200:
        return response["dispatch"]
    raise HTTPException(status_code=response["code"], detail=response["msg"])

@app.get("/summary")
def summary(token = Header(None)):
    username = functions.verify_token(token , "access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.summary()["response"]

@app.post("/logic")
def login(username,password):
    tokens = functions.verify_login(username, password)
    return tokens

@app.post("/refresh")
def refresh(token= Header(None)):
    username = functions.verify_token(token , "refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"access_token": functions.create_token(username,"access")}