import falcon
import json
import logging
import traceback
from server.services.country import CountryService
from server.services.server_validation import Validations
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
from server.models.entities import *


class Country:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.country_service = CountryService()
        self.country_validation = Validations()

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        dataset = {'country_name': req.get_param('country_name'),
                   'country_code': req.get_param('country_code'),
                   'desc': req.get_param('desc')}

        exist_country = self.country_validation.country_validate(dataset)
        if exist_country:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({
                'message': "'" + dataset['country_name'] + "' is already present in the Country Profile.",
                'status': 'failed'})
        else:
            output = self.country_service.country_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({
                    'message': "'" + dataset['country_name'] + "' Has Been added to the Country Profile.",
                    'status': 'success'})
            else:
                resp.body = json.dumps({
                    'message': "Failed in adding '" + dataset['country_name'] + "' to the Country Profile."
                               + traceback.format_exc(),
                    'status': 'failed'})
                logging.error(traceback.format_exc())

    def on_get(self, req, resp):
        pass

    def on_put_update(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'txn': req.get_param('txn'),
                   'country_name': req.get_param('country_name'),
                   'country_code': req.get_param('country_code'),
                   'desc': req.get_param('desc')}
        output = self.country_service.country_updating(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(
                {'message': dataset['country_name'] + "'s details has been updated.",
                 'status': 'success'})
            # self.logging.info(req.get_param('first_name') + ' successfully updated')
        else:
            resp.body = json.dumps({'message': "Failed to update the details of '" + dataset['country_name'] + "'",
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_delete_trash_collection(self, req, resp, data):
        resp.status = falcon.HTTP_200
        try:
            collect_obj = self.country_service.delete(country_name=data)
            if collect_obj:
                resp.body = json.dumps({'message': data + ' successfully deleted',
                                        'status': 'success'})
                self.logging.info(data + ' successfully deleted')

        except:
            resp.body = json.dumps({'message': 'error occurred on deletion'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'country_name': req.get_param("country_name"),
                   'status': req.get_param("status")}
        output = self.country_service.country_status(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': dataset['country_name'] + ' successfully Enabled!!!'
            if dataset['status'] == 'true' else dataset['country_name'] + ' successfully Disabled!!!',
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': "Failed to update the Status for '" + dataset['country_name'] + "'",
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())


class CountryAPI:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.service = CountryService()

    def on_get(self, req, resp):
        pass

    def on_get_byname(self, req, resp, name):
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.service.pull_reference_data(name)
            data_list = []
            for x in rec_object:
                data_list.append({'country_name': x.country_name,
                                  'country_code': x.country_code,
                                  'desc': x.desc})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching ' + name + ' details!!!',
                                    'status': 'failed'})

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.service.get_records()
            json_data = rec_object.to_json()
            resp.body = json_data
            self.logging.info('Listing out all countries')
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching recruiters details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
