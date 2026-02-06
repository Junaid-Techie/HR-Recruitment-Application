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
from server.models.entities import *
from server.services.scheduler import Scheduler
from server.services.job import Job
from server.services.application import Application
from server.services.server_validation import Validations
from server.services.email import Mail
# from falcon_jinja2 import FalconTemplate
# from server.models.entities import *
# from server.models.entities import CandidateDoc, JobDoc, PreScreeningDoc, ApplicationDoc, ScheduleDoc
from server.config.applogging import ResponseLoggerMiddleware


# template_path = "D:\src\hiring-office\server\\ui"
# falcon_template = FalconTemplate(path=template_path)


class Scheduling:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.mail = Mail()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.service = Scheduler()
        self.interviewer_validation = Validations()
        # print(self.applogging)

    def on_post_assign_interviewer(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('job'),
                   'candidate': req.context.model['candidate'],
                   'interviewer_name': req.get_param('interviewer_name'),
                   'interviewer_email': req.get_param('interviewer_email'),
                   'interviewer_phone': req.get_param('interviewer_phone'),
                   'scheduled_datetime': req.get_param('scheduled_datetime'),
                   'round_number': req.get_param('round_number'),
                   'interview_channel': req.get_param('interview_channel'),
                   'interview_type': req.get_param('interview_type')}
        candidate = self.service.get_candidate_name(dataset)
        exist_data = self.interviewer_validation.interviewer_validate(dataset)
        if exist_data:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({
                'message': dataset['interviewer_name'] + ' is already scheduled for the candidate ' +
                           candidate + ' for ' + dataset['interview_type'] + ' of round ' + dataset['round_number'],
                'status': 'failed'})
        else:
            output = self.service.scheduler_assign_interviewer(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(
                    {'message': 'Interviewer ' + dataset[
                        'interviewer_name'] + ' is successfully assigned to ' + candidate,
                     'status': 'success'})
            else:
                # self.logging .error(traceback.format_exc())
                resp.body = json.dumps(
                    {'message': 'Failed in scheduling for  ' + str(candidate) + traceback.format_exc(),
                     'status': 'failed'})
                logging.error(traceback.format_exc())

    def on_get(self, req, resp):
        pass

    def on_put_re_assign(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('job'),
                   'candidate': req.context.model['candidate'],
                   'interviewer_name': req.get_param('interviewer_name'),
                   'interviewer_email': req.get_param('interviewer_email'),
                   'interviewer_phone': req.get_param('interviewer_phone'),
                   'scheduled_datetime': req.get_param('scheduled_datetime'),
                   'round_number': req.get_param('round_number'),
                   'interview_type': req.get_param('interview_type')}
        output = self.service.scheduler_reasignment(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': dataset['interviewer_name'][0] + "'s details has been updated.",
                'status': 'success'})
        else:
            resp.body = json.dumps(
                {'message': 'Failed to update the details of ' + dataset['interviewer_name'][0],
                 'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_recruiter_status(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('jobcode'),
                   'c_email': req.context.model['c_email'],
                   'i_email': req.context.model['i_email'],
                   'schedule_status': req.context.model['schedule_status'],
                   'comment': req.context.model['comment'],
                   'i_type': req.context.model['i_type'],
                   'i_name': req.context.model['i_name'],
                   'sch_date': req.context.model['sch_date'],
                   'c_name': req.context.model['c_name']}
        output = self.service.scheduler_recruiter_status(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': dataset['c_name'][0] + "'s scheduled " + dataset['schedule_status'][0]
                                               + ' successfully!.',
                                    'status': 'success'})
        else:
            resp.body = json.dumps(
                {'message': 'Failed to update the details of ' + dataset['c_name'][0],
                 'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_interviewer_edit(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('job'),
                   'candidate': req.context.model['candidate'],
                   'scheduled_datetime': req.context.model['scheduled_datetime'],
                   'interviewer_name': req.get_param('interviewer_name'),
                   'interviewer_email': req.get_param('interviewer_email'),
                   'interview_type': req.get_param('interview_type'),
                   'interviewer_acknowledge_comments': req.get_param('interviewer_acknowledge_comments')}
        output = self.service.scheduler_interviewer_edit(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(
                {'message': dataset['interviewer_name'] + "'s details have been updated.",
                 'status': 'success'})
        else:
            resp.body = json.dumps({
                'message': 'Failed to update the details of ' + str(dataset['interviewer_name']),
                'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_interviewer_status(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'job': req.get_param('jobcode'),
                   'c_email': req.context.model['c_email'],
                   'i_email': req.context.model['i_email'],
                   'interviewer_acknowledgement': req.context.model['interviewer_acknowledgement'],
                   'comment': req.context.model['comment'],
                   'r_number': req.context.model['r_number'],
                   'c_name': req.context.model['c_name'],
                   'sch_date': req.context.model['sch_date'],
                   'i_name': req.context.model['i_name']}
        output = self.service.scheduler_interviewer_status(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(
                {'message': dataset['c_name'][0] + "'s scheduled " + dataset['interviewer_acknowledgement'][0]
                            + ' successfully!.',
                 'status': 'success'})
        else:
            resp.body = json.dumps(
                {'message': 'Failed to update the details of ' + dataset['c_name'][0],
                 'status': 'Failed'})
            self.logging.error(traceback.format_exc())


class SchedulingAPI:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.mail = Mail()
        self.schedule_service = Scheduler()
        self.job_service = Job()
        self.interviewProcessObj = Application()

    def on_get(self, req, resp):
        pass

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        scheduler_data = self.schedule_service.scheduler_get_all()
        if scheduler_data is not None:
            resp.status = falcon.HTTP_201
            print(scheduler_data)
            resp.body = json.dumps(scheduler_data)
            self.logging.info('Listing out all schedules')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Candidate details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_shortlisted_jobs(self, req, resp, job):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        # dataset = {'job': job}
        # jobobj = self.job_service.get_data_byid(job)
        shortlist_data = self.interviewProcessObj.get_readyforschedule_by_job(job)
        dataset = []
        if shortlist_data is not None:
            for each in shortlist_data:
                dataset.append({'applicant': {'first_name': each.applicant.first_name,
                                              'last_name': each.applicant.last_name, 'email': each.applicant.email}})

            resp.status = falcon.HTTP_201
            resp.body = json.dumps(dataset)
            self.logging.info('Listing out all Shortlisted Candidates')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Shortlisted Candidate!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_notschedule(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        not_scheduled = self.schedule_service.scheduler_notscheduled()
        if not_scheduled is not None:
            resp.status = falcon.HTTP_201
            try:
                if req.get_param('api_cnt'):
                    resp.body = len(not_scheduled)
                    return resp.body
            except:
                pass
            resp.body = json.dumps(not_scheduled)
            self.logging.info('Listing out all Not Scheduled Candidates')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
