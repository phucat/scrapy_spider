from scrapy.exceptions import CloseSpider

import scrapy
import logging

# install
# sudo apt-get install unixodbc-dev
# https://blogs.msdn.microsoft.com/sqlnativeclient/2016/10/20/odbc-driver-13-0-for-linux-released/

import pyodbc
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=81.2.234.35;DATABASE=DataEntryDatabase;UID=scraper;PWD=123456Ab.')
cursor = cnxn.cursor()
cursor.execute("select user_id, user_name from users")
rows = cursor.fetchall()

#
# from sqlalchemy import create_engine
# engine = create_engine("mssql+pyodbc://scraper:123456Ab.@81.2.234.35/DataEntryDatabase?driver=Microsoft+ODBC+Driver+13")
# for row in engine.execute("select user_id, user_name from users"):
#     print row.user_id, row.user_name

cur = db.cursor()
root_url = 'https://www.yellowpages.com'


class YellowSpider(scrapy.Spider):

    name = 'yellow page spider'

    def __init__(self, search='', location='', page_limit=200, *args, **kwargs):
        super(YellowSpider, self).__init__(*args, **kwargs)

        self.start_urls = []
        page = 0
        loop = True
        while loop:
            initial_url = '%s/search?search_terms=%s&geo_location_terms=%s' % (root_url, search, location)
            url = initial_url if page == 0 else initial_url + "&page=" + str(page)
            self.start_urls.append(url)
            page += 1
            if page > page_limit:
                loop = False

    # logging.info(start_urls)

    def parse(self, response):

        container = response.css('div.organic .v-card')

        if len(container) == 0:
            # exit if end of page
            raise CloseSpider('End of Page')

        for dom in container:
            vcard = {}

            id_c = dom.css('h2.n a').xpath('@href').extract_first()
            # logging.info(id_c)
            try:
                _id = int(id_c.split("lid=")[1])
            except Exception as e:
                continue

            vcard['scraping_source_id'] = _id
            result = cur.execute("SELECT scraping_source_id from tbl_scraper_data WHERE scraping_source_id='%s'" % _id)
            # logging.info('=========')
            # logging.info(result)

            if result == 0:

                company = dom.css('.info h2 a ::text').extract_first()
                vcard['company'] = company

                address = dom.css('.adr ::text').extract()
                adr = ''
                for a in address:
                    adr = adr + a + " "
                vcard['address'] = adr

                phone = dom.css('.phone ::text').extract_first()
                vcard['phone'] = phone

                categories = dom.css('.categories ::text').extract()
                industry = ''
                for c in categories:
                    industry = industry + c + ", "
                vcard['industry_focus'] = industry

                vcard['logo_url'] = dom.css('.media-thumbnail a img').xpath('@src').extract_first()

                link = root_url + dom.css('.business-name').xpath('@href').extract_first()
                vcard['link'] = link

                vcard['email'] = ''
                vcard['number_of_employees'] = 3
                vcard['is_importable'] = ''

                logging.info('----------------------------------')
                logging.info(vcard)

                insert_data(vcard)
                yield scrapy.http.Request(link, callback=self.get_email)

    def get_email(self, response):
        scraping_source_id = response.request.url.split('lid=')[1]
        logging.info(scraping_source_id)
        email = response.css('.email-business').xpath('@href').extract_first()
        email = None if email is None else email.split('mailto:')[1]
        logging.info(email)
        if email is not None:
            cur.execute("UPDATE tbl_scraper_data SET email='%s' WHERE scraping_source_id='%s'" % (email, scraping_source_id))
            db.commit()


def insert_data(vcard):

    sql = "INSERT INTO tbl_scraper_data " \
          "(phone, address, company, email, logo_url, number_of_employees, industry_focus, scraping_source_id, " \
          "is_importable, link) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    data = (vcard.get('phone'),
            vcard.get('address'),
            vcard.get('company'),
            vcard.get('email'),
            vcard.get('logo_url'),
            vcard.get('number_of_employees'),
            vcard.get('industry_focus'),
            vcard.get('scraping_source_id'),
            vcard.get('is_importable'),
            vcard.get('link')
            )
    # logging.info(data)
    cur.execute(sql, data)
    db.commit()
