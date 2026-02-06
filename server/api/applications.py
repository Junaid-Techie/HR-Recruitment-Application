import falcon
from server.services import application, resume, job, candidate
from server.services.server_validation import Validations
import json
import re
import traceback
from server.config.applogging import ResponseLoggerMiddleware
from server.models import entities
# import cgi
# from server.extraction.extract import *
# from server.extraction.extract import from_stream, _write_stream
import nltk


# nltk.download('words')


class Applications:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.app_service = application.Application()
        self.resume = resume.Resume()
        self.profiles = candidate.Candidate()
        self.job = job.Job()

    def on_get_job(self, req, resp, job):
        resp.status = falcon.HTTP_200
        resp.body = self.app_service.get_by_job('nism_123').to_json()

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        job_id = req.context.model.get('jobId')
        resp.status = falcon.HTTP_200
        resp.body = f'job id is : {job_id}'

    def on_post_job(self, req: falcon.Request, resp: falcon.Response, job):
        resp.status = falcon.HTTP_200
        resp.body = f'with sufix job id is : {job}'

    def on_get(self, req, resp):
        try:
            canobj = self.app_service.get_objects()
            # resp.body = json.dumps(canobj)
            candidate_data = []
            for ipd in canobj:
                # job = self.job.get_data_byref(ipd.applicant.job)
                candidate_data.append({'code': ipd.job._data['code'], 'first_name': ipd.applicant.first_name,
                                       'phone': ipd.applicant.phone,
                                       'email': ipd.applicant.email,
                                       'notice_period': ipd.applicant.notice_period,
                                       'experience': ipd.applicant.experience,
                                       'status': ipd.applicant.status,
                                       'primary_skill': ipd.applicant.primary_skill, })

            resp.body = json.dumps(candidate_data)
        except:
            self.logging.error(traceback.format_exc())
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})

    def on_get_candidatepreviewfile(self, req, resp):
        jobcode = req.get_param('code')
        email = req.get_param('email')
        jobObject = entities.JobDoc.objects(code=jobcode).first()
        objAppdoc = entities.InterviewProcessDoc.objects.filter(job=jobObject.to_dbref(),
                                                                applicant__email=email).first()
        candidateobj = objAppdoc.applicant
        content_type = candidateobj.resume.content_type
        filename = candidateobj.resume.filename
        # candidateobj.resume.read()
        resp.downloadable_as = re.split(r"\\|//", filename)[-1]
        resp.content_type = content_type
        resp.stream = open(filename, 'rb')
        # data = candidateobj.resume.resume.read()
        # resp.set_header("Content-Disposition", "attachment; filename=\"%s\"" % filename)
        # #resp.stream = data
        # resp.write = data
        resp.status = falcon.HTTP_200
    # def on_post(self, req, resp):
    #     self.service.save(None)


class MapApplications:
    def __init__(self):
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.can_service = application.Application()
        self.resume_service = entities.ResumeDoc()
        self.job_service = entities.JobDoc()
        self.profile_service = candidate.Candidate()
        self.can_validation = Validations()

    def on_get(self, req, resp):
        pass

    def on_post_bulkresumeupload(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {
            'jobcode': req.get_param('code'),
            'resumes': req._params['resumes[]']}
        output = self.can_service.bulk_resume(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(
                {'message': 'Bulk resumes successfully uploaded to jobcode ' + dataset['jobcode'],
                 'status': 'success'})
        else:
            resp.body = json.dumps(
                {'message': 'Failed in bulk uploading Candidate resume!!! ',
                 'status': 'failed'})

    def on_post(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {'jobcode': req.get_param('code'),
                   'first_name': req.get_param('first_name'),
                   'middle_name': req.get_param('middle_name'),
                   'last_name': req.get_param('last_name'),
                   'email': req.get_param('email'),
                   'phone': req.get_param('phone'),
                   'notice_period': req.get_param('notice_period'),
                   'experience': float(req.get_param('experience')),
                   'education': req.get_param('education'),
                   'primary_skill': req._params['primary_skill'],
                   'secondary_skill': req._params['secondary_skill'],
                   'resume': req.get_param('resume')}

        exist_data = self.can_validation.candidate_validate(dataset)
        if exist_data:
            resp.status = falcon.HTTP_202
            resp.body = json.dumps(
                {'message': 'Resume of ' + dataset['first_name'] + ' ' + dataset['last_name'] +
                            ' for job code ' + dataset['jobcode'] + ' is already present in the Candidate List.',
                 'status': 'failed'})
        else:
            output = self.can_service.interview_process_post(dataset)
            if output:
                resp.status = falcon.HTTP_201
                resp.body = json.dumps(
                    {'message': ' Resume of ' + dataset['first_name'] + ' ' + dataset['last_name'] +
                                ' successfully uploaded to Job Code ' + dataset['jobcode'],
                     # 'filename': dataset['resume'].filename,
                     'status': 'success'})
            else:
                resp.body = json.dumps({
                    'message': ' Resume of ' + dataset['first_name'] + ' ' + dataset['last_name'] +
                               ' is failed to  upload to the Job Code ' + dataset['jobcode'],
                    'status': 'failed'})
                self.logging.error(traceback.format_exc())

    def on_put_putreq(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        try:
            second_skill = req._params['secondary_skill']
        except:
            second_skill = ''
        dataset = {'jobcode': req.get_param('code'),
                   'txn': req.get_param('txn'),
                   'resume': req.get_param('resumes'),
                   'first_name': req.get_param('first_name'),
                   'middle_name': req.get_param('middle_name'),
                   'last_name': req.get_param('last_name'),
                   'email': req.get_param('email'),
                   'phone': req.get_param('phone'),
                   'notice_period': req.get_param('notice_period'),
                   'experience': req.get_param('experience'),
                   'education': req.get_param('education'),
                   'primary_skills': req.context.model['primary_skill'],
                   'secondary_skills': second_skill}
        output = self.can_service.interview_process_update(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(
                {'message': dataset['first_name'] + ' ' + dataset['last_name']
                            + ' details successfully updated to jobcode ' + dataset['jobcode'],
                 'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed in updating the details of '
                                               + dataset['first_name'] + ' ' + dataset['last_name'],
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_put_edit_status(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {
            'status': req.context.model['status'],
            'reference': req.context.model['txn'][0]
        }
        output = self.can_service.status_edit(dataset)
        if output:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({
                'message': 'Candidate profile successfully ' + 'Enabled!!!' if dataset['status'] == 'true'
                else 'candidate profile successfully ' + 'Disabled!!!',
                'status': 'success'})
        else:
            resp.body = json.dumps({'message': 'Failed to update the status',
                                    'status': 'failed'})
            self.logging.error(traceback.format_exc())

    def on_get_all_search(self, req, resp):
        self.logging.info('request started for Posting in ' + str(__file__))
        resp.status = falcon.HTTP_200
        dataset = {}
        try:
            dataset['code'] = req.get_param('code')
        except:
            dataset['code'] = ''

        dataset = {'code': req.get_param('code'),
                   'email': req.get_param('email'),
                   'phone': req.get_param('phone'),
                   'education': req.get_param('education'),
                   'primary_skill': req.get_param('primary_skill'),
                   'location': req.get_param('location')}
        candidate_data = self.can_service.get_data(dataset)
        if candidate_data is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(candidate_data)
            # resp.body = json.dumps({'message': 'Successful in Fetching Job details!!!'})
        else:
            self.logging.error(traceback.format_exc())
            resp.body = json.dumps({'message': 'Failed in Fetching Job details!!!',
                                    'status': 'failed'})
