from server.services.country import CountryService
from server.services.state import StateService
from server.services.city import CityService
from server.services.education import EducationService
from server.services.skill import SkillService
from server.services.functionalorg import FunctionalOrg
from server.services.job import Job
from server.services.recruiter import RecruiterService
from server.services.application import Application
from server.services.scheduler import Scheduler
from server.services.feedback import Feed
from server.config.applogging import ResponseLoggerMiddleware
import logging
import traceback


class Validations:

    def __init__(self):
        log_obj = ResponseLoggerMiddleware()
        self.logging = log_obj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.country_service = CountryService()
        self.state_service = StateService()
        self.city_service = CityService()
        self.edu_service = EducationService()
        self.skill_service = SkillService()
        self.func_service = FunctionalOrg()
        self.job_service = Job()
        self.recruiter_service = RecruiterService()
        self.applicant_service = Application()
        self.interviewer_service = Scheduler()
        self.feedback_service = Feed()

    def education_validate(self, dataset):
        try:
            validate_data = self.edu_service.pull_reference_data(dataset['qualification'],
                                                                 dataset['specialisation']).first()
            try:
                exist_edu = validate_data.qualification
            except:
                return False
            return dataset['qualification'] == exist_edu
        except:
            logging.error(traceback.format_exc())
            return False

    def skill_validate(self, dataset):
        try:
            validate_data = self.skill_service.pull_reference_data(dataset['skill_name']).first()
            try:
                exist_skill = validate_data.skill_name
            except:
                return False
            return dataset['skill_name'] == exist_skill
        except:
            logging.error(traceback.format_exc())
            return False

    def func_org_validate(self, dataset):
        try:
            validate_data = self.func_service.pull_reference_data(dataset['org_email']).first()
            try:
                exist_func_org = validate_data.org_email
            except:
                return False
            return dataset['org_email'] == exist_func_org
        except:
            logging.error(traceback.format_exc())
            return False

    def country_validate(self, dataset):
        try:
            validate_data = self.country_service.pull_reference_data(dataset['country_name']).first()
            try:
                exist_country = validate_data.country_name
            except:
                return False
            return dataset['country_name'] == exist_country
        except:
            logging.error(traceback.format_exc())
            return False

    def state_validate(self, dataset):
        try:
            validate_data = self.state_service.pull_reference_data(dataset['country_name'],
                                                                   dataset['state_name']).first()
            try:
                exist_state = validate_data.state_name
            except:
                return False
            return dataset['state_name'] == exist_state
        except:
            logging.error(traceback.format_exc())
            return False

    def city_validate(self, dataset):
        try:
            validate_data = self.city_service.pull_reference_data(dataset['country_name'], dataset['state_name'],
                                                                  dataset['city_name']).first()
            try:
                exist_city = validate_data.city_name
            except:
                return False
            return dataset['city_name'] == exist_city
        except:
            logging.error(traceback.format_exc())
            return False

    def job_validate(self, dataset):
        try:
            validate_data = self.job_service.pull_reference_data(dataset['code']).first()
            try:
                exist_job = validate_data.code
            except:
                return False
            return dataset['code'] == exist_job
        except:
            logging.error(traceback.format_exc())
            return False

    def recruiter_validate(self, dataset):
        try:
            validate_data = self.recruiter_service.pull_reference_data(dataset['email']).first()
            try:
                exist_recruiter = validate_data.email
            except:
                return False
            return dataset['email'] == exist_recruiter
        except:
            logging.error(traceback.format_exc())
            return False

    def interviewer_validate(self, dataset):
        try:
            validate_data = self.interviewer_service.pull_reference_data(dataset['job'],
                                                                         dataset['candidate'],
                                                                         dataset['interviewer_email'],
                                                                         int(dataset['round_number']),
                                                                         dataset['interview_type'])
            try:
                exist_interviewer = validate_data.schedule[0].interviewer.interviewer_email
            except:
                return False
            return dataset['interviewer_email'] == exist_interviewer
        except:
            logging.error(traceback.format_exc())
            return False

    def candidate_validate(self, dataset):
        try:
            validate_data = self.applicant_service.pull_reference_data(dataset['jobcode'], dataset['email']).first()
            try:
                exist_applicant = validate_data.applicant.email
            except:
                return False
            return dataset['email'] == exist_applicant
        except:
            logging.error(traceback.format_exc())
            return False

    def feedback_validate_round_selection(self, dataset):
        try:
            validate_data = self.feedback_service.pull_reference_data(dataset['job'],
                                                                      dataset['candidate'],
                                                                      dataset['interview_type'])
            try:
                exist_interviewer = validate_data.schedule[0].interview_type
            except:
                return False
            return dataset['next_round'] == exist_interviewer
        except:
            logging.error(traceback.format_exc())
            return False

    def feedback_validate_round_repeat(self, dataset):
        try:
            validate_data = self.feedback_service.pull_reference_data(dataset['job'],
                                                                      dataset['candidate'],
                                                                      dataset['interview_type'])
            try:
                exist_interviewer = validate_data.schedule[0].next_round
            except:
                return False
            return dataset['next_round'] == exist_interviewer
        except:
            logging.error(traceback.format_exc())
            return False
