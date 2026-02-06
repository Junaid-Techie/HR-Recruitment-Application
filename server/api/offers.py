import falcon
import json
import logging
# from server.extraction.extract import from_stream
from server.services.offer import Offer
# from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback
# import datetime
# import pathlib
# import jinja2
# from falcon_jinja2 import FalconTemplate
# import server.config as cfg
# from server.models import entities
from server.services.email import Mail


# from server.config.config import get_html_template_path
# template_path =  get_html_template_path()
# STATIC_PATH = pathlib.Path(__file__).parent / 'static'
# print(str(STATIC_PATH))


class OfferApi:
    def __init__(self):
        self.offer_service = Offer()
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('job'),
                   'applicant': req.context.model['applicant'],
                   'comments': req.get_param('comments'),
                   'join_date': req.get_param('join_date'),
                   'offer_attachment': req.get_param('offer_attachment')}
        output = self.offer_service.offer_posting(dataset)
        candidate_name = self.offer_service.get_candidate_name(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': candidate_name + ' is successfully added to job offer list.',
                'status': 'success'})
        else:
            resp.body = json.dumps(
                {'message': 'Failed in adding ' + candidate_name + ' to Job offer list.' + traceback.format_exc(),
                 'status': 'failed'})
            logging.error(traceback.format_exc())

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        output = self.offer_service.get_data()
        if output is not None:
            resp.body = json.dumps(output)
            self.logging.info('Listing out all Job Offered list')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Job Offered list details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_accepted_offers(self, req, resp, job):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': job}
        output = self.offer_service.accepted_offer(dataset)
        if output is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(output)
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Accepted job offer details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
