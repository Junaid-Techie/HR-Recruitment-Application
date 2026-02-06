import falcon
import json
import logging
# from bson import json_util
# from pymongo.errors import DuplicateKeyError
# # import dateutil.parser
import traceback
# from bson.errors import InvalidId
# from bson.objectid import ObjectId
# import pymongo
# from bson.objectid import ObjectId
# from pymongo import UpdateOne
# from server.extraction.extract import from_stream
from server.services.state import StateService
from server.services.server_validation import Validations
# from server.models.entities import *
# from server.models.entities import StateDoc, CountryDoc
from server.config.applogging import ResponseLoggerMiddleware


class State:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.state_service = StateService()
        self.state_validation = Validations()

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        self.logging.info('request started for Posting in ' + str(__file__))
        dataset = {'state_name': req.get_param('state_name'),
                   'state_desc': req.get_param('state_desc'),
                   'country_name': req.get_param('country_name')}
        exist_state = self.state_validation.state_validate(dataset)
        if exist_state:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({
                'message': "'" + dataset['state_name'] + "' is already present in the State Profile.",
                'status': 'failed'})
        else:
            output = self.state_service.state_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({
                    'message': "'" + dataset['state_name'] + "' has been added to the State Profile.",
                    'status': 'success'})
            else:
                # self.logging .error(traceback.format_exc())
                resp.body = json.dumps(
                    {'message': "Failed in adding '" + dataset[
                        'state_name'] + "' to the State Profile." + traceback.format_exc(),
                     'status': 'failed'})
                logging.error(traceback.format_exc())

    def on_get(self, req, resp):
        pass

    def on_put_update(self, req, resp):
        resp.status = falcon.HTTP_200
        txn = qualify = req.context.model["txn"]
        (country, state) = txn.split('#')
        dataset = {'state': state, 'country': country,
                   'state_name': req.get_param('state_name'),
                   'state_desc': req.get_param('state_desc'), 'country_name': req.get_param('country_name')}
        output = self.state_service.state_updating(dataset)
        if output:
            resp.body = json.dumps({'message': dataset['state_name'] + "'s details has been updated.",
                                    'status': 'success'})
            # self.logging.info(req.get_param('first_name') + ' successfully updated')
        else:
            resp.body = json.dumps({'message': "Failed to update the details of '" + dataset['state_name'] + "'.",
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_delete_trash_collection(self, req, resp, data):
        resp.status = falcon.HTTP_200
        try:
            collect_obj = self.state_service.pull_reference_data(data)
            if collect_obj.delete():
                resp.body = json.dumps({'message': data + ' successfully deleted',
                                        'status': 'success'})
                self.logging.info(data + ' successfully deleted')

        except:
            resp.body = json.dumps({'message': 'error occurred on deletion',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        resp.status = falcon.HTTP_200
        country_name = req.get_param('country_name')
        countryObj = self.state_service.country_modelObj.objects(country_name=country_name).first()
        dataset = {'state_name': req.get_param("state_name"),
                   'status': req.get_param("status"), 'country': countryObj}
        output = self.state_service.status_update(dataset)
        if output:
            resp.body = json.dumps({'message': dataset['state_name'] + ' successfully ' + 'Enabled!!!'
            if dataset['status'] == 'true' else dataset['state_name'] + ' successfully ' + 'Disabled!!!',
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': "Failed to update the Status for '" + dataset['state_name'] + "'",
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())


class StateAPI:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.service = StateService()

    def on_get(self, req, resp):
        pass

    def on_get_byname(self, req, resp, name):
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.service.pull_reference_data(name)
            data_list = []
            for x in rec_object:
                data_list.append({'state_name': x.state_name,
                                  'state_desc': x.state_desc,
                                  'country_name': x.country.country_name})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed in fetching ' + name + ' details!!!',
                                    'status': 'failed'})

    def on_get_all(self, req, resp):
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.service.get_records()
            # print(json_data)
            data_list = []
            for x in rec_object:
                data_list.append({'state_name': x.state_name,
                                  'state_desc': x.state_desc,
                                  'country_name': x.country.country_name})
            resp.body = json.dumps(data_list)

            self.logging.info('Listing out all states')

        except:
            resp.body = json.dumps({'message': 'Listing out all state details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
