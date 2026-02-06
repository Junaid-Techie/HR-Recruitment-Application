import falcon
import json
import logging
import traceback
from server.services.city import CityService
from server.services.server_validation import Validations
from server.models.entities import CityDoc, StateDoc, CountryDoc
from server.config.applogging import ResponseLoggerMiddleware
# from bson import json_util
# from pymongo.errors import DuplicateKeyError
# # import dateutil.parser
# from bson.errors import InvalidId
# from bson.objectid import ObjectId
# import pymongo
# from bson.objectid import ObjectId
# from pymongo import UpdateOne
# from server.extraction.extract import from_stream
# from server.models.entities import *


class City:
    def __init__(self):
        # super().__init__
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.city_service = CityService()
        self.city_validation = Validations()

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'country_name': req.get_param('country_name'),
                   'state_name': req.get_param('state_name'),
                   'city_name': req.get_param('city_name'),
                   'city_desc': req.get_param('city_desc'),
                   'address': req.get_param('address')}
        exist_city = self.city_validation.city_validate(dataset)
        if exist_city:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({'message': "'" + dataset['city_name'] +
                                               "' is already present in City Profile.",
                                    'status': 'failed'})
        else:
            output = self.city_service.city_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({
                    'message': dataset['city_name'] + ' has been added to the City Profile.',
                    'status': 'success'})
            else:
                resp.body = json.dumps({
                    'message': 'Failed in adding ' + dataset['city_name'] + ' to the City profile.'
                               + traceback.format_exc(),
                    'status': 'failed'})
                logging.error(traceback.format_exc())

    def on_get(self, req, resp):
        pass

    def on_put_update(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'country_name': req.get_param('country_name'),
                   'state_name': req.get_param('state_name'),
                   'city_name': req.get_param('city_name'),
                   'city_desc': req.get_param('city_desc'),
                   'address': req.get_param('address'),
                   'txn': req.context.model['txn']}
        output = self.city_service.city_update(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': dataset['city_name'] + ' has been updated!',
                                    'status': 'success'})
        else:
            resp.body = json.dumps(
                {'message': 'Failed in updating ' + str(dataset['city_name']) + traceback.format_exc(),
                 'status': 'failed'})
            logging.error(traceback.format_exc())

    def on_delete_trash_collection(self, req, resp, data):
        resp.status = falcon.HTTP_200
        try:
            collect_obj = CityDoc.objects(city_name=data)
            if collect_obj.delete():
                resp.body = json.dumps({'message': data + ' successfully deleted',
                                        'status': 'success'})
                self.logging.info(data + ' successfully deleted')

        except:
            resp.body = json.dumps({'message': 'error occurred on deletion',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'status': req.get_param('status'),
                   'city_name': req.context.model['city_name'][0],
                   'country_name': req.get_param('country_name'),
                   'state_name': req.get_param('state_name')}
        output = self.city_service.status_edit(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': 'City profile successfully ' + 'Enabled!!!' if dataset['status'] == 'true'
                else 'candidate profile successfully ' + 'Disabled!!!', 'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the Status for ' + str(dataset['city_name']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())


class CityAPI:
    def __init__(self):
        # super.__init__
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.city_service = CityService()

    def on_get(self, req, resp):
        pass

    def on_get_byname(self, req, resp, name):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        try:
            rec_object = CityDoc.objects(city_name=name)
            data_list = []
            for x in rec_object:
                data_list.append({'country_name': x.country.country_name,
                                  'state_name': x.state.state_name,
                                  'city_name': x.city_name,
                                  'city_desc': x.city_desc,
                                  'address': x.address})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching ' + name + ' details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        city_data = self.city_service.city_getall()
        if city_data is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(city_data)
            self.logging.info('Listing out all cities')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching city details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_post_states(self, req, resp):
        resp.status = falcon.HTTP_200
        try:
            country = CountryDoc.objects(country_name=req.get_param('country_name')).first()
            state = StateDoc.objects(country=country)
            dataset = []
            for it in state:
                dataset.append({'state_name': it.state_name})
            resp.body = json.dumps(dataset)
            self.logging.info('Listing out countries')
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching country details!!!'})
            self.logging.error(traceback.format_exc())

    def on_post_cities(self, req, resp):
        resp.status = falcon.HTTP_200
        try:
            country = CountryDoc.objects(country_name=req.get_param('country_name')).first()
            state = StateDoc.objects(state_name=req.get_param('state_name'),
                                     country=country).first()
            # state = StateDoc.objects(state_name=req.get_param('state_name'),
            # country_country_name=req.get_param('country_name')).first()
            resp.body = state.to_json()
            self.logging.info('Listing out cities wrt states and countries')
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching country details!!!'})
            self.logging.error(traceback.format_exc())
