import falcon
import json
import logging
# from server.extraction.extract import from_stream
from server.services.feedback import Feed
from server.services.server_validation import Validations
# from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback
# import datetime
# import pathlib
# import jinja2
from falcon_jinja2 import FalconTemplate
# import server.config as cfg
from server.services.email import Mail


# from server.config.config import get_html_template_path
# template_path =  get_html_template_path()
# STATIC_PATH = pathlib.Path(__file__).parent / 'static'
# print(str(STATIC_PATH))
# template_path = "C:\\Users\\rsurampally\Projects\hiring-office\server\\ui"
# falcon_template = FalconTemplate(path=template_path)


class Feedback:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.service = Feed()
        self.feedback_validation = Validations()
        self.mail = Mail()

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('job'),
                   'candidate': req.context.model['Candidate'],
                   'interview_feedback': req.get_param('interview_feedback'),
                   'interview_type': req.get_param('interview_type'),
                   'round_number': req.get_param('round_number'),
                   'next_round': req.get_param('next_round'),
                   'jd': req.get_param('jd'),
                   'image': req.get_param('image'),
                   'content_type': req.content_type}
        round_select = self.feedback_validation.feedback_validate_round_selection(dataset)
        round_repeat = self.feedback_validation.feedback_validate_round_repeat(dataset)
        if round_select:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({'message': 'Please, do not select the same round.',
                                    'status': 'failed'})
        elif round_repeat:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({
                'message': 'Feedback for selected round is already saved. Please, select another round.',
                'status': 'failed'})
        else:
            output = self.service.feedback_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({
                    'message': 'FeedBack Has been Added',  # str(sched_obj.job.code) +
                    'status': 'success'})
            else:
                resp.body = json.dumps(
                    {'message': 'Failed in adding feedback  ' + traceback.format_exc(),
                     'status': 'failed'})  # str(sched_obj.job.code) +
                logging.error(traceback.format_exc())

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        output = self.service.get_data()
        # print(output)
        if output is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(output)
            # resp.body = json.dumps({'message': 'Successful in fetching feedback details!!!'})
            self.logging.info('Listing out all Feedback')
        else:
            resp.body = json.dumps({'message': 'Failed in fetching feedback details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_shortlisted_applications(self, req, resp, job):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': job}
        output = self.service.shortlisted_applications(dataset)
        # print(job)
        if output is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(output)
            # resp.body = json.dumps({'message': 'Successful in fetching shortlisted feedback details!!!'})
            self.logging.info('Listing out all shortlisted Feedback')
        else:
            resp.body = json.dumps({'message': 'Failed in fetching shortlisted feedback details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_interview_type(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('job'),
                   'candidate': req.get_param('candidate')}
        output = self.service.interview_type(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(output)
            # resp.body = json.dumps({'message': 'Successful in fetching interview type details!!!'})
            self.logging.info('Listing out all interview type details')
        else:
            resp.body = json.dumps({'message': 'Failed in fetching interview type details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
