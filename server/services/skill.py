# from server.models import entities
# import falcon
# import json
# from server.extraction.extract import from_stream
from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback


class SkillService:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.skill_modelObj = SkillDoc

    def save(self, skill):
        doc = self.skill_modelObj(skill_name=skill.get('skill_name'),
                                  skill_desc=skill.get('skill_desc'))
        doc.save()

    def skill_posting(self, dataset):
        try:
            self.logging.info('request started for Posting in ' + str(__file__))
            skill = {'skill_name': dataset['skill_name'],
                     'skill_desc': dataset['skill_desc']}
            self.save(skill)
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def skill_update(self, dataset):
        try:
            update_obj = self.skill_modelObj.objects(skill_name=dataset['txn'])
            update_obj.update(set__skill_desc=dataset['skill_desc'], set__skill_name=dataset['skill_name'])
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def status_update(self, dataset):
        try:
            update_obj = self.skill_modelObj.objects(skill_name=dataset['skill_name'])
            if dataset['status'].lower() == 'true':
                update_obj.update(set__status=bool(True))
            elif dataset['status'].lower() == 'false':
                update_obj.update(set__status=bool(False))
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def get_data(self):
        try:
            rec_object = self.skill_modelObj.objects()
            json_data = rec_object.to_json()
        except:
            json_data = []
            self.logging.error(traceback.format_exc())
        return json_data

    def get_records(self):
        return self.skill_modelObj.objects()

    def pull_reference_data(self, skill):
        if skill:
            obj = self.skill_modelObj.objects(skill_name=skill)
        else:
            obj = self.skill_modelObj.objects(skill_name=skill)
        return obj
