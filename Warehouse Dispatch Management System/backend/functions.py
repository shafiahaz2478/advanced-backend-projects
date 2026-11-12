
from sqlalchemy import Integer, String, Float, Column, create_engine, Date, ForeignKey, func
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, date, timedelta, timezone
import jwt


DB_PATH = "./warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

USERNAME = "Shafi"
PASSWORD = "12345"

ACCESS_TOKEN_EXPIRY = 1
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "thebigkeythatissecretthatnooneshouldseebutitspublicbecauseitsgonnabeingithub"
ALGORITHM = "HS256"

class Package(Base):
    __tablename__ = "package"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    destination = Column(String)
    weight = Column(Float)
    arrival_date = Column(Date)
    status = Column(String)
    batch_id = Column(Integer, ForeignKey("dispatch.id") , nullable=True, default=None)


class Dispatch(Base):
    __tablename__ = "dispatch"
    id = Column(Integer, primary_key=True)
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
        "status": package.status,
        "batch_id":package.batch_id

    }
def dispatch_to_dict(dispatch:Dispatch):
    return {
        "id":dispatch.id,
        "package_id":dispatch.package_id,
        "destination": dispatch.destination,
        "vehicle": dispatch.vehicle,
        "status": dispatch.status

    }

def update_package(id, name=None,destination=None,weight=None,arrival_date=None,status=None, batch_id = None):
    session = Session(engine)
    package = session.get(Package, id)
    if not package:
        return {"code": 404, "msg": "Package Not Found"}

    package.name = name if name else package.name
    package.destination = destination if destination else package.destination
    package.weight = weight if weight else package.weight
    package.arrival_date = arrival_date if arrival_date else package.arrival_date
    package.status = status if status else package.status
    package.batch_id = batch_id if batch_id else package.batch_id

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




def add_dispatch(destination,vehicle,status):
    session = Session(engine)
    dispatch = Dispatch( destination=destination, vehicle=vehicle, status=status)
    session.add(dispatch)
    session.commit()
    response = dispatch_to_dict(dispatch)
    session.close()
    return {"code":200 , "dispatch":response}


def summary():
    session = Session(engine)
    package_received = session.query(Package).count()
    package_pending = session.query(Package).filter(Package.status == "Dispatching").count()
    package_dispatched = session.query(Package).filter(Package.status == "dispatched").count()
    packages = session.query(Package).all()
    package_dest = {}

    for package in packages:
        package_dest[package.destination] = package_dest.get(package.destination , 0) + 1



    response = {
        "package_received":package_received,
        "package_pending":package_pending,
        "package_dispatched":package_dispatched,
        "package_dest":package_dest
    }
    session.close()
    return {"code":200 , "response":response}


def verify_login(username , password):
    if username == USERNAME and password == PASSWORD:
        access_token = create_token(username,"access")
        refresh_token = create_token(username,"refresh")
        return {"access_token":access_token , "refresh_token": refresh_token}

    return None

def create_token(username, token_type):
    payload = {
        "username":username,
        "token_type":token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY if token_type == "access" else REFRESH_TOKEN_EXPIRY)
    }

    return jwt.encode(payload=payload , key=SECRET_KEY , algorithm=ALGORITHM)

def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return False

    if payload["token_type"] == token_type:
        return payload["username"]
    return False





