import falcon
import json
# from server.extraction.extract import from_stream
from server.services.skill import SkillService
from server.services.server_validation import Validations
# from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback
# import pathlib
# import jinja2
from falcon_jinja2 import FalconTemplate

# import server.config as cfg
template_path = "D:\src\hiring-office\server\\ui"
falcon_template = FalconTemplate(path=template_path)


class Skills:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.skill_service = SkillService()
        self.skill_validation = Validations()

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'skill_name': req.get_param('skill_name'),
                   'skill_desc': req.get_param('skill_desc')}
        exist_data = self.skill_validation.skill_validate(dataset)
        if exist_data:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({
                'message': "'" + dataset['skill_name'] + "' is already present in the Technical Skill Master.",
                'status': 'failed'})
        else:
            output = self.skill_service.skill_posting(dataset)
            if output:
                resp.body = json.dumps({
                    'message': "'" + dataset['skill_name'] + "' has been added to the Technical Skill Master.",
                    'status': 'success'})
            else:
                self.logging.error(traceback.format_exc())
                resp.body = json.dumps({
                    'message': "Failed in adding '" + dataset['skill_name'] + "' to the Technical Skill Master.",
                    'status': 'failed'})

    def on_put_update(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'skill_name': req.get_param('skill_name'),
                   'skill_desc': req.get_param('skill_desc'), 'txn': req.get_param('txn')}
        output = self.skill_service.skill_update(dataset)
        if output:
            resp.body = json.dumps({'message': "Successfully updated '" + dataset['skill_name'] + "'.",
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the collection ' + str(dataset['skill_name']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'skill_name': req.context.model['skill_name'][0],
                   'status': req.get_param('status')}
        output = self.skill_service.status_update(dataset)
        if output:
            resp.body = json.dumps({
                'message': dataset['skill_name'] + ' successfully ' + 'Enabled!!!'
                if dataset['status'] == 'true' else dataset['skill_name'] + '  successfully ' + 'Disabled!!!',
                'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the Status for ' + str(dataset['skill_name']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    # def on_get_all(self, req, resp):
    #     resp.status = falcon.HTTP_200
    #     try:
    #         rec_object = SkillDoc.objects()
    #         json_data = rec_object.to_json()
    #         resp.body = json_data
    #     except:
    #         resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!'})

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        output = self.skill_service.get_data()
        if output is not None:
            resp.body = output
            # resp.body = json.dumps({'message': 'Successful in Fetching Job details!!!'})

        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})
