from scrapy.exceptions import CloseSpider

import scrapy
import logging
from us_states import states_list
# install
# sudo apt-get install unixodbc-dev
# pip install pyodbc
# pip install sqlalchemy
# https://blogs.msdn.microsoft.com/sqlnativeclient/2016/10/20/odbc-driver-13-0-for-linux-released/

import pyodbc
cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=81.2.234.35;DATABASE=DataEntryDb;UID=dataentry;PWD=entrz@01')
cursor = cnxn.cursor()

root_url = 'https://www.yellowpages.com'


class YellowPageSpider(scrapy.Spider):

    name = 'yellow page spider'

    def __init__(self, search='', page_limit=1, *args, **kwargs):
        super(YellowPageSpider, self).__init__(*args, **kwargs)

        self.start_urls = []
        states = states_list.split("\n")
        for location in states:
            if location == "":
                continue
            page = 0
            loop = True
            while loop:
                initial_url = '%s/search?search_terms=%s&geo_location_terms=%s' % (root_url, search, location)
                url = initial_url if page == 0 else initial_url + "&page=" + str(page)
                self.start_urls.append(url)
                page += 1
                if page > page_limit:
                    loop = False

            logging.info(self.start_urls)

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

            vcard['scraping_source_id'] = "YP-" + str(_id)
            result = cursor.execute("SELECT SyncGUID from ScrapedCompany WHERE SyncGUID='%s'" % vcard.get('scraping_source_id'))
            result = result.fetchall()
            logging.info(result)

            if len(result) == 0:

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

                insert_data(vcard)
                yield scrapy.http.Request(link, callback=self.get_email)

    def get_email(self, response):
        scraping_source_id = "YP-" + (response.request.url.split('lid=')[1])
        logging.info(scraping_source_id)
        email = response.css('.email-business').xpath('@href').extract_first()
        email = None if email is None else email.split('mailto:')[1]
        website = response.css('.website-link').xpath('@href').extract_first()

        logging.info("----------------------")
        logging.info(email)
        logging.info(website)
        logging.info("----------------------")

        if email is not None or website is not None:
            sql = "UPDATE ScrapedCompany SET CompanyEmail='%s', CompanyWebsite='%s' WHERE SyncGUID='%s'"\
                  % (email, website, scraping_source_id)
            logging.info(sql)
            cursor.execute(sql)
            cnxn.commit()


def insert_data(vcard):

    sql = "INSERT INTO ScrapedCompany " \
          "(CompanyPhone, CompanyAddress, CompanyName, CompanyEmail, CompanyLogoUrl, NumberOfEmployees, " \
          "ScrapingSourceID, IsImportable, CompanyWebsite, CountryID, SyncGUID, IndustryFocuses, SourceUrl) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
            vcard.get('phone'),
            vcard.get('address'),
            vcard.get('company'),
            vcard.get('email'),
            vcard.get('logo_url'),
            vcard.get('number_of_employees'),
            1,
            vcard.get('is_importable'),
            '',
            1,
            vcard.get('scraping_source_id'),
            vcard.get('industry_focus'),
            vcard.get('link')
          )
    logging.info(sql)
    try:
        cursor.execute(sql)
        cnxn.commit()
    except Exception as e:
        pass