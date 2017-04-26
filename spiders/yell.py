import logging

import scrapy
from commons.connect import DBConnect

from data.uk_cities import uk_city_list


root_url = 'https://www.yell.com'


class YellSpider(scrapy.Spider):

    name = 'Yell spider'
    connect = None

    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 5,
        'AUTOTHROTTLE_ENABLED': False,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'HTTP_PROXY': 'http://127.0.0.1:8123',
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'RETRY_TIMES': 20,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 408, 403],
        # 'DOWNLOADER_MIDDLEWARES': {
        #      'middlewares.RandomUserAgentMiddleware': 400,
        #      'middlewares.ProxyMiddleware': 410,
        #      'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
        # }
    }

    def __init__(self, search='', *args, **kwargs):
        self.connect = DBConnect()

        super(YellSpider, self).__init__(*args, **kwargs)

        self.start_urls = []
        # url = '%s/ucs/UcsSearchAction.do?keywords=%s&location=%s&scrambleSeed=420366096' % (root_url, search, "Braintree")
        # self.start_urls.append(url)

        states = uk_city_list.split("\n")
        for location in states:
            if location == "":
                continue
            url = '%s/ucs/UcsSearchAction.do?keywords=%s&location=%s' % (root_url, search, location)
            self.start_urls.append(url)

        logging.info(self.start_urls)

    def parse(self, response):
        #
        # for setting in self.settings:
        #     logging.info(setting + " : " + str(self.settings.get(setting)))

        #yield scrapy.http.Request('https://www.yell.com/biz/fix-it-up-blackwood-901448702/', callback=self.get_content)
        container = response.css('div.businessCapsule')

        for dom in container:

            link = dom.css('div div a').xpath('@href').extract_first()
            logging.info(link)
            yield scrapy.http.Request(root_url + link, callback=self.get_content)

        next_page = response.css('.pagination--next').xpath('@href').extract_first()

        if next_page is not None:
            logging.info("--------nextpage----------")
            n = root_url + next_page
            logging.info(n)
            yield scrapy.http.Request(n)

    def get_content(self, response):

        url_split = response.request.url.split('-')
        data_id = "YL-" + str(url_split[len(url_split) - 1].split('/')[0])
        capsule = response.css("div.businessCapsule")

        vcard = dict()
        vcard['scraping_source_id'] = data_id
        exist = self.connect.is_exist(data_id)

        if not exist:

            company = response.css('h1.businessCapsule--title ::text').extract_first()
            logging.info(company)
            vcard['company'] = company
            addreses = capsule.css('p.address span ::text').extract()
            addr = ''
            for a in addreses:
                addr += addr + a + ", "
            vcard['address'] = addr
            phone = response.css('.business-telephone ::text').extract_first()
            vcard['phone'] = None if phone is None else phone.replace('\n', "")
            industry = response.css('ol.breadcrumbs ::text').extract()
            vcard['industry_focus'] = industry[14] if len(industry) > 0 else None
            logo_url = capsule.css('div.businessCapsule--logo img').xpath("@src").extract_first()
            vcard['logo_url'] = root_url + logo_url if logo_url is not None else None
            vcard['link'] = response.request.url

            containers = response.css('div.businessCapsule--callToAction a').xpath("@href").extract()
            logging.info(containers)

            vcard['website'] = containers[0] if len(containers) > 0 else ''
            vcard['email'] = containers[1] if len(containers) > 1 else ''
            vcard['number_of_employees'] = 1
            vcard['is_importable'] = ''
            vcard['country_id'] = 2
            vcard['data_source'] = 2

            if company is None:
                logging.info("---------NO COMPANY NAME ERROR-----------")
                logging.info(vcard.get('link'))
                logging.info("---------NO COMPANY NAME ERROR-----------")

            else:
                self.connect.insert_data(vcard)
            logging.info(vcard)
