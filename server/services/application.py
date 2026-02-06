from server.models.entities import *
from server.config.applogging import ResponseLoggerMiddleware
# import falcon
# import json
# import cgi
from server.extraction.extract import *
from server.extraction.extract import from_stream, _write_stream
import re
import traceback
from server.services.email import Mail


class Application:
    def __init__(self):
        self.mail = Mail()
        logobj = ResponseLoggerMiddleware()
        self.logging = logobj.set_up_logging()
        self.logging.info('logging started in ' + str(__file__) + str(__class__) + ' class')
        self.interview_process = InterviewProcessDoc()
        self.resume_service = ResumeDoc()
        self.candidate_service = CandidateDoc()
        self.jobObj = JobDoc()
        self.funcObj = FunctionalOrgDoc()

    def save(self, dataset):
        self.candidate_service.first_name = dataset.get('first_name')
        self.candidate_service.middle_name = dataset.get('middle_name')
        self.candidate_service.last_name = dataset.get('last_name')
        self.candidate_service.email = dataset.get('email')
        self.candidate_service.phone = dataset.get('phone')
        self.candidate_service.notice_period = dataset.get('notice_period')
        self.candidate_service.experience = dataset.get('experience')
        self.candidate_service.education = dataset.get('education')
        self.candidate_service.primary_skill = dataset.get('primary_skill')
        self.candidate_service.secondary_skill = dataset.get('secondary_skill')

        try:
            if 'list' not in str(type(dataset['primary_skill'])):
                self.candidate_service.primary_skill = [dataset.get('primary_skill')]
            else:
                self.candidate_service.primary_skill = dataset.get('primary_skill')
        except:
            pass
        try:
            if 'list' not in str(type(dataset.get('secondary_skill'))):
                self.candidate_service.secondary_skill = [dataset.get('secondary_skill')]
            else:
                self.candidate_service.secondary_skill = [dataset.get('secondary_skill')]
        except:
            pass

        docobj = dataset.get('resume')
        (temp_file, output) = _write_stream(docobj, docobj.filename, 'jobprofiles')
        with open(temp_file, 'rb') as fh:
            self.resume_service.resume.put(fh, filename=temp_file, content_type=docobj.headers._headers[1][1])
        try:
            self.resume_service.content = output
            self.resume_service.filename = temp_file
            self.resume_service.content_type = docobj.headers._headers[1][1]
            self.resume_service.save()
        except:
            self.resume_service.delete(filename=self.resume_service.filename)
            self.resume_service.save()
        self.candidate_service.resume = self.resume_service.to_dbref()
        self.interview_process.applicant = self.candidate_service
        job = JobDoc.objects(code=dataset.get('jobcode')).first()
        self.interview_process.job = job.to_dbref()
        try:
            self.interview_process.save()
            funObj = FunctionalOrgDoc.objects(org_email=job.functional_org[0]).first()
            self.mail.resume_upload_sendmail({'to_email': funObj.org_email,
                                              'jobcode': dataset['jobcode'],
                                              'candidate': dataset['first_name'] + ' ' + dataset['last_name'],
                                              'email': dataset['email']})
            return 'success'

        except:
            self.logging.error(traceback.format_exc())
            return 'fail'

    def get_objects(self):
        return InterviewProcessDoc.objects()

    def get_by_job(self, job_code):
        job = JobDoc.objects(code=job_code).first()
        applications = InterviewProcessDoc.objects(job=job.to_dbref())
        return applications

    def get_readyforschedule_by_job(self, job_code):
        job = JobDoc.objects(code=job_code).first()
        applications = InterviewProcessDoc.objects(job=job.to_dbref(), prescreen_status= 'Accept')
        return applications


    def get_by_candidate(self, job_code, phone):
        job = JobDoc.objects(code=job_code).first()
        applications = InterviewProcessDoc.objects(job__in=[job], applicant__phone=phone).first()
        return applications

    def bulk_resume(self, dataset):
        try:
            # print(req.context)
            # jobcode = req.context.model['code']
            # resumeObj = req.context.model['resume']
            # stream = (req.stream.stream if hasattr(req.stream, 'stream') else req.stream)
            # data = {'content' : from_stream(req.stream, resumeObj.filename)}
            # print(resumeObj.keys())
            # print(resumeObj.file.filename)
            temp_file = ''
            output = ''
            if len(dataset['resumes']) >= 2:
                cnt = 0
                for eachdocobj in dataset['resumes']:
                    (temp_file, output) = ('','')
                    (temp_file, output) = _write_stream(eachdocobj, eachdocobj.filename, 'candidateprofiles')
                    resume_required_data = get_required_info(output)
                    try:
                        jobobj = JobDoc.objects(code=dataset['jobcode']).first()
                    except:
                        jobobj = JobDoc.objects(code=dataset['jobcode'])
                    objCandoc = CandidateDoc()
                    name = resume_required_data.get('name')
                    names = name.split(' ')
                    if len(names) > 1:
                        objCandoc.last_name = names[-1]
                        objCandoc.first_name = names[0]
                        if len(names) > 2:
                            objCandoc.middle_name = names[1]
                    else:
                        objCandoc.first_name = name
                    objCandoc.email = resume_required_data.get('email') or None
                    objCandoc.phone = resume_required_data.get('mobile') or None
                    exp = resume_required_data.get('exp')
                    regex = r"\b(?:\d+\.*\+*\d*)\b"
                    matches = re.search(regex, exp)
                    if matches:
                        exp = matches.group()
                    objCandoc.experience = float(exp)

                    objAppdoc = InterviewProcessDoc.objects(job=jobobj.to_dbref(),
                                                                     applicant__email=objCandoc.email)
                    file_contenttype = dataset['resumes'][cnt].headers.get_content_type()

                    if not objAppdoc:
                        resumeObj = ResumeDoc()
                        with open(temp_file, 'rb') as fh:
                            try:
                                resumeObj.resume.put(fh, filename=temp_file,
                                                               contenttype=file_contenttype)
                            except:
                                resumeObj.resume.replace(fh, filename=temp_file,
                                                                   contenttype=file_contenttype)
                        try:
                            resumeObj.content = output
                            resumeObj.filename = temp_file
                            resumeObj.content_type = file_contenttype
                            resumeObj.save()
                        except:
                            resumeObj.delete(filename=temp_file)
                            resumeObj.save()
                        objCandoc.resume = resumeObj.to_dbref()
                        intobj = InterviewProcessDoc()
                        intobj.job = jobobj.to_dbref()
                        intobj.applicant = objCandoc
                        intobj.save()
                        cnt = cnt + 1
                    else:
                        with open(temp_file, 'rb') as fh:
                            print(resumeObj.filename)
                            resumeObj.resume.replace(fh, filename=temp_file,
                                                               contenttype=file_contenttype)
                        try:
                            resumeObj.content = output
                            resumeObj.filename = temp_file
                            resumeObj.content_type = file_contenttype
                            resumeObj.save()
                        except:
                            resumeObj.delete(filename=temp_file)
                            resumeObj.save()
                        objCandoc.resume = resumeObj.to_dbref()
                        updated = InterviewProcessDoc.objects(job=jobobj.to_dbref(),
                                                                       applicant__email=objCandoc.email).update_one(
                            set__applicant=objCandoc)
            else:
                (temp_file, output) = _write_stream(dataset['resumes'], dataset['resumes'], 'candidateprofiles')
                resume_required_data = get_required_info(output)
                print(resume_required_data)
            job = JobDoc.objects(code=dataset['jobcode']).first()
            funObj = FunctionalOrgDoc.objects(org_email=job.functional_org[0]).first()
            self.mail.bulk_upload_sendmail({'to_email': funObj.org_email,
                                            'jobcode': dataset['jobcode'],
                                            'func_org': funObj.functional_org})
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def interview_process_post(self, dataset):
        try:
            # print(req.context)
            # jobcode = req.context.model['code']
            # resumeObj = req.context.model['resume']
            # stream = (req.stream.stream if hasattr(req.stream, 'stream') else req.stream)
            # data = {'content' : from_stream(req.stream, resumeObj.filename)}
            # print(resumeObj.keys())
            # print(resumeObj.file.filename)
            # Read image as binary
            # data = docobj.file.read()
            # Retrieve filename
            (temp_file, output) = _write_stream(dataset['resume'], dataset['resume'].filename, 'candidateprofiles')

            # resume_required_data = get_required_info(output)
            # resume_required_data.update(data)
            self.resume_service.filename = temp_file
            self.resume_service.content_type = dataset['resume'].headers._headers[1][1]
            # print(self.resume_service.filename)

            with open(temp_file, 'rb') as fh:
                print(self.resume_service.filename)
                self.resume_service.resume.replace(fh, filename=temp_file,
                                                   content_type=dataset['resume'].headers._headers[1][1])
            try:
                self.resume_service.content = output
                self.resume_service.filename = temp_file
                self.resume_service.content_type = dataset['resume'].headers._headers[1][1]

                self.resume_service.save()
            except:
                self.resume_service.delete(filename=temp_file)
                self.resume_service.save()
            try:
                jobobj = JobDoc.objects(code=dataset['jobcode']).first()
            except:
                jobobj = JobDoc.objects(code=dataset['jobcode'])
            objCandoc = CandidateDoc()
            objCandoc.first_name = dataset['first_name'] or None
            objCandoc.middle_name = dataset['middle_name'] or None
            objCandoc.last_name = dataset['last_name'] or None
            objCandoc.email = dataset['email'] or None
            objCandoc.phone = dataset['phone'] or None
            objCandoc.notice_period = int(dataset['notice_period'] or 0)
            objCandoc.experience = float(dataset['experience'] or 0)
            objCandoc.education = dataset['education'] or 0
            try:
                if 'list' not in str(type(dataset['primary_skill'])):
                    objCandoc.primary_skill = [dataset['primary_skill']]
                else:
                    objCandoc.primary_skill = dataset['primary_skill'] or []
            except:
                pass
            try:
                if 'list' not in str(type(dataset['secondary_skill'])):
                    objCandoc.secondary_skill = [dataset['secondary_skill']]
                else:
                    objCandoc.secondary_skill = dataset['secondary_skill'] or []
            except:
                pass

            objCandoc.resume = self.resume_service.to_dbref()
            objAppdoc = InterviewProcessDoc.objects(job=jobobj.to_dbref(),
                                                             applicant__phone=objCandoc.phone).first()

            if not objAppdoc:
                objAppdoc = InterviewProcessDoc()
                objAppdoc.job = jobobj.to_dbref()
                objAppdoc.applicant = objCandoc
                objAppdoc.save()
            else:
                objAppdoc = InterviewProcessDoc.objects(job=jobobj.to_dbref(),
                                                                 applicant__phone=objCandoc.phone).get()
                objAppdoc.applicant = objCandoc
                objAppdoc.save()
            funObj = FunctionalOrgDoc.objects(org_email=jobobj.functional_org[0]).first()
            self.mail.resume_upload_sendmail({'to_email': funObj.org_email,
                                              'jobcode': dataset['jobcode'],
                                              'candidate': dataset['first_name'] + ' ' + dataset['last_name'],
                                              'email': dataset['email']})
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def interview_process_update(self, dataset):
        try:
            (temp_file, output) = ('', '')
            if dataset['resume']:
                (temp_file, output) = _write_stream(dataset['resume'], dataset['resume'].filename, 'candidateprofiles')
                self.resume_service.filename = temp_file
                self.resume_service.content = output
                self.resume_service.content_type = dataset['resume'].headers._headers[1][1]

                with open(temp_file, 'rb') as fh:
                    print(self.resume_service.filename)
                    self.resume_service.resume.replace(fh, filename=temp_file,
                                                       content_type=dataset['resume'].headers._headers[1][1])
                try:
                    self.resume_service.save()
                except:
                    self.resume_service.delete(filename=temp_file)
                    self.resume_service.save()
            try:
                jobobj = JobDoc.objects(code=dataset['jobcode']).first()
            except:
                jobobj = JobDoc.objects(code=dataset['jobcode'])

            appObject = InterviewProcessDoc.objects(job=jobobj.to_dbref(),
                                                             applicant__phone=dataset['txn']).get()
            appObject.applicant.first_name = dataset['first_name'] or None
            appObject.applicant.middle_name = dataset['middle_name'] or None
            appObject.applicant.last_name = dataset['last_name'] or None
            appObject.applicant.email = dataset['email'] or None
            appObject.applicant.phone = dataset['phone'] or None
            appObject.applicant.notice_period = int(dataset['notice_period'] or 0)
            appObject.applicant.experience = float(dataset['experience'] or 0)
            appObject.applicant.education = dataset['education']
            try:
                if 'list' not in str(type(dataset['primary_skills'])):
                    appObject.applicant.primary_skill = [dataset['primary_skills']]
                else:
                    appObject.applicant.primary_skill = dataset['primary_skills'] or []
            except:
                pass
            try:
                if 'list' not in str(type(dataset['secondary_skills'])):
                    appObject.applicant.secondary_skill = [dataset['secondary_skills']]
                else:
                    appObject.applicant.secondary_skill = dataset['secondary_skills'] or []
            except:
                pass
            if dataset['resume']:
                appObject.applicant.resume = self.resume_service.to_dbref()
            else:
                try:
                    appObject.applicant.resume = appObject.applicant.resume
                except:
                    pass

            InterviewProcessDoc.objects(job=jobobj.to_dbref(), applicant__phone=dataset['txn']).update_one(
                set__applicant=appObject.applicant)
            funObj = FunctionalOrgDoc.objects(org_email=jobobj.functional_org[0]).first()
            self.mail.resume_edit_sendmail({'to_email': funObj.org_email,
                                              'jobcode': dataset['jobcode'],
                                              'candidate': dataset['first_name'] + ' ' + dataset['last_name'],
                                              'email': dataset['email']})
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def status_edit(self, dataset):
        can_obj = CandidateDoc()
        dataset['status'] = dataset['status'][0]
        (code, phone) = dataset['reference'].split("#")
        job_obj = JobDoc.objects(code=code).first()
        try:
            if dataset['status'].lower() == 'true':
                InterviewProcessDoc.objects(job=job_obj.to_dbref(), applicant__phone=phone).update_one(
                    set__status=True)
            elif dataset['status'].lower() == 'false':
                InterviewProcessDoc.objects(job=job_obj.to_dbref(), applicant__phone=phone).update_one(
                    set__status=False)
            return True
        except:
            self.logging.error(traceback.format_exc())
            return False

    def get_data(self, dataset):
        json_data = []
        candidate_object = InterviewProcessDoc()
        try:
            # rec_object = self.candidate_service.objects(job_status__nin='Closed')
            jobobj = JobDoc.objects(code=dataset['code']).first()
            if dataset['code']:
                candidate_object = InterviewProcessDoc.objects(job=jobobj.to_dbref())
            elif dataset['email']:
                candidate_object = InterviewProcessDoc.objects(applicant__email=dataset['email'])
            elif dataset['phone']:
                candidate_object = InterviewProcessDoc.objects(applicant__phone=dataset['phone'])
            elif dataset['education']:
                candidate_object = InterviewProcessDoc.objects(applicant__education=dataset['education'])
                # for each in [candidate_object]:
                #     json_data.append({'code': each.code, 'resume': each.resume, 'first_name': each.first_name,
                #                       'last_name': each.last_name, 'email': each.email, 'phone': each.phone,
                #                       'notice_period': each.notice_period, 'experience': each.experience,
                #                       'education': each.education, 'primary_skills': each.primary_skills,
                #                       'secondary_skills': each.secondary_skills})
            elif dataset['primary_skill']:
                candidate_object = InterviewProcessDoc.objects(applicant__primary_skill=dataset['primary_skill'])
            elif dataset['location']:
                candidate_object = InterviewProcessDoc.objects(job__location=dataset['location'])
            # data = re.split('[\s*,;+]', dataset)
            # for i in data:
            for each in candidate_object:
                json_data.append({'code': each.job.code,  'resume': 'http://localhost:8000/hroffice/api/applications/candidatepreviewfile?code={}&email={}'.format(each.job.code, each.applicant.email),
                                  'first_name': each.applicant.first_name, 'last_name': each.applicant.last_name,
                                  'email': each.applicant.email, 'phone': each.applicant.phone,
                                  'notice_period': each.applicant.notice_period, 'experience': each.applicant.experience,
                                  'education': each.applicant.education, 'primary_skills': each.applicant.primary_skill,
                                  'secondary_skills': each.applicant.secondary_skill})
        except:
            self.logging.error(traceback.format_exc())
        return json_data

    def pull_reference_data(self, jobcode, applicant):
        jobObj = JobDoc.objects(code=jobcode).first()
        if jobcode and applicant:
            app_obj = InterviewProcessDoc.objects(job=jobObj.to_dbref(), applicant__email=applicant)
        else:
            app_obj = InterviewProcessDoc.objects(job=jobObj.to_dbref(), applicant__email=applicant)
        return app_obj
