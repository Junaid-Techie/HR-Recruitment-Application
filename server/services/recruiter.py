from server.models import entities
import falcon
import json
import logging
from bson import json_util
from pymongo.errors import DuplicateKeyError
# import dateutil.parser
import traceback
# from bson.errors import InvalidId
# from bson.objectid import ObjectId
# import pymongo
# from bson.objectid import ObjectId
# from pymongo import UpdateOne
# from server.extraction.extract import from_stream
# from server.models.entities import *
from server.models.entities import *
from server.config.applogging import ResponseLoggerMiddleware
from server.services.email import Mail


class RecruiterService:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.mail = Mail()
        self.recruiter_modelObj = RecruiterDoc
        self.coutry_modelObj = CountryDoc
        self.state_modelObj = StateDoc
        self.city_modelObj = CityDoc
        self.func_modelObj = FunctionalOrgDoc

    def save(self, recruiter):
        doc = self.recruiter_modelObj(
            emp_id=recruiter.get('emp_id'),
            first_name=recruiter.get('first_name'),
            middle_name=recruiter.get('middle_name'),
            last_name=recruiter.get('last_name'),
            phone=recruiter.get('phone'),
            email=recruiter.get('email'),
            designation=recruiter.get('designation'),
            location=recruiter.get('location'),
            shift_start_time=recruiter.get('start_time'),
            shift_end_time=recruiter.get('end_time'),
            functional_org=recruiter.get('functional_org'))
        doc.save()

    def recruiter_posting(self, dataset):
        try:
            (country, state, city) = dataset['location'].split(' >> ')
            country_obj = self.coutry_modelObj.objects.get(country_name=country)
            state_obj = self.state_modelObj.objects.get(state_name=state)
            city_obj = self.city_modelObj.objects(city_name=city, country=country_obj, state=state_obj).first()
            func_org = self.func_modelObj.objects(org_email=dataset['functional_org']).first()
            if "list" not in str(type(dataset['functional_org'])):
                func_org = [dataset['functional_org']]
            else:
                func_org = dataset['functional_org']

            recruiter = {'emp_id': dataset['emp_id'],
                         'first_name': dataset['first_name'],
                         'middle_name': dataset['middle_name'],
                         'last_name': dataset['last_name'],
                         'phone': dataset['phone'],
                         'email': dataset['email'],
                         'designation': dataset['designation'],
                         'location': city_obj,
                         'start_time': dataset['start_time'],
                         'end_time': dataset['end_time'],
                         'functional_org': func_org
                        }
            self.save(recruiter)
            try:
                self.mail.recruiterprofile_sendmail(
                    {'to_email': dataset['email'], 'emp_id': dataset['emp_id'],
                     'emp_name': dataset['first_name'] + '' + dataset['last_name'],
                     'phone': dataset['phone'], 'email': dataset['email']
                     })
            except:
                self.logging.error(traceback.format_exc())
            try:
                self.mail.recruiterprofile_sendmail(
                    {'to_email': dataset['email'], 'emp_id': dataset['emp_id'],
                     'emp_name': dataset['first_name'] + '' + dataset['last_name'],
                     'phone': dataset['phone'], 'email': dataset['email']
                     })
            except:
                logging.error(traceback.format_exc())
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def recruiter_update(self, dataset):
        try:
            update_obj = RecruiterDoc.objects(emp_id=dataset['txn'])
            (country, state, city) = dataset['location'].split(' >> ')
            country_obj = self.coutry_modelObj.objects.get(country_name=country)
            state_obj = self.state_modelObj.objects.get(state_name=state)
            city_obj = self.city_modelObj.objects(city_name=city, country=country_obj, state=state_obj).first()
            # func_org = self.func_modelObj.objects(org_email=dataset['functional_org'])
            update_obj = self.recruiter_modelObj.objects(emp_id=dataset['emp_id'])
            func_org = dataset['functional_org']
            if "list" not in str(type(func_org)):
                func_org = [func_org]
            else:
                func_org = func_org
            update_obj.update(set__emp_id=dataset['emp_id'],
                              set__middle_name=dataset['middle_name'],
                              set__last_name=dataset['last_name'],
                              set__phone=dataset['phone'],
                              set__email=dataset['email'],
                              set__designation=dataset['designation'],
                              set__location=city_obj,
                              set__functional_org=func_org,
                              )
            self.logging.info(dataset['first_name'] + ' successfully updated')
            try:
                self.mail.recruiterprofile_edit_sendmail(
                    {'to_email': dataset['email'], 'emp_id': dataset['emp_id'],
                     'emp_name': dataset['first_name'] + '' + dataset['last_name'],
                     'phone': dataset['phone'], 'email': dataset['email']})
            except:
                logging.error(traceback.format_exc())
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def recruiter_getall(self):
        try:
            rec_object = self.recruiter_modelObj.objects()
            data_list = []
            for each in rec_object:
                data_list.append({'emp_id': each.emp_id, 'name': each.first_name + ' ' + each.last_name,
                                  'phone': each.phone, 'email': each.email, 'location': each.location.city_name,
                                  'status': each.status})
        except:
            data_list = []
            self.logging.error(traceback.format_exc())
        return data_list

    def status_edit(self, dataset):
        try:
            update_obj = self.recruiter_modelObj.objects(emp_id=dataset['code'])
            if dataset['status'].lower() == 'true':
                update_obj.update(set__status=bool(True))
            elif dataset['status'].lower() == 'false':
                update_obj.update(set__status=bool(False))
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def pull_reference_data(self, recruiter):
        if recruiter:
            rec_obj = self.recruiter_modelObj.objects(email=recruiter)
        else:
            rec_obj = self.recruiter_modelObj.objects(email=recruiter)
        return rec_obj

