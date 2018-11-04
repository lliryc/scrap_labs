from sqlalchemy import Column, DateTime, String, Text, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class LabInfo(Base):
    __tablename__ = 'lab_info'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=500))
    desc = Column(Text())
    contact_name = Column(String(length=5000))
    contact_tel = Column(String(length=200))
    contact_email = Column(String(length=200))
    base_org_title = Column(String(length=500))
    base_org_form = Column(String(length=500))
    base_org_address = Column(String(length=1000))
    base_org_phone = Column(String(length=200))
    base_org_fax = Column(String(length=200))
    base_org_email = Column(String(length=200))
    base_org_site = Column(String(length=200))

class DeviceInfo(Base):
    __tablename__ = 'device_info'
    id = Column(Integer, primary_key=True)
    title = Column(String(length=500))
    manufacturer = Column(String(length=500))
    device_class = Column(String(length=500))
    year = Column(String(length=500))
    price_segment = Column(String(length=500))
    tech_condition = Column(String(length=500))
    reglament = Column(String(length=500))

    desc = Column(Text())

    contact_name = Column(String(length=5000), nullable=True)

    base_org_title = Column(String(length=500))
    base_org_form = Column(String(length=500))
    base_org_address = Column(String(length=1000))
    base_org_phone = Column(String(length=200))
    base_org_fax = Column(String(length=200))
    base_org_email = Column(String(length=200))
    base_org_site = Column(String(length=200))


class MapCache(Base):
    __tablename__ = 'map_cache'
    id = Column(Integer, primary_key=True)
    address = Column(String(length=500))
    geocode = Column(String(length=500))


# engine = db.create_engine('mysql+mysqldb://vlab_db_user:3edc3EDC@localhost/labs?charset=utf8mb4')
# connection = engine.connect()
#
# sessionm = sessionmaker()
# sessionm.configure(bind=engine)
# sessionm.configure(bind=engine)
# Base.metadata.create_all(engine)
# labsession = sessionm()
# connection.close()
