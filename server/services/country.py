from server.models import entities
from server.config.applogging import ResponseLoggerMiddleware
import logging
import falcon
import json
# import cgi
# from server.extraction.extract import *
# from server.extraction.extract import from_stream, _write_stream
# import re
import traceback
# from server.services.email import Mail


class CountryService:

    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.country_modelObj = entities.CountryDoc

    def save(self, country):
        doc = self.country_modelObj(country_name=country.get('country_name'),
                                    country_code=country.get('country_code'),
                                    desc=country.get('desc'))
        doc.save()

    def country_posting(self, dataset):
        try:
            country = {'country_name': dataset['country_name'],
                       'country_code': dataset['country_code'],
                       'desc': dataset['desc']}

            self.save(country)
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def get_records(self):
        return self.country_modelObj.objects()

    def country_updating(self, dataset):
        try:
            update_obj = self.country_modelObj.objects(country_name=dataset['txn'])
            print(dataset['country_name'], dataset['desc'])
            update_obj.update(set__country_name=dataset['country_name'],
                              set__country_code=dataset['country_code'],
                              set__desc=dataset['desc'])
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def country_status(self, dataset):
        try:
            update_obj = entities.CountryDoc.objects(country_name=dataset['country_name'])

            if dataset['status'].lower() == 'true':
                update_obj.update(set__status=bool(True))
            elif dataset['status'].lower() == 'false':
                update_obj.update(set__status=bool(False))
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def pull_reference_data(self, country):
        if country:
            obj = self.country_modelObj.objects(country_name=country)
        else:
            obj = self.country_modelObj.objects(country_name=country)
        return obj
