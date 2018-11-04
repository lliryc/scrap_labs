import scrapy
import sqlalchemy as db
import urllib
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from scrap_labs.spiders.models import LabInfo, MapCache
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

class GiSpider(scrapy.Spider):
    name = "gis"

    def start_requests(self):
        engine = db.create_engine('mysql+mysqldb://vlab_db_user:3edc3EDC@localhost/labs?charset=utf8')
        connection = engine.connect()

        sessionm = sessionmaker()
        sessionm.configure(bind=engine)
        mapsession = sessionm()
        address = None
        try:
            labs = mapsession.query(LabInfo).all()
        except MultipleResultsFound as e:
            print(e)
            return
        except NoResultFound as e:
            print(e)
            return
        connection.close()

        urls = []
        for lab in labs:
            address = lab.base_org_address
            url = 'https://geocode-maps.yandex.ru/1.x/?apikey=da7206dc-3691-4c21-ba76-3f02da818f1e&format=json&geocode={}'.format(urllib.parse.quote_plus(address))
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # get address string
        # print(response.body_as_unicode())
        # return
        urlparse_res = urllib.parse.urlparse(response.request.url)
        query = urlparse_res.query
        param_dict = urllib.parse.parse_qs(query)
        address = param_dict["geocode"]

        # get coordinates
        jsonresponse = json.loads(response.body_as_unicode())

        results = jsonresponse["response"]["GeoObjectCollection"]

        if int(results["metaDataProperty"]["GeocoderResponseMetaData"]["found"]) == 0:
            print("Not found")
            print(address)
            return None

        geo_object = results["featureMember"][0]["GeoObject"]

        coordinates = geo_object["Point"]["pos"]

        # save result to db
        map_cache = MapCache()

        map_cache.address = address
        map_cache.geocode = coordinates.replace(" ", ", ")

        engine = db.create_engine('mysql+mysqldb://vlab_db_user:3edc3EDC@localhost/labs?charset=utf8')
        connection = engine.connect()

        sessionm = sessionmaker()
        sessionm.configure(bind=engine)
        mapsession = sessionm()

        mapsession.add(map_cache)
        mapsession.commit()

        connection.close()

        return None
