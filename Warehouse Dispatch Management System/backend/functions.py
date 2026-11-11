from sqlalchemy import Integer, String, Float, Column, create_engine, Date, ForeignKey, func
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date, timedelta


DB_PATH = "./warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Package(Base):
    __tablename__ = "package"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(Float)
    arrival_date = Column(Date)
    status = Column(String)

Base.metadata.create_all(engine)
def register_package(name,destination,weight,arrival_date):
    session = Session(engine)
    package = Package(name=name, destination=destination, weight=weight, arrival_date=arrival_date, status="Dispatching")
    session.add(package)
    session.commit()
    response = package_to_dict(package)
    session.close()
    return {"code":200,"package":response}

def get_package(id):
    session = Session(engine)
    package = session.get(Package , id)
    if not package:
        return {"code":404 , "msg":"Package Not Found"}
    response = package_to_dict(package)
    session.close()
    return {"code":200,"package":response}


def package_to_dict(package:Package):
    return {
        "id":package.id,
        "name":package.name,
        "destination": package.destination,
        "weight": package.weight,
        "arrival_date":package.arrival_date,
        "status": package.status

    }

def update_package(id, name=None,destination=None,weight=None,arrival_date=None,status=None):
    session = Session(engine)
    package = session.get(Package, id)
    if not package:
        return {"code": 404, "msg": "Package Not Found"}

    package.name = name if name else package.name
    package.destination = destination if destination else package.destination
    package.weight = weight if weight else package.weight
    package.arrival_date = arrival_date if arrival_date else package.arrival_date
    package.status = status if status else package.status

    session.commit()
    response = package_to_dict(package)
    session.close()
    return {"code": 200, "package": response}



