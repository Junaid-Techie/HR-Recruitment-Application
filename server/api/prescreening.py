import falcon
import json
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
from server.services.prescreening import PreScreening
from server.models.entities import *
from server.config.applogging import ResponseLoggerMiddleware


class Prescreening:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.service = PreScreening()
        # print(self.applogging)

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))

        try:
            prescreening = {'job': req.get_param('job'),
                            'candidate': req.get_param('email'),
                            'shortlist_status': req.get_param('status'),
                            'prescreen_comments': req.get_param('comments')}
            self.service.save(prescreening)
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': 'Resume has been Successfully Shortlisted!',
                'status': 'success'})
        except Exception as e:
            # self.logging .error(traceback.format_exc())
            resp.body = json.dumps(
                {'message': 'Failed in short listing the resume' + traceback.format_exc()})
            logging.error(traceback.format_exc())

    def on_get(self, req, resp):
        pass

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'jobcode': req.get_param('jobcode'),
                   'c_name': req.context.model['c_name'][0],
                   'c_phone': req.context.model['c_phone'][0],
                   'c_email': req.context.model['c_email'][0],
                   'shortlist_status': req.get_param('shortlist_status'),
                   'comments': req.context.model['comment'][0]}
        output = self.service.status_update(dataset)
        if output:
            resp.body = json.dumps({
                'message': req.context.model['c_name'][0] + "'s resume "
                           + dataset['shortlist_status'] + ' successfully!.',
                'status': 'success'})
            # self.logging.info(req.get_param('first_name') + ' successfully updated')
        else:
            resp.body = json.dumps(
                {'message': 'Failed to update the details of ' + req.context.model['c_name'][0],
                 'status': 'Failed'})
            self.logging.error(traceback.format_exc())

    def on_delete_trash_collection(self, req, resp, data):
        resp.status = falcon.HTTP_200
        try:
            collect_obj = CityDoc.objects(city_name=data)
            if collect_obj.delete():
                resp.body = json.dumps({'message': data + ' successfully deleted'})
                self.logging.info(data + ' successfully deleted')

        except:
            resp.body = json.dumps({'message': 'error occurred on deletion'})
            self.logging.error(traceback.format_exc())


class PrescreeningAPI:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.service = PreScreening()

    def on_get(self, req, resp):
        pass

    def on_get_all(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            data_list = self.service.pull_data()
            resp.body = json.dumps(data_list)
            self.logging.info('Listing out all Candidate')
        except:
            print(traceback.format_exc())
            resp.body = json.dumps({'message': 'Failed in fetching Candidate details!!!'})
            self.logging.error(traceback.format_exc())

    def on_get_notaccepted(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            data_list = self.service.prescreen_notaccepted()
            try:
                if req.get_param('api_cnt'):
                    resp.body = len(data_list)
                    return resp.body
            except:
                pass
            resp.body = json.dumps(data_list)
            self.logging.info('Listing out all not accepted profiles')
        except:
            resp.body = json.dumps({'message': 'Failed in fetching Candidate details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
