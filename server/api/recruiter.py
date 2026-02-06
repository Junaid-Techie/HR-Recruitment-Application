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
from server.services.recruiter import RecruiterService
from server.services.server_validation import Validations
# from server.models.entities import *
# from server.models.entities import RecruiterDoc, CityDoc, CountryDoc, StateDoc
from server.config.applogging import ResponseLoggerMiddleware
from server.services.email import Mail


class Recruiter:
    def __init__(self):
        # super().__init__
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.mail = Mail()
        self.rec_service = RecruiterService()
        self.rec_validation = Validations()

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'emp_id': req.get_param('emp_id'),
                   'first_name': req.get_param('first_name'),
                   'middle_name': req.get_param('middle_name'),
                   'last_name': req.get_param('last_name'),
                   'phone': req.get_param('phone'),
                   'email': req.get_param('email'),
                   'designation': req.get_param('designation'),
                   'location': req.get_param('location'),
                   'start_time': req.get_param('start_time'),
                   'end_time': req.get_param('end_time'),
                   'functional_org': req.params.get('functional_org')}
        exist_data = self.rec_validation.recruiter_validate(dataset)
        if exist_data:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps(
                {'message': dataset['first_name'] + ' ' + dataset['last_name']
                            + ' is already present in the Recruiter Profile.',
                 'status': 'failed'})
        else:
            output = self.rec_service.recruiter_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(
                    {'message': dataset['first_name'] + ' ' + dataset['last_name']
                                + ' has been added to the Recruiter Profile.',
                     'status': 'success'})
            else:
                resp.body = json.dumps(
                    {'message': 'Failed in adding ' + dataset['first_name'] + ' to the Recruiter Profile Master'
                                + traceback.format_exc(),
                     'status': 'failed'})
                logging.error(traceback.format_exc())

    def on_get(self, req, resp):
        # resp.status = falcon.HTTP_200
        # recruiters = []
        # notes_obj = RecruiterDoc.objects(name=req.get_param('name'))
        # for object in notes_obj:
        #     recruiters.append(object)
        pass

    # def on_put_update(self, req, resp):
    #     try:
    #         resp.status = falcon.HTTP_200
    #         update_obj = self.rec_service.recruiter_modelObj.objects(emp_id=req.get_param('txn'))
    #         (country, state, city) = req.get_param('location').split(' >> ')
    #         countryObj = self.rec_service.coutry_modelObj.objects.get(country_name=country)
    #         stateObj = self.rec_service.state_modelObj.objects.get(state_name=state)
    #         cityObj = self.rec_service.city_modelObj.objects(city_name=city, country=countryObj,
    #                                                          state=stateObj).first()
    #         update_obj.update(set__emp_id=req.get_param('emp_id'), set__first_name=req.get_param('first_name'),
    #                           set__middle_name=req.get_param('middle_name'),
    #                           set__last_name=req.get_param('last_name'),
    #                           set__phone=req.get_param('phone'),
    #                           set__email=req.get_param('email'),
    #                           set__designation=req.get_param('designation'),
    #                           set__location=cityObj)
    #         self.logging.info(req.get_param('first_name') + ' successfully updated!!!')
    #     except:
    #         resp.body = json.dumps({'message': 'Failed to update the details of ' + str(req.get_param('name'))})
    #         self.logging.error(traceback.format_exc())

    def on_put_putreq(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'emp_id': req.get_param('emp_id'),
                   'first_name': req.get_param('first_name'),
                   'middle_name': req.get_param('middle_name'),
                   'last_name': req.get_param('last_name'),
                   'phone': req.get_param('phone'),
                   'email': req.get_param('email'),
                   'designation': req.get_param('designation'),
                   'location': req.get_param('location'),
                   'start_time': req.get_param('start_time'),
                   'end_time': req.get_param('end_time'),
                   'txn': req.get_param('txn'),
                   'functional_org': req.params.get("functional_org"),
                   'name': req.get_param('name')}
        output = self.rec_service.recruiter_update(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': 'Successfully update the details of  ' + str(dataset['txn']),
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the details of ' + str(dataset['txn']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_delete_trash_collection(self, req, resp, data):
        self.logging.info(req.get_param('first_name') + ' successfully updated')
        resp.status = falcon.HTTP_200
        try:
            collect_obj = self.rec_service.recruiter_modelObj.objects(emp_id=data)
            if collect_obj.delete():
                resp.body = json.dumps({'message': data + ' successfully deleted',
                                        'status': 'success'})
                self.logging.info(data + ' successfully deleted')
        except:
            resp.body = json.dumps({'message': 'error occurred on deletion',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'status': req.context.model['status'],
                   'code': req.context.model['code']}
        output = self.rec_service.status_edit(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': 'candidate profile successfully ' + 'Enabled!!!'
            if dataset['status'] == 'true' else 'candidate profile successfully ' + 'Disabled!!!',
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the Status for ' + str(dataset['code']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

        # try:
        #     resp.status = falcon.HTTP_200
        #     code = req.get_param("emp_id")
        #     status = req.get_param("status")
        #     updateObj = RecruiterDoc.objects(emp_id=code)
        #     if status.lower() == 'true':
        #         updateObj.update(set__status=bool(True))
        #     elif status.lower() == 'false':
        #         updateObj.update(set__status=bool(False))
        #     resp.body = json.dumps({
        #         'message': code + ' recruiter successfully ' + 'Enabled!!!' if status == 'true' else code +
        #         ' recruiter successfully ' + 'Disabled!!!'})
        # except:
        #     resp.body = json.dumps({'message': 'Failed to update the Status for ' + str(req.get_param('code'))})
        #     self.logging.error(traceback.format_exc())


class RecruiterAPI:
    def __init__(self):
        # super.__init__
        self.recruiter_service = RecruiterService()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')

    def on_get(self, req, resp):
        pass

    def on_get_byname(self, req, resp, name):
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.recruiter_service.recruiter_modelObj.objects(first_name=name)
            data_list = []
            for x in rec_object:
                data_list.append({'emp_id': x.emp_id,
                                  'first_name': x.first_name,
                                  'middle_name': x.middle_name,
                                  'last_name': x.last_name,
                                  'phone': x.phone,
                                  'email': x.email,
                                  'designation': x.designation})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching ' + name + ' details!!!',
                                    'status': 'failed'})

    def on_get_list(self, req, resp, data):
        self.logging.info('request started for GET in ' + str(__class__))
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.recruiter_service.recruiter_modelObj.objects(emp_id=data)
            data_list = []
            for x in rec_object:
                data_list.append({'empid': x.emp_id, 'first_name': x.first_name, 'phone': x.phone, 'email': x.email,
                                  'designation': x.designation})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching ' + data + ' details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_all(self, req, resp):
        self.logging.info('request started for GET in ' + str(__class__))
        resp.status = falcon.HTTP_200
        recruiter_data = self.recruiter_service.recruiter_getall()
        if recruiter_data is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(recruiter_data)
            self.logging.info('Listing out all recruiters')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching recruiters details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_delete_remove(self, req, resp, recid):
        resp.status = falcon.HTTP_200
        try:
            collect_obj = self.recruiter_service.recruiter_modelObj.objects(emp_id=recid)
            if collect_obj.delete():
                resp.body = json.dumps({'message': recid + ' successfully deleted', 'status': 'success'})
        except:
            resp.body = json.dumps({'message': 'error occurred on deletion',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
