from server.models.entities import *
# import falcon
# import json
import logging
# from bson import json_util
# from pymongo.errors import DuplicateKeyError
# import dateutil.parser
import traceback
# from bson.errors import InvalidId
# from bson.objectid import ObjectId
# import pymongo
# from bson.objectid import ObjectId
# from pymongo import UpdateOne
# from server.extraction.extract import from_stream
# from server.models.entities import *
# from server.models.entities import StateDoc, CountryDoc
from server.config.applogging import ResponseLoggerMiddleware


class StateService:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.state_modelObj = StateDoc
        self.country_modelObj = CountryDoc

    def save(self, state):
        doc = self.state_modelObj(country=state.get('country_name'),
                                  state_name=state.get('state_name'),
                                  state_desc=state.get('state_desc'))
        doc.save()

    def state_posting(self, dataset):
        self.logging.info('request started for Posting in ' + str(__file__))
        country = CountryDoc.objects(country_name=dataset['country_name']).first()
        try:
            state = {'state_name': dataset['state_name'],
                     'state_desc': dataset['state_desc'],
                     'country_name': country}
            self.save(state)
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def state_updating(self, dataset):
        try:
            country_obj = self.country_modelObj.objects(country_name=dataset['country']).first()
            newcountry_obj = self.country_modelObj.objects(country_name=dataset['country_name']).first()

            update_obj = self.state_modelObj.objects(state_name=dataset['state'], country=country_obj)
            update_obj.update(set__state_name=dataset['state_name'],
                              set__state_desc=dataset['state_desc'], set__country=newcountry_obj)
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def status_update(self, dataset):
        try:
            update_obj = self.state_modelObj.objects(state_name=dataset['state_name'], country=dataset['country'])
            if dataset['status'].lower() == 'true':
                update_obj.update(set__status=bool(True))
            elif dataset['status'].lower() == 'false':
                update_obj.update(set__status=bool(False))
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def get_records(self):
        return self.state_modelObj.objects()

    def pull_reference_data(self, country, state):
        if country and state:
            country_obj = self.country_modelObj.objects(country_name=country).first()
            obj = self.state_modelObj.objects(country=country_obj, state_name=state)
        else:
            obj = self.state_modelObj.objects()
        return obj
