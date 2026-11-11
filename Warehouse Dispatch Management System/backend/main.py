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


