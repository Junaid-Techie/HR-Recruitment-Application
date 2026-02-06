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
from server.services.email import Mail
from falcon_jinja2 import FalconTemplate
from server.models.entities import *
# from server.models.entities import CandidateDoc, JobDoc, InterviewProcessDoc
from server.config.applogging import ResponseLoggerMiddleware
# template_path = "D:\src\hiring-office\server\\ui"
# falcon_template = FalconTemplate(path=template_path)
from datetime import datetime
from server.services.email import Mail


class Scheduler:
    def __init__(self):
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.mail = Mail()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.jobObj = JobDoc()
        self.interviewerObj = InterviewerDoc()
        self.InterviewProcessObj = InterviewProcessDoc()
        self.scheduleObj = ScheduleDoc()

    def save(self, scheduling):
        self.interviewerObj.interviewer_email = scheduling.get('interviewer_email')
        self.interviewerObj.interviewer_name = scheduling.get('interviewer_name')
        self.interviewerObj.interviewer_phone = scheduling.get('interviewer_phone')
        self.scheduleObj.interviewer = self.interviewerObj
        self.scheduleObj.interview_type = scheduling.get('interview_type')
        self.scheduleObj.interview_channel = scheduling.get('interview_channel')
        self.scheduleObj.round_number = scheduling.get('round_number')
        self.scheduleObj.scheduled_datetime = scheduling.get('scheduled_datetime')

        # doc = self.interviewerObj\
        #         (
        #     job=scheduling.get('job'),
        #     candidate=scheduling.get('candidate'),
        #     interviewer_name=scheduling.get('interviewer_name'),
        #     interviewer_email=scheduling.get('interviewer_email'),
        #     interviewer_phone=scheduling.get('interviewer_phone'),
        #     scheduled_datetime=scheduling.get('scheduled_datetime'),
        #     interviewer_acknowledgement=scheduling.get('interviewer_acknowledgement'),
        #     interviewer_comments=scheduling.get('interviewer_comments'),
        #     candidate_acknowledgement=scheduling.get('candidate_acknowledgement'),
        #     candidate_comments=scheduling.get('comments'),
        #     recruiter_acknowledgement=scheduling.get('recruiter_acknowledgement'),
        #     recruiter_comments=scheduling.get('recruiter_comments'),
        #     schedule_status=scheduling.get('schedule_status'),
        #     round_number=scheduling.get('round_number'),
        #     interview_type=scheduling.get('interview_type'),
        # )

        InterviewProcessDoc.objects(
            job=scheduling.get('job').to_dbref(),
            applicant__email=scheduling.get('candidate')[0].applicant.email).update_one(push__schedule=self.scheduleObj)

    def scheduler_assign_interviewer(self, dataset):
        self.logging.info('request started for Posting in ' + str(__file__))
        job = JobDoc.objects(code=dataset['job']).first()
        candidate = InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                                prescreen_status='Accept')
        try:
            scheduling = {'job': job,
                          'candidate': candidate,
                          'interviewer_name': dataset['interviewer_name'],
                          'interviewer_email': dataset['interviewer_email'],
                          'interviewer_phone': dataset['interviewer_phone'],
                          'scheduled_datetime': dataset['scheduled_datetime'],
                          'round_number': dataset['round_number'],
                          'interview_channel': dataset['interview_channel'],
                          'interview_type': dataset['interview_type']}
            self.save(scheduling)
            try:
                self.mail.assigning_interviewer_sendmail(
                    {'to_email': dataset['interviewer_email'], 'cc_email': [job.functional_org[0]],
                     'schedule_dt': scheduling.get('scheduled_datetime'), 'jobcode': job.code,
                     'candidate': candidate[0].applicant.first_name, 'interviewer_name': dataset['interviewer_name'],
                     'interviewer_email': dataset['interviewer_email'],
                     'interview_type': dataset['interview_type']})
            except:
                logging.error(traceback.format_exc())
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def scheduler_reasignment(self, dataset):
        try:
            job = JobDoc.objects(code=dataset['job']).first()
            InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                        prescreen_status='Accept',
                                        schedule__round_number=int(dataset['round_number'])).update(
                set__schedule__S__interviewer__interviewer_name=dataset['interviewer_name'],
                set__schedule__S__interviewer__interviewer_email=dataset['interviewer_email'],
                set__schedule__S__interviewer__interviewer_phone=dataset['interviewer_phone'],
                set__schedule__S__scheduled_datetime=dataset['scheduled_datetime'],
                set__schedule__S__round_number=int(dataset['round_number']),
                set__schedule__S__interview_type=dataset['interview_type'], )
            candidate = InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                                    prescreen_status='Accept',
                                                    schedule__interview_type=dataset['interview_type']).first()
            self.mail.scheduler_reassign_sendmail({
                'to_email': dataset['interviewer_email'],
                'cc_email': [job.functional_org[0]],
                'schedule_dt': dataset['scheduled_datetime'], 'jobcode': job.code,
                'candidate': candidate.applicant.first_name, 'interviewer_name': dataset['interviewer_name'],
                'interviewer_email': dataset['interviewer_email'],
                'interview_type': dataset['interview_type']})
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def scheduler_recruiter_status(self, dataset):
        try:
            job = JobDoc.objects(code=dataset['job']).first()
            update_obj = InterviewProcessDoc.objects(job=job.to_dbref(),
                                                     applicant__email=dataset['c_email'][0],
                                                     prescreen_status='Accept',
                                                     schedule__interview_type=dataset['i_type'][0])
            # schedule__interviewer__interviewer_email = dataset['i_email'][0],
            schedule_status = dataset['schedule_status'][0]
            if dataset['schedule_status'][0] == 'Reschedule':
                schedule_status = 'Yet to Confirm'

            update_obj.update(set__schedule__S__schedule_status=schedule_status,
                              set__schedule__S__recruiter_comments=dataset['comment'][0])
            self.mail.interviewer_status_sendmail(
                {'to_email': dataset['i_email'][0],
                 'cc_email': [dataset['c_email'][0]], 'jobcode': job.code,
                 'candidate': dataset['c_name'][0], 'interviewer_name': dataset['i_name'][0],
                 'interview_type': dataset['i_type'][0], 'schedule_date': dataset['sch_date'][0],
                 'schedule_status': dataset['schedule_status'][0]})
            # else:
            #     schedule_obj = ScheduleDoc()
            #     schedule_obj.job = job_obj
            #     schedule_obj.applicant = candidate_obj
            #     schedule_obj.schedule_status = dataset['schedule_status'][0]
            #     schedule_obj.recruiter_comments = dataset['comment'][0]
            #     schedule_obj.save()
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def scheduler_interviewer_edit(self, dataset):
        try:
            job = JobDoc.objects(code=dataset['job']).first()
            dataset['interviewer_acknowledgement'] = 'Yet to Confirm'
            dataset['schedule_status'] = 'Yet to Confirm'

            InterviewProcessDoc.objects(job=job.to_dbref(),
                                        applicant__email=dataset['candidate'],
                                        prescreen_status='Accept',
                                        schedule__interview_type=dataset['interview_type']).update(
                set__schedule__S__scheduled_datetime=dataset['scheduled_datetime'],
                set__schedule__S__interviewer_acknowledge_comments=dataset['interviewer_acknowledge_comments'],
                set__schedule__S__interviewer_acknowledge_status=dataset['interviewer_acknowledgement'],
                set__schedule__S__schedule_status=dataset['schedule_status'])
            # schedule__interviewer__interviewer_email = dataset['interviewer_email'],
            candidate_name = InterviewProcessDoc.objects(job=job.to_dbref(),
                                                         applicant__email=dataset['candidate'],
                                                         schedule__interviewer__interviewer_email=dataset[
                                                             'interviewer_email'],
                                                         prescreen_status='Accept',
                                                         schedule__interview_type=dataset['interview_type']).first()
            self.mail.interviewer_reschedule_sendmail(
                {'to_email': dataset['interviewer_email'],
                 'cc_email': [dataset['candidate']], 'jobcode': job.code,
                 'candidate': candidate_name.applicant.first_name, 'interviewer_name': dataset['interviewer_name'],
                 'interview_type': dataset['interview_type'], 'schedule_date': dataset['scheduled_datetime'],
                 'schedule_status': dataset['schedule_status']})
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def scheduler_interviewer_status(self, dataset):
        try:
            job = JobDoc.objects(code=dataset['job']).first()
            if dataset['interviewer_acknowledgement'][0] == 'Propose for Reschedule':
                interviewer_acknowledgement = 'Yet to Confirm'
            if dataset['interviewer_acknowledgement'][0] == 'Accepted':
                schedule_status = 'Ready'
            else:
                schedule_status = 'Yet to Confirm'

            comments = str(dataset['comment'][0])
            interviewer_acknowledgement = dataset['interviewer_acknowledgement'][0]

            update_obj = InterviewProcessDoc.objects(job=job.to_dbref(),
                                                     applicant__email=dataset['c_email'][0],
                                                     schedule__interview_type__in=dataset['r_number'],
                                                     prescreen_status='Accept',
                                                     ).update(
                set__schedule__S__interviewer_acknowledge_status=interviewer_acknowledgement,
                set__schedule__S__interviewer_acknowledge_comments=comments,
                set__schedule__S__schedule_status=schedule_status)
            #                                         schedule__interviewer__interviewer_email=dataset['i_email'][0],
            # else:
            #     schedule_obj = InterviewProcessDoc()
            #     schedule_obj.job = job
            #     schedule_obj.applicant. = candidate_obj
            #     schedule_obj.interviewer_acknowledgement = dataset['interviewer_acknowledgement']
            #     schedule_obj.interviewer_comments = dataset['comment'][0]
            #     schedule_obj.save()
            try:
                self.mail.interviewer_status_sendmail(
                    {'to_email': dataset['i_email'][0],
                     'cc_email': [dataset['c_email'][0]], 'jobcode': job.code,
                     'candidate': dataset['c_name'][0], 'interviewer_name': dataset['i_name'][0],
                     'interview_type': dataset['r_number'][0], 'schedule_date': dataset['sch_date'][0],
                     'schedule_status': dataset['interviewer_acknowledgement'][0],
                     })
            except:
                self.logging.error(traceback.format_exc())
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def scheduler_get_all(self):
        data_list = []
        try:
            rec_object = InterviewProcessDoc.objects(prescreen_status='Accept')
            for canobj in rec_object:
                if canobj.job.code == canobj.job.code and canobj.prescreen_status == 'Accept':
                    data_list.append({'job': canobj.job.code,
                                      'candidate': canobj.applicant.first_name + ' ' + canobj.applicant.last_name,
                                      'candidate_email': canobj.applicant.email,
                                      'interviewer_name': canobj.schedule[-1].interviewer.interviewer_name,
                                      'interviewer_email': canobj.schedule[-1].interviewer.interviewer_email,
                                      'interviewer_phone': canobj.schedule[-1].interviewer.interviewer_phone,
                                      'scheduled_datetime': canobj.schedule[-1].scheduled_datetime,
                                      'candidate_acknowledgement': canobj.schedule[-1].candidate_acknowledge_status,
                                      'candidate_comments': canobj.schedule[-1].candidate_acknowledge_comments,
                                      'interview_type': canobj.schedule[-1].interview_type,
                                      'interviewer_acknowledgement': canobj.schedule[-1].interviewer_acknowledge_status,
                                      'interviewer_comments': canobj.schedule[-1].interviewer_acknowledge_comments,
                                      'schedule_status': canobj.schedule[-1].schedule_status,
                                      })
            self.logging.info('Listing out all schedules')
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def scheduler_get_by_candidate(self, job_code, email):
        job = JobDoc.objects(code=job_code).first()
        rescheduler = InterviewProcessDoc.objects(job__in=[job], applicant__email=email).first()
        return rescheduler

    def scheduler_get_roundnumber(self, job_code, email):
        job = JobDoc.objects(code=job_code).first()
        rescheduler = InterviewProcessDoc.objects(job__in=[job], applicant__email=email)
        round = rescheduler.schedule[-1].round_number
        # print(round)
        return round

    def scheduler_shortlisted(self, dataset):
        rec_object = []
        try:
            job = JobDoc.objects(code=dataset['job']).first()
            rec_object = InterviewProcessDoc.objects(job=job.to_dbref(),
                                                     prescreen_status='Accept').to_json()
        except:
            self.logging.error(traceback.format_exc())
        return rec_object

    def scheduler_notscheduled(self):
        data_list = []
        try:
            rec_object = InterviewProcessDoc.objects(schedule__interviewer_acknowledge_status='Yet to Confirm')
            for obj in rec_object:
                data_list.append({'jobcode': obj.job.code,
                                  'candidate_name': obj.applicant.first_name + " " + obj.applicant.last_name,
                                  'candidate_email': obj.applicant.email,
                                  'interviewer_name': obj.schedule[-1].interviewer.interviewer_name,
                                  'interviewer_email': obj.schedule[-1].interviewer.interviewer_email,
                                  'scheduled_datetime': obj.schedule[-1].scheduled_datetime,
                                  'interviewer_acknowledgement': obj.schedule[-1].interviewer_acknowledge_status})
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def pull_reference_data(self, jobcode, candidate_email, interviewer_email, round_number, interview_type):
        job_obj = JobDoc.objects(code=jobcode).first()
        if jobcode and candidate_email and interviewer_email:
            interviewer_obj = InterviewProcessDoc.objects(job=job_obj.to_dbref(),
                                                          applicant__email=candidate_email,
                                                          schedule__interviewer__interviewer_email=interviewer_email,
                                                          schedule__round_number=round_number,
                                                          schedule__interview_type=interview_type).first()
        else:
            interviewer_obj = InterviewProcessDoc.objects(job=job_obj.to_dbref(),
                                                          applicant__email=candidate_email,
                                                          schedule__interviewer_email=interviewer_email,
                                                          schedule__round_number=round_number,
                                                          schedule__interview_type=interview_type).first()
        return interviewer_obj

    def scheduleicon_count(self):
        return InterviewProcessDoc.objects(schedule__interviewer_acknowledge_status='Yet to Confirm').count()

    def get_candidate_name(self, dataset):
        job = JobDoc.objects(code=dataset['job']).first()
        candidate = InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['candidate'],
                                                prescreen_status='Accept')
        return candidate[0].applicant.first_name
