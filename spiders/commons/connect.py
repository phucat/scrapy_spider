import pyodbc

# install
# sudo apt-get install unixodbc-dev
# pip install pyodbc
# pip install sqlalchemy
# https://blogs.msdn.microsoft.com/sqlnativeclient/2016/10/20/odbc-driver-13-0-for-linux-released/
import logging

import datetime
from retry import retry


class DBErrorException(Exception):
    pass


server = '81.2.234.35'
database = 'DataEntryDb'
username = 'dataentry'
password = 'entrz@01'


class DBConnect(object):

    def __init__(self):

        self.conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'
                                   % (server, database, username, password))
        self.cursor = self.conn.cursor()


    def insert_data(self, vcard):

        sql = "INSERT INTO ScrapedCompany " \
              "(CreatedDate, CreatedBy, CompanyPhone, CompanyAddress, CompanyName, CompanyEmail, CompanyLogoUrl, NumberOfEmployees, " \
              "ScrapingSourceID, IsImportable, CompanyWebsite, CountryID, SyncGUID, IndustryFocuses, SourceUrl) " \
              "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                11,
                vcard.get('phone'),
                vcard.get('address').replace("'", "") if vcard.get('address') is not None else None,
                vcard.get('company').replace("'", "") if vcard.get('company') is not None else None,
                vcard.get('email'),
                vcard.get('logo_url'),
                vcard.get('number_of_employees'),
                vcard.get('data_source'),
                vcard.get('is_importable'),
                vcard.get('website'),
                vcard.get('country_id'),
                vcard.get('scraping_source_id'),
                vcard.get('industry_focus'),
                vcard.get('link')
              )

        logging.info(sql)

        try:
            self.cursor.execute(sql)
            self.conn.commit()
            logging.info("----------")
            logging.info("successfully saved on db : %s" % vcard.get('company'))
            logging.info("----------")

        except Exception as e:
            logging.info("####### ERROR!! ########")
            logging.error(e)
            error_code = e[0]

    def is_exist(self, source_id):
        result = self.cursor.execute(
            "SELECT SyncGUID from ScrapedCompany WHERE SyncGUID='%s'" % source_id)
        result = result.fetchall()
        logging.info(result)

        if len(result) == 0:
            return False

        return True
