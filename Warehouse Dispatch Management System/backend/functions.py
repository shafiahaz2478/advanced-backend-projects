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


class Dispatch(Base):
    __tablename__ = "dispatch"
    id = Column(Integer, primary_key=True)
    package_id = Column(Integer, ForeignKey("package.id"))
    destination = Column(String)
    vehicle = Column(String)
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
def dispatch_to_dict(dispatch:Dispatch):
    return {
        "id":dispatch.id,
        "package_id":dispatch.package_id,
        "destination": dispatch.destination,
        "vehicle": dispatch.vehicle,
        "status": dispatch.status

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

def del_package(id):
    session = Session(engine)
    package = session.get(Package, id)
    if not package:
        return {"code": 404, "msg": "Package Not Found"}
    if package.status == "dispatched":
        return {"code": 403, "msg": "Package already dispatched"}

    session.delete(package)
    session.commit()
    session.close()
    return {"code": 200, "msg": "Package deleted"}

def get_packages(destination=None,arrival_date=None,status=None):
    session = Session(engine)
    packages = session.query(Package)
    if destination:
        packages = packages.filter(Package.destination == destination)

    if arrival_date:
        packages = packages.filter(Package.arrival_date == arrival_date)

    if status:
        packages = packages.filter(Package.status == status)

    packages = packages.all()

    response = []

    for package in packages:
        response.append(package_to_dict(package))

    session.close()
    return {"code":200 , "packages": response}

def get_dispatch(destination=None,vehicle=None,status=None):
    session = Session(engine)
    dispatches = session.query(Dispatch)
    if destination:
        dispatches = dispatches.filter(Dispatch.destination == destination)

    if vehicle:
        dispatches = dispatches.filter(Dispatch.vehicle == vehicle)

    if status:
        dispatches = dispatches.filter(Dispatch.status == status)

    dispatches = dispatches.all()
    response = []

    for dispatch in dispatches:
        response.append(dispatch_to_dict(dispatch))


    session.close()
    return {"code": 200, "dispatches": response}




def add_dispatch(package_id, destination,vehicle,status):
    session = Session(engine)
    package = session.get(Package, package_id)
    if not package:
        return {"code": 404, "msg": "Package Not Found"}
    dispatch = Dispatch(package_id=package_id , destination=destination, vehicle=vehicle, status=status)
    session.add(dispatch)
    session.commit()
    response = dispatch_to_dict(dispatch)
    session.close()
    return {"code":200 , "dispatch":response}


