import falcon
import json
# from server.extraction.extract import from_stream
from server.services.education import EducationService as eduService
from server.services.server_validation import Validations
# from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback
import logging
# import pathlib
# import jinja2
from falcon_jinja2 import FalconTemplate

# import server.config as cfg
# from server.models.entities import EducationDoc
template_path = "D:\src\hiring-office\server\\ui"
falcon_template = FalconTemplate(path=template_path)


class Education:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.edu_service = eduService()
        self.edu_validation = Validations()

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        try:
            self.logging.info('request started for Posting in ' + str(__file__))
            dataset = {'qualification': req.get_param('qualification'),
                       'specialisation': req.get_param('specialisation'),
                       'university': req.get_param('university'),
                       'qualification_description': req.get_param('qualification_description')}
            exist_edu = self.edu_validation.education_validate(dataset)
            if exist_edu:
                resp.status = falcon.HTTP_202
                resp.body = json.dumps({
                    'message': "'" + dataset['qualification'] + "'  is already present in the Education Master.",
                    'status': 'failed'})
            else:
                output = self.edu_service.on_posting(dataset)
                if output:
                    resp.status = falcon.HTTP_201
                    resp.body = json.dumps({
                        'message': "'" + dataset['qualification'] + "' has been added to the Education Master.",
                        'status': 'success'})
                else:
                    resp.body = json.dumps(
                        {'message': "Failed in adding '" + dataset['qualification']
                                    + "' to the Education Master." + traceback.format_exc(),
                         'status': 'failed'})
                    logging.error(traceback.format_exc())
        except:
            logging.error(traceback.format_exc())

    def on_get_all(self, req, resp):
        resp.status = falcon.HTTP_200
        try:
            rec_object = self.edu_service.get_records()
            json_data = rec_object.to_json()
            resp.body = json_data
        except:
            resp.body = json.dumps({'message': 'Failed in Fetching Education Qualification details!!!',
                                    'status': 'fail'})

    def on_put_updatestatus(self, req, resp):
        resp.status = falcon.HTTP_200
        qualification = req.get_param("qualification")
        specialisation = req.context.model["specialisation"][0]
        status = req.get_param("status")
        try:
            # print(qualification, specialisation)
            r_status = self.edu_service.update_status(qualification, specialisation, status)
            resp.body = json.dumps({
                'message': qualification + ' qualification successfully ' + 'Enabled!!!'
                if status == 'true' and r_status == True else qualification + ' qualification successfully ' + 'Disabled!!!',
                'status': 'success'})
        except:
            resp.body = json.dumps({'message': 'Failed to update the Status for ' + str(qualification),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_eduputreq(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            # qualification = req.get_param("txn")
            qualification = req.context.model["txn"]
            (qualification, speciality) = qualification.split("#")
            edu = {'qualification': req.get_param('qualification'),
                   'specialisation': req.get_param('specialisation'),
                   'university': req.get_param('university'),
                   'desc': req.get_param('qualification_description')}
            status = self.edu_service.update_reference_data(edu)
            if status:
                resp.body = json.dumps({
                    'message': "'" + qualification + '(' + speciality + ')' + "' qualification successfully updated!!!",
                    'status': 'success'})
            else:
                resp.body = json.dumps(
                    {'message': 'Failed to update the Status for ' + str(edu['qualification']),
                     'status': 'failed'})

        except:
            self.logging.error(traceback.format_exc())
            resp.body = json.dumps(
                {'message': 'Failed to update the Status for ' + str(req.get_param('qualification')),
                 'status': 'failed'})
