import scrapy
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from scrap_labs.spiders.models import LabInfo

class LabSpider(scrapy.Spider):
    name = "labs"

    def start_requests(self):
        #urls = ['http://techpetroleum.ru/labor/about.php?id_labor=499']
        urls = ['http://techpetroleum.ru/labor/about.php?id_labor={}'.format(str(t)) for t in range(1,506)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        lab = LabInfo()
        lab.title = response.xpath("//span[@class='zagolovk']/text()").extract_first()
        print("Title: {}".format(lab.title))

        lab.desc = response.xpath("//h2[text()='Направления деятельности']/following-sibling::p/text()").extract_first()
        print("Desc: {}".format(lab.desc))

        cn = response.xpath("//h2[text()='Контакты']/following-sibling::p/text()").extract_first()
        if cn is not None:
            lab.contact_name = cn
            print("Contact name: {}".format(lab.contact_name))

        org_content = response.xpath("//div[@class='grid1-42 text-left']/table/tr/td/table/tr/td/text()").extract()
        lab.base_org_title = org_content[3]
        print("Base org title: {}".format(lab.base_org_title))

        org_details = response.xpath("//div[@class='grid1-42 text-left']/table/tr/td[@class='subzagh910']/text()").extract()
        lab.base_org_form = org_details[0]
        print("Base org form: {}".format(lab.base_org_form))

        lab.base_org_address = org_details[1]
        print("Base org address: {}".format(lab.base_org_address))

        lab.base_org_phone = org_details[2]
        print("Base org phone: {}".format(lab.base_org_phone))

        lab.base_org_fax = org_details[3]
        print("Base org fax: {}".format(lab.base_org_fax))

        lab.base_org_email = org_details[4]
        print("Base org email: {}".format(lab.base_org_email))

        lab.base_org_site = org_details[5]
        print("Base org site: {}".format(lab.base_org_site))

        engine = db.create_engine('mysql+mysqldb://vlab_db_user:3edc3EDC@localhost/labs?charset=utf8mb4')
        connection = engine.connect()

        sessionm = sessionmaker()
        sessionm.configure(bind=engine)
        labsession = sessionm()

        labsession.add(lab)
        labsession.commit()

        connection.close()

        return None
