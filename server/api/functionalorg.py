import falcon
import json
# from server.extraction.extract import from_stream
from server.services.functionalorg import FunctionalOrg as orgService
from server.services.server_validation import Validations
# from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback
# import pathlib
# import jinja2
from falcon_jinja2 import FalconTemplate
# import server.config as cfg
# from server.models.entities import EducationDoc
template_path = "D:\src\hiring-office\server\\ui"
falcon_template = FalconTemplate(path=template_path)


class FunctionalOrg:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.func_org_service = orgService()
        self.func_org_validation = Validations()

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'org_name': req.get_param('org_name'),
                   'org_email': req.get_param('orgemail'),
                   'cc_email': req.get_param('ccemail')}
        exist_data = self.func_org_validation.func_org_validate(dataset)
        if exist_data:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({
                'message': dataset['org_name'] + ' is already present in the Functional Org Profile.',
                'status': 'failed'})
        else:
            output = self.func_org_service.functional_org_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({
                    'message': str(dataset['org_name']) + ' has been added to the Functional Org Profile.',
                    'status': 'success'})
            else:
                self.logging.error(traceback.format_exc())
                resp.body = json.dumps({
                    'message': 'Failed in adding ' + str(dataset['org_name'] + ' to the Functional Org Profile.'),
                    'status': 'failed'})

    def on_put_orgputreq(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'org_name': req.get_param('org_name'),
                   'org_email': req.get_param('orgemail'),
                   'cc_email': req.get_param('ccemail'),
                   'txn': req.get_param("txn")}
        output = self.func_org_service.functional_org_update(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': dataset['txn']+' successfully updated',
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the details for ' + str(dataset['org_name']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'functional_org': req.context.model['org_name'][0],
                   'status': req.get_param("status")}
        output = self.func_org_service.status_update(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'message': dataset['functional_org']+' successfully ' + 'Enabled!!!'
            if dataset['status'] == 'true' else dataset['functional_org']+' successfully '+'Disabled!!!',
                                    'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the status for ' + dataset['functional_org'],
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    # def on_get_all(self, req, resp):
    #     resp.status = falcon.HTTP_200
    #     try:
    #         rec_object = FunctionalOrgDoc.objects()
    #         json_data = rec_object.to_json()
    #         print(json_data)
    #         resp.body = json_data
    #     except:
    #         resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!'})

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        output = self.func_org_service.get_data()
        if output is not None:
            resp.status = falcon.HTTP_201
            resp.body = output
            # resp.body = json.dumps({'message': 'Successful in Fetching functional org details!!!'})
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching functional org details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
