# import falcon
# import json
# import logging
# from server.extraction.extract import from_stream
from server.models.entities import *
# from bson.objectid import ObjectId
from server.extraction.extract import from_stream, _write_stream
from server.config.applogging import ResponseLoggerMiddleware
import traceback
# import io
# import os
# import uuid
# import mimetypes
import datetime
import pathlib
#import jinja2
# from falcon_jinja2 import FalconTemplate
# import server.config as cfg
from server.models.entities import InterviewProcessDoc, FeedbackRefereceDoc, ImageReferenceDoc
from server.services.email import Mail


class Feed:
    def __init__(self):
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.interviewfeedbackObj = InterviewProcessDoc()
        self.referenceservice = FeedbackRefereceDoc()
        # self.imageservice = ImageReferenceDoc()
        # self._storage_path = storage_path

    def save(self, feed):
        doc = InterviewProcessDoc(feed)
        doc.save()

    def feedback_posting(self, dataset):
        try:
            docobj = dataset.get('jd')
            (temp_file, output) = _write_stream(docobj, docobj.filename, 'jd')
            with open(temp_file, 'rb') as fh:
                self.referenceservice.feedback.replace(fh, filename=temp_file, content_type=docobj.headers._headers[1][1])
            try:
                self.referenceservice.content = output
                self.referenceservice.filename = temp_file
                self.referenceservice.content_type = docobj.headers._headers[1][1]
                self.referenceservice.save()
            except:
                self.referenceservice.delete(filename=self.referenceservice.filename)
                self.referenceservice.save()

            # imgobj = dataset.get('image')
            # (temp_file, output) = _write_stream(imgobj, imgobj.filename, 'image')
            # with open(temp_file, 'rb') as fh:
            #     self.imageservice.image.put(fh, filename=temp_file, content_type=imgobj.headers._headers[1][1])
            # try:
            #     self.imageservice.content = output
            #     self.imageservice.filename = temp_file
            #     self.imageservice.content_type = imgobj.headers._headers[1][1]
            #     self.imageservice.save()
            # except:
            #     self.imageservice.delete(filename=self.imageservice.filename)
            #     self.imageservice.save()

            # imgobj = dataset.get('image')
            # ext = mimetypes.guess_extension(dataset['content_type'])
            # filename = "{uuid}{ext}".format(uuid=uuid.uuid4(), ext=ext)
            # image_path = os.path.join(self._storage_path, filename)
            # (temp_file, output) = _write_stream(imgobj, imgobj.filename, 'image')
            # with open(image_path, 'wb') as image_file:
            #     self.imageservice.image.put(image_file, filename=temp_file,content_type='image/png')
            # try:
            #     self.imageservice.content = output
            #     self.imageservice.filename = image_path
            #     self.imageservice.content_type = 'image/png'
            #     self.imageservice.save()
            # except:
            #     self.imageservice.delete(filename=self.imageservice.filename)
            #     self.imageservice.save()

            if dataset['next_round'] == 'Rejected':
                job = JobDoc.objects(code=dataset['job']).first()
                InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                            schedule__interviewer_acknowledge_status='Accepted',
                                            schedule__round_number=int(dataset['round_number'])).update(
                    set__schedule__S__next_round=dataset['next_round'],
                    set__schedule__S__interview_feedback_comments=dataset['interview_feedback'],
                    set__schedule__S__nextround_eligibility=False,
                    set__schedule__S__interview_evalution_doc=self.referenceservice.to_dbref(),
                    set__schedule__S__interview_evaluation_dt=str(datetime.datetime.now().date()))
            else:
                job = JobDoc.objects(code=dataset['job']).first()
                InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                            schedule__interviewer_acknowledge_status='Accepted',
                                            schedule__round_number=int(dataset['round_number'])).update(
                    set__schedule__S__next_round=dataset['next_round'],
                    set__schedule__S__interview_feedback_comments=dataset['interview_feedback'],
                    set__schedule__S__nextround_eligibility=True,
                    set__schedule__S__interview_evalution_doc=self.referenceservice.to_dbref(),
                    set__schedule__S__interview_evaluation_dt=str(datetime.datetime.now().date()))
            candidate = InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                                    schedule__interviewer_acknowledge_status='Accepted',
                                                    schedule__round_number=int(dataset['round_number'])).first()
            self.mail.feedback_sendmail(
                {'to_email': job.functional_org[0],
                 'cc_email': [dataset['candidate']],
                 'jobcode': job.code,
                 'candidate': candidate.applicant.first_name,
                 'interview_type': dataset['interview_type'],
                 'next_round': dataset['next_round']})
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def get_data(self):
        data_list = []
        try:
            feed_object = InterviewProcessDoc.objects(schedule__nextround_eligibility__exists = (True or False))
            for canobj in feed_object:
                data_list.append({'job': canobj.job.code,
                                  'candidate': canobj.applicant.first_name + ' ' + canobj.applicant.last_name,
                                  'interview_feedback': canobj.schedule[-1].interviewer_acknowledge_status,
                                  'feedback_date': canobj.schedule[-1].interview_evaluation_dt,
                                  'interview_type':  canobj.schedule[-1].interview_type,
                                  'next_round': canobj.schedule[-1].next_round})
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def shortlisted_applications(self, dataset):
        data_list = []
        try:
            jobobj = JobDoc.objects(code=dataset['job']).first().to_dbref()
            feed_object = InterviewProcessDoc.objects(job=jobobj, schedule__interviewer_acknowledge_status='Accepted')
            for eachschedule in feed_object:
                data_list.append({'first_name': str(eachschedule.applicant.first_name), 'last_name': str(eachschedule.applicant.last_name),
                                  'email': str(eachschedule.applicant.email)})
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def interview_type(self, dataset):
        data_list = []
        try:
            job_obj = JobDoc.objects(code=dataset['job']).first()
            feed_object = InterviewProcessDoc.objects(job=job_obj, schedule__interviewer_acknowledge_status='Accepted')
            for eachschedule in feed_object:
                data_list.append(
                    {'interview_type': str(eachschedule.schedule[-1].interview_type), 'round_number': eachschedule.schedule[-1].round_number})
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def pull_reference_data(self, jobcode, candidate_email, interview_type):
        job_obj = JobDoc.objects(code=jobcode).first()
        if jobcode and candidate_email:
            feedback_obj = InterviewProcessDoc.objects(job=job_obj.to_dbref(),
                                                       applicant__email=candidate_email,
                                                       schedule__interview_type=interview_type).first()
        else:
            feedback_obj = InterviewProcessDoc.objects(job=job_obj.to_dbref(),
                                                       applicant__email=candidate_email,
                                                       schedule__interview_type=interview_type).first()
        return feedback_obj
