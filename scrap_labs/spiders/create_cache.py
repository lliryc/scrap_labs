import scrapy
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scrap_labs.spiders.models import MapCache

def create_map_cache():
    engine = db.create_engine('mysql+mysqldb://vlab_db_user:3edc3EDC@localhost/labs?charset=utf8mb4')
    connection = engine.connect()

    sessionm = sessionmaker()
    sessionm.configure(bind=engine)
    map_session = sessionm()

    map_session.add(lab)
    map_session.commit()

    connection.close()

    return None
