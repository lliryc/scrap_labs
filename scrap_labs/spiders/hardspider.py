import scrapy
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from scrap_labs.spiders.models import DeviceInfo

class HardSpider(scrapy.Spider):
    name = "devices"

    def start_requests(self):
        #urls = ['http://techpetroleum.ru/labor/about.php?id_labor=499']
        urls = ['http://techpetroleum.ru/equipment/about.php?id_oborud={}'.format(str(t)) for t in range(0,9821)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        di = DeviceInfo()
        di.title = response.xpath("//span[@class='zagolovk']/text()").extract_first()
        print("Title: {}".format(di.title.strip()))

        di.desc = response.xpath("//h2[text()='Описание прибора']/following-sibling::p/text()").extract_first()
        print("Desc: {}".format(di.desc))

        org_content = response.xpath("//div[@class='grid-82']/table/tr/td[@class='subzagh910']/text()").extract()
        di.manufacturer = org_content[0]
        print("Manufacturer: {}".format(di.manufacturer.strip()))

        di.device_class = org_content[1]
        print("Device class: {}".format(di.device_class.strip()))

        di.year = org_content[2]
        print("Year: {}".format(di.year.strip()))

        di.price_segment = org_content[3]
        print("Price segment: {}".format(di.price_segment.strip()))

        di.tech_condition = org_content[4]
        print("Technical condition: {}".format(di.tech_condition.strip()))

        di.reglament = org_content[5]
        print("Reglament: {}".format(di.reglament.strip()))

        org_content = response.xpath("//div[@class='grid1-42 text-left']/table/tr/td/table/tr/td/text()").extract()
        di.base_org_title = org_content[3]
        print("Base org title: {}".format(di.base_org_title.strip()))

        org_details = response.xpath("//div[@class='grid1-42 text-left']/table/tr/td[@class='subzagh910']/text()").extract()
        di.base_org_form = org_details[0]
        print("Base org form: {}".format(di.base_org_form.strip()))

        di.base_org_address = org_details[1]
        print("Base org address: {}".format(di.base_org_address.strip()))

        di.base_org_phone = org_details[2]
        print("Base org phone: {}".format(di.base_org_phone.strip()))

        di.base_org_fax = org_details[3]
        print("Base org fax: {}".format(di.base_org_fax.strip()))

        di.base_org_email = org_details[4]
        print("Base org email: {}".format(di.base_org_email.strip()))

        di.base_org_site = org_details[5]
        print("Base org site: {}".format(di.base_org_site.strip()))

        engine = db.create_engine('mysql+mysqldb://vlab_db_user:3edc3EDC@localhost/labs?charset=utf8mb4')
        connection = engine.connect()

        sessionm = sessionmaker()
        sessionm.configure(bind=engine)
        hardsession = sessionm()

        hardsession.add(di)
        hardsession.commit()

        connection.close()

        return None
