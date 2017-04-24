import logging

import scrapy

from data.us_states import states_list
from commons.connect import DBConnect


root_url = 'https://www.yellowpages.com'
TOTAL_PAGES = 0


class YellowPageSpider(scrapy.Spider):

    name = 'yellow page spider'
    connect = None

    def __init__(self, search='', *args, **kwargs):
        self.connect = DBConnect()

        super(YellowPageSpider, self).__init__(*args, **kwargs)

        self.start_urls = []
        states = states_list.split("\n")
        for location in states:
            if location == "":
                continue
            url = '%s/search?search_terms=%s&geo_location_terms=%s' % (root_url, search, location)
            self.start_urls.append(url)

        logging.info(self.start_urls)

    def parse(self, response):

        container = response.css('div.organic .v-card')
        for dom in container:
            vcard = {}

            id_c = dom.css('h2.n a').xpath('@href').extract_first()
            # logging.info(id_c)
            try:
                _id = int(id_c.split("lid=")[1])
            except Exception as e:
                continue

            vcard['scraping_source_id'] = "YP-" + str(_id)
            result = self.connect.cursor.execute("SELECT SyncGUID from ScrapedCompany WHERE SyncGUID='%s'" % vcard.get('scraping_source_id'))
            result = result.fetchall()
            logging.info(result)

            link = root_url + dom.css('.business-name').xpath('@href').extract_first()

            if len(result) == 0:
                yield scrapy.http.Request(link, callback=self.get_content)

        next_page = response.css('a.next.ajax-page').xpath("@href").extract_first()
        if next_page is not None:
            logging.info("---------------------")
            logging.info(next_page)
            logging.info("---------------------")
            yield scrapy.http.Request(root_url + next_page)

    def get_content(self, response):

        vcard = dict()
        scraping_source_id = "YP-" + (response.request.url.split('lid=')[1])
        vcard['scraping_source_id'] = scraping_source_id

        vcard['company'] = response.css('header article div.sales-info h1 ::text').extract_first()
        addresses = response.css('div.contact p.address span ::text').extract()
        addr = ''
        for a in addresses:
            addr = addr + a
        vcard['address'] = addr
        vcard['phone'] = response.css('p.phone ::text').extract_first()
        categories = response.css('dd.categories span a ::text').extract()
        cs = ''
        for c in categories:
            cs = cs + c + ", "
        vcard['industry_focus'] = cs
        vcard['logo_url'] = response.css('#business-info dl dd.logo img').xpath('@src').extract_first()
        vcard['link'] = response.request.url
        mailto = response.css('a.email-business').xpath("@href").extract_first()
        vcard['email'] = '' if mailto is None else mailto.split('mailto:')[1]
        vcard['website'] = response.css('#main-header div a.website-link').xpath('@href').extract_first()
        vcard['number_of_employees'] = 1
        vcard['is_importable'] = ''
        vcard['country_id'] = 1
        vcard['data_source'] = 1

        logging.info(vcard)
        self.connect.insert_data(vcard)
