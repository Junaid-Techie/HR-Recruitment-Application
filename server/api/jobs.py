import falcon
import json
# from server.extraction.extract import from_stream, _write_stream
from server.services.job import Job
from server.services.server_validation import Validations
from server.models.entities import *
# from bson.objectid import ObjectId
from server.config.applogging import ResponseLoggerMiddleware
import traceback
# import pathlib
# import jinja2
from falcon_jinja2 import FalconTemplate
# import server.config as cfg
from server.models.entities import JobDoc
from server.services.email import Mail
import re

# from server.config.config import get_html_template_path
# template_path =  get_html_template_path()
# STATIC_PATH = pathlib.Path(__file__).parent / 'static'
# print(str(STATIC_PATH))
template_path = "D:\src\hiring-office\server\\ui"
falcon_template = FalconTemplate(path=template_path)


class Jobs:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.coutry_modelObj = CountryDoc
        self.state_modelObj = StateDoc
        self.city_modelObj = CityDoc
        self.mail = Mail()
        self.job_service = Job()
        self.job_validation = Validations()

    def on_get(self, req, resp):
        pass

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        (country, state, city) = req.get_param('location').split(' >> ')
        dataset = {'country': country,
                   'state': state,
                   'city': city,
                   'jd': req.get_param('jd'),
                   'functional_org': req.params.get("functional_org"),
                   'required_skills': req.params.get('required_skills'),
                   'interview_pattern': req.params.get('interview_pattern'),
                   'code': req.get_param('code'),
                   'title': req.get_param('title'),
                   'desc': req.get_param('desc'),
                   'positions': req.get_param('positions'),
                   'minexp': req.get_param('minexp'),
                   'maxexp': req.get_param('maxexp'),
                   'edu': req.get_param('edu'),
                   'client': req.get_param('client'),
                   'hr_name': req.get_param('hr_name'),
                   'hr_email': req.get_param('hr_email'),
                   'hr_phone': req.get_param('hr_phone'),
                   'end_date': req.get_param('end_date'),
                   'emp_type': req.get_param('emp_type')}
        exist_data = self.job_validation.job_validate(dataset)
        if exist_data:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps({'message': dataset['code'] + ' is already present in the Job Profile.',
                                    'status': 'failed'})
        else:
            output = self.job_service.job_posting(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps({
                    'message': str(dataset['code']) + ' has ben added to the Job Profile.',
                    'status': 'success'})
            else:
                self.logging.error(traceback.format_exc())
                resp.body = json.dumps({'message': 'Failed to add ' + str(dataset['code'] + ' to the Job Profile.'),
                                        'status': 'failed'})

    def on_delete(self, req, resp):
        pass

    def on_delete_collection(self, req, resp, code):
        from falcon_cors import CORS
        try:
            resp.status = falcon.HTTP_200
            collectObj = JobDoc.objects(code=code)
            if collectObj.delete():
                resp.body = json.dumps({'message': code + ' successfully deleted!',
                                        'status': 'success'})
        except:
            resp.body = json.dumps({'message': 'Failed deleting the collection ' + str(req.get_param('code')),
                                    'status': 'failed'})

    def on_put_update(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        (country, state, city) = req.get_param('location').split(' >> ')
        dataset = {'country': country,
                   'state': state,
                   'city': city,
                   'jd': req.get_param('jd'),
                   'functional_org': req.params.get("functional_org"),
                   'required_skills': req.params.get('required_skills'),
                   'interview_pattern': req.params.get('interview_pattern'),
                   'code': req.get_param('code'),
                   'title': req.get_param('title'),
                   'desc': req.get_param('desc'),
                   'positions': req.get_param('positions'),
                   'minexp': req.get_param('minexp'),
                   'maxexp': req.get_param('maxexp'),
                   'edu': req.get_param('edu'),
                   'client': req.get_param('client'),
                   'hr_name': req.get_param('hr_name'),
                   'hr_email': req.get_param('hr_email'),
                   'hr_phone': req.get_param('hr_phone'),
                   'end_date': req.get_param('end_date'),
                   'emp_type': req.get_param('emp_type')}
        output = self.job_service.job_update(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': str(dataset['code']) + ' is updated.',
                'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update ' + str(dataset['code']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_updatestatus(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'code': req.get_param("code"), 'job_status': req.get_param("job_status")}
        output = self.job_service.update_status(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': dataset['code'] + ' job code status successfully updated.',
                'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the Status for ' + str(dataset['code']),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())


class JobSearch:
    def __init__(self):
        self.service = Job()
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')

    def on_get_id(self, req, resp, id):
        self.logging.info('request started for GET in ' + str(__class__) + 'for ' + id)

        try:
            resp.status = falcon.HTTP_200
            jobObject = self.service.get_data_byid(id)
            data_list = []
            for x in jobObject:
                data_list.append({'code': x.code, 'title': x.title, 'location': x.location})
            resp.body = json.dumps(data_list)

        except:
            resp.body = json.dumps({'message': 'Failed to get collection on id ' + str(req.get_param('code')),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_title(self, req, resp, title):
        try:
            resp.status = falcon.HTTP_200
            jobObject = self.service.get_data_bytitle(title)
            data_list = []
            for x in jobObject:
                data_list.append({'code': x.code, 'title': x.title, 'location': x.location})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed to get collection on title ' + str(req.get_param('title')),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_company(self, req, resp, company):
        try:
            resp.status = falcon.HTTP_200
            jobObject = self.service.get_data_bycompany(company)
            data_list = []
            for x in jobObject:
                data_list.append({'code': x.code, 'title': x.title, 'location': x.location, 'company': x.company})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed to get collection on company ' + str(req.get_param('company')),
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_titlecompany(self, req, resp):
        try:
            resp.status = falcon.HTTP_200
            title = req.get_param('title')
            company = req.get_param('company')
            jobObject = self.service.get_data_by_title_company(title, company)
            data_list = []
            for x in jobObject:
                data_list.append({'code': x.code, 'title': x.title, 'location': x.location, 'company': x.company})
            resp.body = json.dumps(data_list)
        except:
            resp.body = json.dumps({'message': 'Failed to get collection on title and company ',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_all(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        job_data = self.service.get_data()
        if job_data is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(job_data)
            # resp.body = json.dumps({'message': 'Successful in Fetching Job details!!!'})
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_jobpreviewfile(self, req, resp):
        jobcode = req.get_param('code')
        jobObject = JobDoc.objects(code=jobcode).first()
        content_type = jobObject.jd.contentType
        filename = jobObject.jd.filename
        # jobObject.jd.read()
        d_filename = re.split(r"\\|//", filename)[-1]
        resp.downloadable_as = d_filename
        resp.content_type = content_type
        resp.stream = open(filename, 'rb')
        # resp.set_header("Content-Disposition", "attachment; filename=\"%s\"" % filename)
        # resp.stream =str(jobObject.jd.read()).encode()
        resp.status = falcon.HTTP_200
        # resp.downloadable_as = None
        # assert resp.downloadable_as == 'attachment; filename='+filename

    def on_get_notclosed(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'api_cnt': req.get_param('api_cnt')}
        output = self.service.notclosed()
        if output:
            try:
                if req.get_param('api_cnt'):
                    resp.body = len(output)
                    return resp.body
            except:
                pass
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(output)
            self.logging.info('Listing out all jobs')
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})

    def on_get_all_skillsearch(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        data = req.get_param('required_skills')
        job_data = self.service.get_data_skillsearch(data)
        if job_data is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(job_data)
            # resp.body = json.dumps({'message': 'Successful in Fetching Job details!!!'})
        else:
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())
