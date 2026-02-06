from server.models.entities import *
# import falcon
# import json
# import logging
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
# from server.models.entities import *
from server.config.applogging import ResponseLoggerMiddleware
# from server.services.application import Application
from server.services.email import Mail

class PreScreening:
    def __init__(self):
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.jobObj = JobDoc()
        self.appdoc = InterviewProcessDoc()

    def save(self, prescreening):
        job = self.jobObj.objects(code=prescreening.get('job')).first()
        InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=prescreening.get('candidate')).update_one(
            set__prescreen_status=prescreening.get('shortlist_status'), set__prescreen_comments=prescreening.get('comments'))

    def status_update(self, dataset):
        try:
            job = JobDoc.objects(code=dataset.get('jobcode')).first()
            InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset.get('c_email'), applicant__phone=dataset['c_phone']).update_one(
                set__prescreen_status=dataset.get('shortlist_status'),
                set__prescreen_comments=dataset.get('comments'))
            if dataset['shortlist_status'] == 'Accept':
                funObj = FunctionalOrgDoc.objects(org_email=job.functional_org[0]).first()
                self.mail.prescreen_sendmail(
                    {'to_email': funObj.org_email,
                     'cc_email': [dataset['c_email']],
                     'jobcode': dataset['jobcode'], 'c_name': dataset['c_name'], 'c_email': dataset['c_email'],
                     'shortlist_status': dataset['shortlist_status']})

            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def ready_for_prescreening(self):
        return InterviewProcessDoc.objects(prescreen_status = "New")


    def pull_data(self):
        data_list = []

        try:
            rec_object = self.ready_for_prescreening()
            for canobj in rec_object:
                if canobj.job._data['job_status'] not in ('New', 'Open', 'Active'):
                    continue
                prescreen_status = 'New'
                prescreen_comments = ''
                try:

                    prescreen_status= canobj.prescreen_status
                    prescreen_comments = canobj.prescreen_comments

                except:
                    pass

                try:
                    primary_skill = canobj.applicant.primary_skill
                except:
                    primary_skill  = []
                try:
                    last_name = canobj.applicant.last_name
                except:
                    last_name = " "

                data_list.append({'candidate_name': canobj.applicant.first_name+' '+ str(last_name),
                                          'candidate_email': canobj.applicant.email,
                                          'candidate_phone': canobj.applicant.phone,
                                          'candidate_primary_skill': primary_skill,
                                          'candidate_prescreen_status': prescreen_status or 'New',
                                          'resume': '',
                                          'comments': prescreen_comments or '',
                                          'jobcode':canobj.job._data['code']})
        except:
            pass
        return data_list

    def prescreen_notaccepted(self):
        data_list = []
        try:
            rec_object = InterviewProcessDoc.objects(prescreen_status__ne = "Accept")
            for obj in rec_object:
                if obj.job.job_status == "Open" :
                    data_list.append({'jobcode': obj.job.code,
                                      'candidate_name': obj.applicant.first_name + " " + obj.applicant.last_name,
                                      'candidate_email': obj.applicant.email,
                                      'candidate_phone': obj.applicant.phone,
                                      'candidate_primary_skill': obj.applicant.primary_skill,
                                      })
            self.logging.info('Listing out all jobs')
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def prescreenicon_count(self):
        return InterviewProcessDoc.objects(prescreen_status__ne = "Accept").count()
