# from server.models.entities import *
# import falcon
# import json
import logging
from server.extraction.extract import from_stream
from server.models.entities import *
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


class Offer:
    def __init__(self):
        # self.service = Offerservice()
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')

    def save(self, feed):
        doc = OfferDoc(feed)
        doc.save()

    def offer_posting(self, dataset):
        try:
            job = JobDoc.objects(code=dataset['job']).first()
            candidate_obj = InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['applicant'],
                                                        schedule__next_round='Offer').first()
            offerobj = OfferDoc()
            docobj = dataset['offer_attachment']
            (temp_file, output) = from_stream(docobj, docobj.filename)
            with open(temp_file, 'rb') as fh:
                offerobj.offer_attachment.put(fh, filename=temp_file, content_type=docobj.headers._headers[1][1])
            offerobj.job = job
            offerobj.applicant = candidate_obj.applicant
            offerobj.comments = dataset['comments']
            offerobj.join_date = dataset['join_date']
            offerobj.save()
            self.mail.offer_sendmail({'to_email': dataset['applicant'],
                                      'cc_email': [job.functional_org[0], job.hr_email],
                                      'jobcode': job.code,
                                      'candidate': candidate_obj.applicant.first_name,
                                      'join_date': dataset['join_date'],
                                      'filename': temp_file})
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def get_data(self):
        data_list = []
        try:
            offer_object = OfferDoc.objects()
            for canobj in offer_object:
                data_list.append({'job': canobj.job.code,
                                  'applicant': canobj.applicant.first_name + ' ' + canobj.applicant.last_name,
                                  'join_date': canobj.join_date,
                                  'comments': canobj.comments})
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def accepted_offer(self, dataset):
        try:
            jobobj = JobDoc.objects(code=dataset['job']).first()
            offer_object = InterviewProcessDoc.objects(job=jobobj.to_dbref(), schedule__next_round="Offer")
            data_list = []
            for eachoffer in offer_object:
                data_list.append(
                    {'first_name': str(eachoffer.applicant.first_name), 'last_name': str(eachoffer.applicant.last_name),
                     'email': str(eachoffer.applicant.email)})
        except:
            self.logging.error(traceback.format_exc())
        return data_list

    def get_candidate_name(self, dataset):
        job = JobDoc.objects(code=dataset['job']).first()
        candidate = InterviewProcessDoc.objects(job=job.to_dbref(), applicant__email=dataset['applicant'],
                                                schedule__next_round='Offer')
        return candidate[0].applicant.first_name
