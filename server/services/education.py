from server.models import entities
import logging
import traceback
from server.config.applogging import ResponseLoggerMiddleware


class EducationService:
    def __init__(self):
        self.edu_modelObj = entities.EducationDoc
        log_obj = ResponseLoggerMiddleware()
        self.logging = log_obj.set_up_logging()

    def save(self, edu):
        doc = entities.EducationDoc(qualification=edu.get('qualification'),
                                    specialisation=edu.get('specialisation'),
                                    university=edu.get('university'),
                                    qualification_description=edu.get('qualification_description'))
        doc.save()

    def on_posting(self, dataset):
        try:
            edu = {'qualification': dataset['qualification'],
                   'specialisation': dataset['specialisation'],
                   'university': dataset['university'],
                   'qualification_description': dataset['qualification_description']}

            self.save(edu)
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def get_records(self):
        return self.edu_modelObj.objects()

    def pull_reference_data(self, qualification, specialisation):
        if qualification and specialisation:
            obj = self.edu_modelObj.objects(qualification=qualification, specialisation=specialisation)
        else:
            obj = self.edu_modelObj.objects(qualification=qualification)
        return obj

    def update_status(self, qualification, specialisation, status):
        updateObj = self.pull_reference_data(qualification, specialisation)
        try:
            if status.lower() == 'true':
                updateObj.update(set__status=bool(True))
                return True
            elif status.lower() == 'false':
                updateObj.update(set__status=bool(False))
                return True
        except:
            return False

    def update_reference_data(self, data):
        try:
            updateObj = self.pull_reference_data(data.get('qualification'), data.get('specialisation'))
            updateObj.update(set__qualification=data.get('qualification'),
                             set__specialisation=data.get('specialisation'),
                             set__qualification_description=data.get('desc'),
                             set__university=data.get('university'))
            return True
        except:
            self.logging.error(traceback.format_exc())
            print(traceback.format_exc())
            return False
