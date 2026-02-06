from server.models import entities
import falcon
import json
from server.extraction.extract import from_stream
from server.models.entities import *
from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback


class FunctionalOrg:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.funcorg_modelobj = FunctionalOrgDoc

    def save(self, org):
        doc = self.funcorg_modelobj(
            functional_org=org.get('functional_org'),
            org_email=org.get('org_email'),
            cc_email=org.get('cc_email'),
        )
        doc.save()

    def functional_org_posting(self, dataset):
        try:
            edu = {'functional_org': dataset['org_name'],
                   'org_email': dataset['org_email'],
                   'cc_email': dataset['cc_email']}
            self.save(edu)
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def functional_org_update(self, dataset):
        try:
            updateObj = self.funcorg_modelobj.objects(functional_org=dataset['txn'])
            updateObj.update(set__functional_org=dataset['org_name'],
                             set__org_email=dataset['org_email'],
                             set__cc_email=dataset['cc_email'])
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def status_update(self, dataset):
        try:
            updateObj = self.funcorg_modelobj.objects(functional_org=dataset['functional_org'])
            if dataset['status'].lower() == 'true':
                updateObj.update(set__status=bool(True))
            elif dataset['status'].lower() == 'false':
                updateObj.update(set__status=bool(False))
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def get_data(self):
        try:
            rec_object = self.funcorg_modelobj.objects()
            json_data = rec_object.to_json()
        except:
            json_data = []
            self.logging.error(traceback.format_exc())
        return json_data

    def get_objects(self):
        return self.funcorg_modelobj.objects()

    def pull_reference_data(self, func_org):
        if func_org:
            func_obj = self.funcorg_modelobj.objects(org_email=func_org)
        else:
            func_obj = self.funcorg_modelobj.objects(org_email=func_org)
        return func_obj
