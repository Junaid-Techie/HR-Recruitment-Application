import falcon
# import json
from server.config import settings
# import jinja2
from falcon_jinja2 import FalconTemplate
from server.services import education, country, state, city, skill, functionalorg, recruiter, job, application, \
    scheduler, prescreening
from server.config.config import get_html_template_path, get_appurl, get_apptitle, get_staticurl, get_select_options
import re


class ServePages:
    template_path = FalconTemplate(path=get_html_template_path())

    def __init__(self):
        self.staticurl = get_staticurl()
        self.appurl = get_appurl()
        self.apptitle = get_apptitle()
        self.interview_type = settings.interview_type
        self.interview_channel = settings.interview_channel
        self.next_round = settings.next_round
        self.eduObj = education.EducationService()
        self.countryObj = country.CountryService()
        self.stateObj = state.StateService()
        self.cityObj = city.CityService()
        self.skillObj = skill.SkillService()
        self.funcorgObj = functionalorg.FunctionalOrg()
        self.jobObj = job.Job()
        self.applicantObj = application.Application()
        self.scheduleObj = scheduler.Scheduler()
        self.prescreningObj = prescreening.PreScreening()
        self.employeetype = settings.employement_type

    @template_path.render('index.html')
    def on_get_home(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'

        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages']}

    # Education actions start here
    @template_path.render('education_list.html')
    def on_get_educationprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'EducationProfile.js', 'validate_js': 'EducationProfile_validate.js'}

    @template_path.render('education_add.html')
    def on_get_addeducation(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'educationprofile_url': 'educationprofile',
                        'jsfile': 'EducationProfile.js', 'validate_js': 'EducationProfile_validate.js'}

    @template_path.render('education_edit.html')
    def on_post_editeducation(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        qualify = req.context.model["txn"][0]
        (qualify, speciality) = qualify.split("#")
        # qualify.replace('+', ' ')
        SelectEduObj = self.eduObj.pull_reference_data(qualify, speciality).first()
        resp.context = {'static_url': self.staticurl,
                        'qualification': SelectEduObj.qualification,
                        'university': SelectEduObj.university,
                        'specialisation': SelectEduObj.specialisation,
                        'qualification_description': SelectEduObj.qualification_description,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'educationprofile_url': 'educationprofile',
                        'txn': req.context.model["txn"][0],
                        'jsfile': 'EducationProfile.js', 'validate_js': 'EducationProfile_validate.js'}

    # Education Services end here

    # Country Starts here
    @template_path.render('country_list.html')
    def on_get_countryprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'country_url': 'countryprofile',
                        'jsfile': 'CountryProfile.js', 'validate_js': 'CountryProfile_validate.js'}

    @template_path.render('country_add.html')
    def on_get_addcountry(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'country_url': 'countryprofile',
                        'jsfile': 'CountryProfile.js', 'validate_js': 'CountryProfile_validate.js'}

    @template_path.render('country_edit.html')
    def on_post_editcountry(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.context.model['txn'][0]
        skillobj = self.countryObj.pull_reference_data(operation).first()
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'country_code': skillobj.country_code,
                        'country_name': skillobj.country_name,
                        'desc': skillobj.desc,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'country_url': 'countryprofile',
                        'jsfile': 'CountryProfile.js', 'validate_js': 'CountryProfile_validate.js'}

    @template_path.render('state_list.html')
    def on_get_stateprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'StateProfile.js', 'validate_js': 'StateProfile_validate.js',
                        'state_url': 'stateprofile'}

    @template_path.render('state_add.html')
    def on_get_addstate(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        countryobj = country.CountryService()
        countryobj = countryobj.get_records()
        resp.context = {'countryobj': countryobj, 'static_url': self.staticurl, 'url': self.appurl,
                        'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'state_url': 'stateprofile',
                        'jsfile': 'StateProfile.js', 'validate_js': 'StateProfile_validate.js'}

    @template_path.render('state_edit.html')
    def on_post_editstate(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        qualify = req.context.model["txn"][0]
        countryObj = self.countryObj.get_records()
        (c_country, s_state) = qualify.split("#")
        skillobj = self.stateObj.pull_reference_data(c_country, s_state).first()

        country_options = get_select_options(countryObj, 'country_name', 'country_name',
                                             [skillobj.country.country_name])
        # print(country_options)
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'country': country_options,
                        'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'state_name': skillobj.state_name, 'state_desc': skillobj.state_desc,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'], 'state_url': 'stateprofile',
                        'jsfile': 'StateProfile.js', 'validate_js': 'StateProfile_validate.js', 'txn': qualify}

    # state end

    # city start
    @template_path.render('city_list.html')
    def on_get_cityprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'city_url': 'cityprofile',
                        'jsfile': 'CityProfile.js', 'validate_js': 'CityProfile_validate.js'}

    @template_path.render('city_add.html')
    def on_get_addcity(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        countryobj = self.countryObj.get_records()
        stateobj = self.stateObj.get_records()
        resp.context = {'countryobj': countryobj, 'stateobj': stateobj, 'static_url': self.staticurl,
                        'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'schedule_url': 'listinterviewer',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'city_url': 'cityprofile',
                        'jsfile': 'CityProfile.js', 'validate_js': 'CityProfile_validate.js'}

    @template_path.render('city_edit.html')
    def on_post_editcity(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.context.model['txn'][0]
        (country, state, city) = operation.split('#')
        # print(country, state, city)
        skillobj = self.cityObj.pull_reference_data(country, state, city).first()
        Country = self.countryObj.get_records()
        State = self.stateObj.get_records()
        country_options = get_select_options(Country, 'country_name', 'country_name', [skillobj.country.country_name])
        state_options = get_select_options(State, 'state_name', 'state_name', [skillobj.state.state_name])
        # print(country_options)
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'country': country_options, 'state': state_options, 'schedule_url': 'listinterviewer',
                        'city_desc': skillobj.city_desc, 'city_name': skillobj.city_name, 'address': skillobj.address,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'city_url': 'cityprofile',
                        'jsfile': 'CityProfile.js', 'validate_js': 'CityProfile_validate.js', 'txn': operation}

    # skills start
    @template_path.render('skillprofile_list.html')
    def on_get_skillsprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'skillprofile_url': 'skillprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'SkillProfile.js', 'validate_js': 'SkillProfile_validate.js'}

    @template_path.render('skillprofile_add.html')
    def on_get_addskill(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'skillprofile_url': 'skillprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'SkillProfile.js', 'validate_js': 'SkillProfile_validate.js'}

    @template_path.render('skillprofile_edit.html')
    def on_post_editskill(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.context.model['txn'][0]
        skillobj = self.skillObj.skill_modelObj.objects(skill_name=operation).first()
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'skill_name': skillobj.skill_name, 'skill_desc': skillobj.skill_desc,
                        'skillprofile_url': 'skillprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'SkillProfile.js', 'validate_js': 'SkillProfile_validate.js'}

    # functional Org
    @template_path.render('functionalorg_list.html')
    def on_get_orgprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        # print(settings.ui_pages['service_pages'],"\n", settings.ui_pages['master_pages'])
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'orgprofile_url': 'funcorgprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'FunctionalOrg.js', 'validate_js': 'FunctionalOrg_validate.js'}

    @template_path.render('functionalorg_add.html')
    def on_get_addorg(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'FunctionalOrg.js', 'validate_js': 'FunctionalOrg_validate.js',
                        'orgprofile_url': 'funcorgprofile',
                        }

    @template_path.render('functionalorg_edit.html')
    def on_post_editorg(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        qualify = req.get_param("txn")
        # qualify.replace('+', ' ')
        SelectEduObj = self.funcorgObj.funcorg_modelobj.objects(functional_org=req.context.model['txn'][0]).first()
        resp.context = {'static_url': self.staticurl, 'orgname': SelectEduObj.functional_org,
                        'orgemail': SelectEduObj.org_email, 'ccemail': SelectEduObj.cc_email,
                        'url': self.appurl, 'apptitle': self.apptitle, 'orgprofile_url': 'funcorgprofile',
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'FunctionalOrg.js', 'validate_js': 'FunctionalOrg_validate.js'}

    # recruiters
    @template_path.render('recruiter_list.html')
    def on_get_recruiter(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'recruiter_url': 'recruiter',
                        'resumeupload_url': 'applications/candidateprofile',
                        'jsfile': 'RecruiterProfile.js', 'validate_js': 'RecruiterProfile_validate.js'}

    @template_path.render('recruiter_add.html')
    def on_get_addrecruiter(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        cities_list = []
        for each in self.cityObj.city_modelObj.objects():
            cities_list.append(
                {'c_s_c': each.country.country_name + ' >> ' + each.state.state_name + ' >> ' + each.city_name})
        city_options = get_select_options(cities_list, 'c_s_c', 'c_s_c', [])
        SelectFuncObj = self.funcorgObj.get_objects()
        funcorg_options = get_select_options(SelectFuncObj, 'org_email', 'functional_org', [])
        # print(city_options)
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'work_location': city_options, 'functional_org': funcorg_options,
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'home_url': 'home', 'recruiter_url': 'recruiter',
                        'jsfile': 'RecruiterProfile.js', 'validate_js': 'RecruiterProfile_validate.js'}

    @template_path.render('recruiter_edit.html')
    def on_post_editrecruiter(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        recobj = recruiter.RecruiterService()
        recobj = recobj.recruiter_modelObj.objects(emp_id=req.get_param('txn')).first()
        FuncObj = self.funcorgObj.get_objects()
        cities_list = []
        cityObj = recobj.location
        for each in self.cityObj.city_modelObj.objects():
            cities_list.append(
                {'c_s_c': each.country.country_name + ' >> ' + each.state.state_name + ' >> ' + each.city_name})
        city_options = get_select_options(cities_list, 'c_s_c', 'c_s_c',
                                          [
                                              cityObj.country.country_name + ' >> ' + cityObj.state.state_name + ' >> ' + cityObj.city_name])
        # print(city_options)
        try:
            functional_org = get_select_options(FuncObj, 'org_email', 'functional_org', recobj.functional_org)
        except:
            functional_org = get_select_options(FuncObj, 'org_email', 'functional_org', [])
        resp.context = {'recobj': recobj,
                        'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'recruiter_url': 'recruiter', 'functional_org': functional_org,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'RecruiterProfile.js', 'validate_js': 'RecruiterProfile_validate.js',
                        'work_location': city_options}

    # job profile
    @template_path.render('jobprofile_list.html')
    def on_get_jobprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'job_code': req.get_param('job_code'),
                        'jobprofile_url': 'jobprofile', 'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'jobProfile.js', 'validate_js': 'Jobprofile_validate.js'}

    @template_path.render('jobprofile_add.html')
    def on_get_addjobprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        cities_list = []
        for each in self.cityObj.get_records():
            cities_list.append(
                {'c_s_c': each.country.country_name + ' >> ' + each.state.state_name + ' >> ' + each.city_name})
        city_options = get_select_options(cities_list, 'c_s_c', 'c_s_c', [])
        SelectEduObj = self.eduObj.get_records()
        options = get_select_options(SelectEduObj, 'qualification', 'qualification', [])
        SkillallObj = self.skillObj.get_records()
        # print(SkillallObj)
        positions = []
        for itm in range(101):
            if itm <= 0:
                continue
            positions.append({'ky': itm, 'vl': itm})
        positions_options = get_select_options(positions, 'ky', 'vl', [])
        min_exp = []
        max_exp = []
        for itm in range(20):
            if itm <= 0:
                continue
            min_exp.append({'ky': itm, 'vl': itm})
            max_exp.append({'ky': itm, 'vl': itm})
        minexp_options = get_select_options(min_exp, 'ky', 'vl', [])
        maxexp_options = get_select_options(max_exp, 'ky', 'vl', [])
        SelectFuncObj = self.funcorgObj.get_objects()
        funcorg_options = get_select_options(SelectFuncObj, 'org_email', 'functional_org', [])
        primary_options = get_select_options(SkillallObj, 'skill_name', 'skill_name', [])
        interview_channel = self.interview_channel
        channel_options = []
        for itm in interview_channel:
            value = interview_channel[itm]
            channel_options.append({'ky': itm, 'vl': value})
        interview_channel_options = get_select_options(channel_options, 'ky', 'vl', [])
        emp_option = self.employeetype
        emp_options = []
        for itm in emp_option:
            value = emp_option[itm]
            emp_options.append({'ky': itm, 'vl': value})
        employement_options = get_select_options(emp_options, 'ky', 'vl', [])
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'education_options': options, 'functional_org': funcorg_options,
                        'skill_options': primary_options, 'work_location': city_options,
                        'positions_options': positions_options, 'interview_channel_options': interview_channel_options,
                        'minexp_options': minexp_options, 'maxexp_options': maxexp_options,
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'jobprofile_url': 'jobprofile', 'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'jobProfile.js', 'validate_js': 'Jobprofile_validate.js',
                        'employement_options': employement_options}

    @template_path.render('jobprofile_update.html')
    def on_post_editjobprofile(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.get_param('txn')
        jobobj = self.jobObj.get_data_byid(operation).first()
        EducationallObj = self.eduObj.get_records()
        FuncObj = self.funcorgObj.get_objects()
        SkillObj = self.skillObj.get_records()
        cities_list = []
        cityObj = jobobj.location
        for each in self.cityObj.get_records():
            cities_list.append(
                {'c_s_c': each.country.country_name + ' >> ' + each.state.state_name + ' >> ' + each.city_name})
        city_options = get_select_options(cities_list, 'c_s_c', 'c_s_c',
                                          [
                                              cityObj.country.country_name + ' >> ' + cityObj.state.state_name + ' >> ' + cityObj.city_name])
        # print(city_options)
        try:
            edu_options = get_select_options(EducationallObj, 'qualification', 'qualification', [jobobj.edu])
        except:
            edu_options = get_select_options(EducationallObj, 'qualification', 'qualification', [])
        try:
            skill_options = get_select_options(SkillObj, 'skill_name', 'skill_name', jobobj.required_skills)
        except:
            skill_options = get_select_options(SkillObj, 'skill_name', 'skill_name', [])
        try:
            functional_orgs = get_select_options(FuncObj, 'org_email', 'functional_org', jobobj.functional_org)
        except:
            functional_orgs = get_select_options(FuncObj, 'org_email', 'functional_org', [])
        positions = []
        for itm in range(101):
            if itm <= 0:
                continue
            positions.append({'ky': itm, 'vl': itm})
        positions = []
        for itm in range(101):
            if itm <= 0:
                continue
            positions.append({'ky': itm, 'vl': itm})
        try:
            positions_options = get_select_options(positions, 'ky', 'vl', [str(jobobj.positions)])
        except:
            positions_options = get_select_options(positions, 'ky', 'vl', [])
        min_exp = []
        max_exp = []
        for itm in range(20):
            if itm <= 0:
                continue
            min_exp.append({'ky': itm, 'vl': itm})
            max_exp.append({'ky': itm, 'vl': itm})
        try:
            (minexp, maxexp) = jobobj.experience.split('-')
        except:
            (minexp, maxexp) = ('', '')
        try:
            minexp_options = get_select_options(min_exp, 'ky', 'vl', [str(minexp)])
        except:
            minexp_options = get_select_options(min_exp, 'ky', 'vl', [])
        try:
            maxexp_options = get_select_options(max_exp, 'ky', 'vl', [str(maxexp)])
        except:
            maxexp_options = get_select_options(max_exp, 'ky', 'vl', [])

        interview_channel = self.interview_channel
        channel_options = []
        for itm in interview_channel:
            value = interview_channel[itm]
            channel_options.append({'ky': itm, 'vl': value})
        try:
            interview_channel_options = get_select_options(channel_options, 'ky', 'vl', jobobj.interview_pattern)
        except:
            interview_channel_options = get_select_options(channel_options, 'ky', 'vl', [])

        #
        # interview_data = [{'name': 'Video Call', 'value': 'Video Call'}, {'name': 'Telephone', 'value': 'Telephone'},
        #                   {'name': 'Face to Face', 'value': 'Face to Face'}, {'name': 'HR', 'value': 'HR'}]
        # try:
        #     interview_options = get_select_options(interview_data, 'name', 'value', jobobj.interview_pattern)
        # except:
        #     interview_options = get_select_options(interview_data, 'name', 'value', [])
        jd = ''
        try:
            jd = jobobj.jd.filename
        except:
            jd = ''

        emp_option = self.employeetype
        emp_options = []
        for itm in emp_option:
            value = emp_option[itm]
            emp_options.append({'ky': itm, 'vl': value})
        employement_options = get_select_options(emp_options, 'ky', 'vl', jobobj.emp_type)

        resp.context = {'jobdetail': jobobj, 'jd': jd, 'static_url': self.staticurl, 'url': self.appurl,
                        'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'positions_options': positions_options,
                        'education_options': edu_options, 'minexp_options': minexp_options,
                        'maxexp_options': maxexp_options, 'interview_options': interview_channel_options,
                        'required_skills_options': skill_options,
                        'functional_orgs': functional_orgs,
                        'work_location': city_options,
                        'jobprofile_url': 'jobprofile', 'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'jobProfile.js', 'validate_js': 'Jobprofile_validate.js',
                        'emp_type': employement_options}

    @template_path.render('jobicon_list.html')
    def on_get_jobicon(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'job_code': req.get_param('job_code'),
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'jobicon.js', 'validate_js': 'jobprofile_validate.js'}

    @template_path.render('prescreenicon_list.html')
    def on_get_prescreenicon(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'prescreenicon.js', 'validate_js': 'Prescreening_validate.js'}

    @template_path.render('notschedule_list.html')
    def on_get_notscheduled(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'notschedule.js', 'validate_js': 'Scheduler_validate.js'}

    @template_path.render('login.html')
    def on_get_login(self, req, resp):
        resp.status = falcon.HTTP_200
        session = req.env['beaker.session']
        session.save()
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle, }

    @template_path.render('candidates_list.html')
    def on_get_listcandidate(self, req, resp):
        resp.status = falcon.HTTP_200
        # print('coming inside')
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'resumeupload_url': 'applications/candidateprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'UploadResume.js', 'validate_js': 'ResumeUpload_validate.js'}

    @template_path.render('upload_resume.html')
    def on_get_uploadresume(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        jobobj = self.jobObj.get_objects()
        SkilallObj = self.skillObj.get_records()
        EducationallObj = self.eduObj.get_records()
        edu_options = get_select_options(EducationallObj, 'qualification', 'qualification', [])
        primary_options = get_select_options(SkilallObj, 'skill_name', 'skill_name', [])
        secondary_options = get_select_options(SkilallObj, 'skill_name', 'skill_name', [])
        noticeperiod = []
        for itm in range(366):
            noticeperiod.append({'ky': itm, 'vl': itm})
        noticeperiod_options = get_select_options(noticeperiod, 'ky', 'vl', [])
        experiance = []
        for itm in range(26):
            experiance.append({'ky': itm, 'vl': itm})
        experiance_options = get_select_options(experiance, 'ky', 'vl', [])
        resp.context = {'jobcodes': jobobj, 'static_url': self.staticurl, 'education': edu_options, 'url': self.appurl,
                        'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(), 'experience': experiance_options,
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'primary': primary_options, 'secondary': secondary_options,
                        'resumeupload_url': 'applications/candidateprofile',
                        'notice_period': noticeperiod_options,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'UploadResume.js', 'validate_js': 'ResumeUpload_validate.js'}

    @template_path.render('bulkresume_upload.html')
    def on_get_bulkresumeupload(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        jobobj = self.jobObj.get_objects()
        resp.context = {'jobcodes': jobobj, 'static_url': self.staticurl,
                        'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'resumeupload_url': 'applications/candidateprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'BulkUpload.js', 'validate_js': 'BulkUpload_validate.js'}

    @template_path.render('candidate_edit.html')
    def on_post_editcandidate(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        qualify = req.context.model["txn"][0]
        (jobcode, phone) = qualify.split("#")
        joballobj = self.jobObj.get_objects()
        candidateObj = self.applicantObj.get_by_candidate(jobcode, phone)
        SkilallObj = self.skillObj.get_records()
        EducationallObj = self.eduObj.get_records()
        job_options = get_select_options(joballobj, 'code', 'code', [jobcode])
        edu_options = get_select_options(EducationallObj, 'qualification', 'qualification',
                                         [candidateObj.applicant.education])
        primary_options = get_select_options(SkilallObj, 'skill_name', 'skill_name',
                                             candidateObj.applicant.primary_skill)
        secondary_options = get_select_options(SkilallObj, 'skill_name', 'skill_name',
                                               candidateObj.applicant.secondary_skill)
        noticeperiod = []
        for itm in range(366):
            noticeperiod.append({'ky': itm, 'vl': itm})
        noticeperiod_options = get_select_options(noticeperiod, 'ky', 'vl', [str(candidateObj.applicant.notice_period)])
        experience = []
        for itm in range(20):
            experience.append({'ky': float(itm), 'vl': float(itm)})
        experience_options = get_select_options(experience, 'ky', 'vl', [str(candidateObj.applicant.experience)])
        resp.context = {'static_url': self.staticurl, 'experience': experience_options, 'education': edu_options,
                        'url': self.appurl, 'apptitle': self.apptitle, 'jobcodes': job_options, 'data': candidateObj,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'primary': primary_options, 'secondary': secondary_options,
                        'jobprofile_url': 'jobprofile', 'home_url': 'home', 'recruiter_url': 'recruiter',
                        'notice_period': noticeperiod_options,
                        'profile_name': re.split(r"\\|//", candidateObj.applicant.resume.filename)[-1],
                        'resumeupload_url': 'applications/candidateprofile',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'UploadResume.js', 'validate_js': 'ResumeUpload_validate.js'}

    @template_path.render('prescreening_list.html')
    def on_get_prescreening(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'Prescreening.js', 'validate_js': 'Prescreening_validate.js',
                        'prescreen_url': 'listprescreening'}

    @template_path.render('prescreening_add.html')
    def on_get_addprescreening(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        countryobj = self.countryObj.get_records()
        stateobj = self.stateObj.get_records()
        resp.context = {'countryobj': countryobj, 'stateobj': stateobj, 'static_url': self.staticurl,
                        'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'Prescreening.js', 'validate_js': 'Prescreening_validate.js',
                        'prescreen_url': 'listprescreening'}

    @template_path.render('prescreening_edit.html')
    def on_post_editprescreening(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.context.model['txn'][0]
        (country, state, city) = operation.split('#')
        skillobj = self.cityObj.pull_reference_data(country, state, city).first()
        Country = self.countryObj.get_records()
        State = self.stateObj.get_records()
        country_options = get_select_options(Country, 'country_name', 'country_name', [skillobj.country.country_name])
        state_options = get_select_options(State, 'state_name', 'state_name', [skillobj.state.state_name])
        print(country_options)
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'country': country_options, 'state': state_options,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'city_desc': skillobj.city_desc, 'city_name': skillobj.city_name, 'address': skillobj.address,
                        'prescreen_url': 'listprescreening',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'Prescreening.js', 'validate_js': 'Prescreening_validate.js'}

    # Assign Interviewer
    @template_path.render('assigning_interviewer_list.html')
    def on_get_interviewer(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'Assigning_interviewer.js', 'validate_js': 'Scheduler_validate.js',
                        'schedule_url': 'listinterviewer'}

    @template_path.render('assigning_interviewer_add.html')
    def on_get_addinterviewer(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        countryobj = self.countryObj.get_records()
        stateobj = self.stateObj.get_records()
        JobObj = self.jobObj.get_objects()
        job_options = get_select_options(JobObj, 'code', 'code', [])
        rounds = []
        for itm in range(8):
            if itm <= 0:
                continue
            rounds.append({'ky': itm, 'vl': itm})
        round_options = get_select_options(rounds, 'ky', 'vl', [])
        interview_type = self.interview_type
        interview_types = []
        for itm in interview_type:
            value = interview_type[itm]
            interview_types.append({'ky': itm, 'vl': value})
        interview_options = get_select_options(interview_types, 'ky', 'vl', [])
        interview_channel = self.interview_channel
        interview_channels = []
        for itm in interview_channel.keys():
            value = interview_channel[itm]
            interview_channels.append({'ky': itm, 'vl': value})
        channel_options = get_select_options(interview_channels, 'ky', 'vl', [])
        resp.context = {'countryobj': countryobj, 'stateobj': stateobj, 'static_url': self.staticurl,
                        'job_options': job_options, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'round_options': round_options, 'interview_type': interview_options,
                        'interview_channel': channel_options,
                        'schedule_url': 'listinterviewer',
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'jsfile': 'Assigning_interviewer.js', 'validate_js': 'Scheduler_validate.js'}

    @template_path.render('assigning_interviewer_edit.html')
    def on_post_editinterviewer(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.context.model['txn'][0]
        print(operation)
        (job, candidate) = operation.split('#')
        print(job, candidate)
        schedule_obj = self.scheduleObj.scheduler_get_by_candidate(job, candidate)
        round_options = get_select_options(
            [{'ky': schedule_obj.schedule[-1].round_number, 'vl': schedule_obj.schedule[-1].round_number}], 'ky', 'vl',
            [schedule_obj.schedule[-1].round_number])
        interview_options = get_select_options(
            [{'ky': schedule_obj.schedule[-1].interview_type, 'vl': schedule_obj.schedule[-1].interview_type}], 'ky',
            'vl', [schedule_obj.schedule[-1].interview_type])
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'jobcode': schedule_obj.job.code, 'candidate_email': schedule_obj.applicant.email,
                        'candidate_name': schedule_obj.applicant.first_name + ' ' + schedule_obj.applicant.last_name,
                        'interviewer_name': schedule_obj.schedule[-1].interviewer.interviewer_name,
                        'interviewer_email': schedule_obj.schedule[-1].interviewer.interviewer_email,
                        'interviewer_phone': schedule_obj.schedule[-1].interviewer.interviewer_phone,
                        'scheduled_datetime': schedule_obj.schedule[-1].scheduled_datetime,
                        'schedule': schedule_obj, 'round': round_options, 'interview': interview_options,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'], 'schedule_url': 'listinterviewer',
                        'jsfile': 'Assigning_interviewer.js', 'validate_js': 'Scheduler_validate.js'}

    # Interviewer acceptance
    @template_path.render('interviewer_acceptance_list.html')
    def on_get_interviewer_listpage(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'interviewer_acceptance_url': 'interviewer_listpage',
                        'jsfile': 'Interviewer_acceptance.js', 'validate_js': 'Scheduler_validate.js'}

    @template_path.render('interviewer_acceptance_edit.html')
    def on_post_interviewer_edit(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        operation = req.context.model['txn'][0]
        print(operation)
        (job, candidate) = operation.split('#')
        print(job, candidate)
        schedule_obj = self.scheduleObj.scheduler_get_by_candidate(job, candidate)
        round_options = get_select_options(
            [{'ky': schedule_obj.schedule[-1].interview_type, 'vl': schedule_obj.schedule[-1].interview_type}], 'ky',
            'vl',
            [schedule_obj.schedule[-1].interview_type])
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'jobcode': schedule_obj.job.code, 'candidate_email': schedule_obj.applicant.email,
                        'candidate_name': schedule_obj.applicant.first_name + ' ' + schedule_obj.applicant.last_name,
                        'interviewer_name': schedule_obj.schedule[-1].interviewer.interviewer_name,
                        'interviewer_email': schedule_obj.schedule[-1].interviewer.interviewer_email,
                        'scheduled_datetime': schedule_obj.schedule[-1].scheduled_datetime,
                        'schedule': schedule_obj, 'round': round_options,
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'interviewer_acceptance_url': 'interviewer_listpage',
                        'jsfile': 'Interviewer_acceptance.js', 'validate_js': 'Scheduler_validate.js'}

    @template_path.render('feedback_list.html')
    def on_get_feedback(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'feedback_url': 'feedbacklist',
                        'jsfile': 'feedback.js', 'validate_js': 'feedback_validate.js'}

    @template_path.render('feedback_add.html')
    def on_get_addfeedback(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        JobObj = self.jobObj.get_objects()
        job_options = get_select_options(JobObj, 'code', 'code', [])
        positions = []
        for itm in range(11):
            if itm <= 0:
                continue
            positions.append({'ky': itm, 'vl': itm})
        positions_options = get_select_options(positions, 'ky', 'vl', [])
        interview_type = self.interview_type
        interview_types = []
        for itm in interview_type:
            value = interview_type[itm]
            interview_types.append({'ky': itm, 'vl': value})
        interview_options = get_select_options(interview_types, 'ky', 'vl', [])
        next_round = self.next_round
        next_rounds = []
        for itm in next_round:
            value = next_round[itm]
            next_rounds.append({'ky': itm, 'vl': value})
        next_round_options = get_select_options(next_rounds, 'ky', 'vl', [])
        resp.context = {'job_options': job_options, 'interview_options': interview_options,
                        'next_round_options': next_round_options,
                        'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'feedback_url': 'feedbacklist',
                        'jsfile': 'feedback.js', 'validate_js': 'feedback_validate.js'}

    # Job Offer
    @template_path.render('offer_list.html')
    def on_get_offer_list(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.context = {'static_url': self.staticurl, 'url': self.appurl, 'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'],
                        'offer_url': 'offer_list',
                        'jsfile': 'offer.js', 'validate_js': 'offer_validate.js'}

    @template_path.render('offer_add.html')
    def on_get_add_offer(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        JobObj = self.jobObj.get_objects()
        job_options = get_select_options(JobObj, 'code', 'code', [])
        resp.context = {'job_options': job_options, 'static_url': self.staticurl, 'url': self.appurl,
                        'apptitle': self.apptitle,
                        'jobcnt': self.jobObj.get_jobicon_count(), 'precnt': self.prescreningObj.prescreenicon_count(),
                        'schedcnt': self.scheduleObj.scheduleicon_count(),
                        'jobicon_url': settings.icon_pages['jobicon_url'],
                        'prescreenicon_url': settings.icon_pages['prescreenicon_url'],
                        'notscheduled_url': settings.icon_pages['notscheduled_url'],
                        'master_pages': settings.ui_pages['master_pages'],
                        'service_pages': settings.ui_pages['service_pages'], 'offer_url': 'offer_list',
                        'jsfile': 'offer.js', 'validate_js': 'offer_validate.js'}
