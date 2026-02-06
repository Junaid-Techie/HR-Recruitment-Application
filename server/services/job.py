from server.models.entities import *
from server.config.applogging import ResponseLoggerMiddleware
import falcon
import json
# import cgi
from server.extraction.extract import *
from server.extraction.extract import from_stream, _write_stream
import re
import traceback
from server.services.email import Mail

import re


class Job:
    def __init__(self):
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.job_modelobj = JobDoc
        self.coutry_modelObj = CountryDoc
        self.state_modelObj = StateDoc
        self.city_modelObj = CityDoc

    def save(self, job):
        # doc = entities.JobDoc(
        #     code=job.get('code'),
        #     title=job.get('title'),
        #     location=job.get('location'),
        #     desc=job.get('desc'),
        #     expectation=job.get('expectation'),
        #     edu_desc=job.get('edu_desc'),
        #     edu=job.get('edu'),
        #     company=job.get('company'),
        #     job_status = job.get('job_status') or 'Open',
        #     interview_pattern=[job.get('interview_pattern')]
        # )
        doc = self.job_modelobj(job)
        doc.save()

    def job_posting(self, dataset):
        try:
            docobj = dataset['jd']
            (temp_file, output) = _write_stream(docobj, docobj.filename, 'jobprofiles')
            jobobj = self.job_modelobj()
            func_org = dataset['functional_org']
            if "list" not in str(type(func_org)):
                func_org = [func_org]
            else:
                func_org = func_org
            with open(temp_file, 'rb') as fh:
                jobobj.jd.put(fh, filename=temp_file, content_type=docobj.headers._headers[1][1])
            interview_pattern = []
            skills = dataset['required_skills']
            if "list" not in str(type(skills)):
                skills = [skills]
            else:
                skills = skills
            interview_pattern = dataset['interview_pattern']
            if "list" not in str(type(interview_pattern)):
                interview_pattern = [interview_pattern]
            else:
                interview_pattern = interview_pattern
            jobobj.code = dataset['code']
            jobobj.title = dataset['title']

            cityObj = self.city_modelObj.objects(city_name=dataset['city'],
                                                 country=self.coutry_modelObj.objects.get(
                                                     country_name=dataset['country']),
                                                 state=self.state_modelObj.objects.get(
                                                     state_name=dataset['state'])).first()
            jobobj.location = cityObj
            jobobj.desc = dataset['desc']
            jobobj.functional_org = func_org
            jobobj.positions = dataset['positions']
            jobobj.experience = str(dataset['minexp']) + "-" + str(dataset['maxexp'])
            jobobj.edu = dataset['edu']
            jobobj.interview_pattern = interview_pattern
            jobobj.client = dataset['client']
            jobobj.required_skills = skills
            # jobobj.jd_filename = docobj.filename
            # jobobj.jd_content_type =docobj.content_type
            jobobj.hr_name = dataset['hr_name']
            jobobj.hr_email = dataset['hr_email']
            jobobj.hr_phone = dataset['hr_phone']
            jobobj.end_date = dataset['end_date']
            jobobj.emp_type = dataset['emp_type']
            jobobj.save()
            funObj = FunctionalOrgDoc.objects(org_email=func_org[0]).first()

            try:
                self.mail.jobprofile_sendmail(
                    {'to_email': funObj.org_email,
                     'cc_email': [funObj.cc_email, dataset['hr_email']],
                     'jobcode': dataset['code'], 'jobtitle': dataset['title'], 'func_org': funObj.functional_org})
            except:
                self.logging.error(traceback.format_exc())
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def job_update(self, dataset):

        try:

            cityObj = CityDoc.objects(city_name=dataset['city'],
                                      country=CountryDoc.objects.get(country_name=dataset['country']),
                                      state=StateDoc.objects.get(state_name=dataset['state'])).first()
            updateObj = self.job_modelobj.objects(code=dataset['code'])
            docobj = dataset['jd']
            temp_file = ''
            jobobj = JobDoc()
            func_org = dataset["functional_org"]
            if "list" not in str(type(func_org)):
                func_org = [func_org]
            else:
                func_org = func_org
            interview_pattern = []
            skills = dataset['required_skills']
            if "list" not in str(type(skills)):
                skills = [skills]
            else:
                skills = skills
            interview_pattern = dataset['interview_pattern']
            if "list" not in str(type(interview_pattern)):
                interview_pattern = [interview_pattern]
            else:
                interview_pattern = interview_pattern
            # if docobj is not None or docobj != '':
            #     (temp_file, output) = from_stream(docobj, docobj.filename)
            #     jobobj = JobDoc(code=req.get_param('code'))
            #     with open(temp_file, 'rb') as fh:
            #         jobobj.jd.replace(fh, filename=temp_file, content_type=docobj.headers._headers[1][1])
            # #         jobobj.code = req.get_param('code')
            # #         jobobj.desc = req.get_param('desc')
            # #         jobobj.title = req.get_param('title')
            #         jobobj.save()
            updateObj.update(set__location=cityObj,
                             set__desc=str(dataset['desc']),
                             set__functional_org=func_org,
                             set__positions=int(dataset['positions']),
                             set__experience=str(dataset['minexp']) + "-" + str(dataset['maxexp']),
                             set__interview_pattern=interview_pattern,
                             set__edu=str(dataset['edu']),
                             set__client=str(dataset['client']),
                             set__required_skills=skills,
                             set__hr_name=dataset['hr_name'],
                             set__hr_email=dataset['hr_email'],
                             set__hr_phone=dataset['hr_phone'],
                             set__end_date=dataset['end_date'],
                             set__emp_type = dataset['emp_type'],
                        )
            funObj = FunctionalOrgDoc.objects(org_email=func_org[0]).first()
            try:
                self.mail.jobprofile_edit_sendmail(
                    {'to_email': funObj.org_email,
                     'cc_email': [funObj.cc_email, dataset['hr_email']],
                     'jobcode': dataset['code'], 'jobtitle': dataset['title'], 'func_org': funObj.functional_org})
            except:
                self.logging.error(traceback.format_exc())
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def update_status(self, dataset):
        try:
            update_obj = self.job_modelobj.objects(code=dataset["code"])
            update_obj.update(set__job_status=dataset['job_status'])
            if update_obj:
                update_obj.update(set__job_status=dataset['job_status'])
            else:
                job_obj = JobDoc()
                job_obj.job_status = dataset['job_status'][0]
                job_obj.save()
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    # input_file = req.get_param('file')

    # if input_file.filename:
    #     ext = input_file.filename.split('.')[1]
    #     data = from_stream(input_file.file, ext)
    #     resp.status = falcon.HTTP_200
    #     resp.body = data

    def get_data(self):
        try:
            rec_object = self.job_modelobj.objects()
            json_data = []
            for each in rec_object:
                json_data.append(
                    {'code': each.code, 'title': each.title, 'desc': each.desc, 'positions': each.positions,
                     'experience': each.experience, 'edu': each.edu, 'interview_pattern': each.interview_pattern,
                     'client': each.client, 'job_status': each.job_status, 'jd': each.jd.filename,
                     'location': each.location.city_name, 'status': each.status, 'hr_name': each.hr_name,
                     'hr_email': each.hr_email, 'hr_phone': each.hr_phone,
                     'end_date': each.end_date.strftime("%m/%d/%Y")})
        except:
            json_data = []
            self.logging.error(traceback.format_exc())
        return json_data

    def notclosed(self):
        try:
            rec_object = self.job_modelobj.objects(job_status__nin=['Closed'])
            data_list = []
            for obj in rec_object:
                if obj.job_status != "Closed":
                    data_list.append({'code': obj.code, 'title': obj.title, 'location': obj.location.city_name,
                                      'desc': obj.desc, 'positions': obj.positions, 'experience': obj.experience,
                                      'edu': obj.edu, 'interview_pattern': obj.interview_pattern,
                                      'job_status': obj.job_status, 'client': obj.client, 'status': obj.status,
                                      'hr_name': obj.hr_name, 'hr_email': obj.hr_email, 'hr_phone': obj.hr_phone,
                                      'end_date': obj.end_date.strftime("%m/%d/%Y")})
        except:
            data_list = []
            self.logging.error(traceback.format_exc())
        return data_list

    def get_data_skillsearch(self, data):
        json_data = []
        try:
            rec_object = self.job_modelobj.objects(job_status__nin='Closed')
            data = re.split('[\s*,;+]', data)
            for i in data:
                for each in rec_object(required_skills=i):
                    if len(json_data) > 0:
                        if json_data[0]['code'] == each.code:
                            continue
                    json_data.append(
                        {'code': each.code, 'title': each.title, 'desc': each.desc, 'positions': each.positions,
                         'experience': each.experience, 'edu': each.edu, 'interview_pattern': each.interview_pattern,
                         'client': each.client, 'job_status': each.job_status, 'jd': each.jd.filename,
                         'location': each.location.city_name, 'status': each.status, 'hr_name': each.hr_name,
                         'hr_email': each.hr_email, 'hr_phone': each.hr_phone,
                         'end_date': each.end_date.strftime("%m/%d/%Y")})
        except:
            self.logging.error(traceback.format_exc())
        return json_data

    def get_data_byid(self, id):
        return self.job_modelobj.objects(code=id)

    def get_data_byref(self, id):
        return self.job_modelobj.objects(pk=id)

    def get_data_bytitle(self, title):
        return self.job_modelobj.objects(title=title)

    def get_data_by_id_title(self, id, title):
        return self.job_modelobj.objects(code=id, title=title)

    def get_data_bycompany(self, company):
        return self.job_modelobj.objects(client=company)

    def get_data_by_title_company(self, title, company):
        return self.job_modelobj.objects(title=title, client=company)

    def get_objects(self):
        return self.job_modelobj.objects()

    def pull_reference_data(self, job):
        if job:
            job_obj = self.job_modelobj.objects(code=job)
        else:
            job_obj = self.job_modelobj.objects(code=job)
        return job_obj

    def get_jobicon_count(self):
        return  JobDoc.objects(job_status__ne='Closed').count()

