import falcon
from server.config import middleware, settings, handlecors
from server.config.badrequests import ErrorHandler
from wsgiref import simple_server
from mongoengine import connect
from server.services.servepages import ServePages
from server.api.educations import Education
from server.api.country import Country, CountryAPI
from server.api.state import State, StateAPI
from server.api.city import City, CityAPI
from server.api.skills import Skills
from server.api.functionalorg import FunctionalOrg
from server.api.recruiter import Recruiter, RecruiterAPI
from server.api.jobs import Jobs, JobSearch
import os
from server.config.config import get_html_template_path, get_appurl, get_apptitle, get_staticurl
from beaker.middleware import SessionMiddleware
from server.api.applications import MapApplications, Applications
from server.api.prescreening import Prescreening, PrescreeningAPI
from server.api.scheduler import Scheduling, SchedulingAPI
from server.api.feedback import Feedback
from server.api.offers import OfferApi

falcon_app = falcon.API(
    middleware=[handlecors.Handlecors(), middleware.BodyTransformation()])  # , media_type='application/vnd.api+json'

template_path = get_html_template_path()

# Job Apis
# print(template_path)
# app.add_route('/', RecruiterAPI(), suffix='all')
app_title = get_apptitle()
static_title = get_staticurl()

falcon_app.add_static_route(app_title + static_title + 'css', template_path + "\\" + "css")
falcon_app.add_static_route(app_title + static_title + 'js', template_path + "\\" + "js")

falcon_app.add_route(app_title + 'home', ServePages(), suffix='home')
falcon_app.add_route(app_title + 'index.html', ServePages(), suffix='home')
falcon_app.add_route(app_title, ServePages(), suffix='home')
falcon_app.add_route('/', ServePages(), suffix='home')

# falcon_app.add_route(app_title + 'login', ServePages(), suffix='login')

# Education
falcon_app.add_route(app_title + 'educationprofile', ServePages(), suffix='educationprofile')
falcon_app.add_route(app_title + 'addeducation', ServePages(), suffix='addeducation')
falcon_app.add_route(app_title + 'editeducation', ServePages(), suffix='editeducation')

# falcon_app.add_route('/recruiters', RecruiterAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/educations/addrecord', Education())
falcon_app.add_route(app_title + 'api/educations/fetchrecord', Education(), suffix='all')
falcon_app.add_route(app_title + 'api/educations/editstatus', Education(), suffix='updatestatus')
falcon_app.add_route(app_title + 'api/educations/putrecord', Education(), suffix='eduputreq')

# country
falcon_app.add_route(app_title + 'countryprofile', ServePages(), suffix='countryprofile')
falcon_app.add_route(app_title + 'addcountry', ServePages(), suffix='addcountry')
falcon_app.add_route(app_title + 'editcountry', ServePages(), suffix='editcountry')

# Country Apis
falcon_app.add_route(app_title + 'api/country/addrecord', Country())
falcon_app.add_route(app_title + 'api/country/putrecord', Country(), suffix='update')
falcon_app.add_route(app_title + 'api/country/deleterecord/code/{data}', Country(), suffix='trash_collection')
falcon_app.add_route(app_title + 'api/country/getrecords', CountryAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/country/getrecords/Country_name/{name}', CountryAPI(), suffix='byname')
falcon_app.add_route(app_title + 'api/country/editstatus', Country(), suffix='updatestatus')

# State Apis
falcon_app.add_route(app_title + 'api/state/addrecord', State())
falcon_app.add_route(app_title + 'api/state/putrecord', State(), suffix='update')
falcon_app.add_route(app_title + 'api/state/deleterecord/state_name/{data}', State(), suffix='trash_collection')
falcon_app.add_route(app_title + 'api/state/getrecords', StateAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/state/getrecords/state_name/{name}', StateAPI(), suffix='byname')
falcon_app.add_route(app_title + 'api/state/editstatus', State(), suffix='updatestatus')

# state
falcon_app.add_route(app_title + 'stateprofile', ServePages(), suffix='stateprofile')
falcon_app.add_route(app_title + 'addstate', ServePages(), suffix='addstate')
falcon_app.add_route(app_title + 'editstate', ServePages(), suffix='editstate')

# city
falcon_app.add_route(app_title + 'cityprofile', ServePages(), suffix='cityprofile')
falcon_app.add_route(app_title + 'addcity', ServePages(), suffix='addcity')
falcon_app.add_route(app_title + 'editcity', ServePages(), suffix='editcity')

# City Apis
falcon_app.add_route(app_title + 'api/city/addrecord', City())
falcon_app.add_route(app_title + 'api/city/putrecord', City(), suffix='update')
falcon_app.add_route(app_title + 'api/city/deleterecord/city_name/{data}', City(), suffix='trash_collection')
falcon_app.add_route(app_title + 'api/city/getrecords', CityAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/city/getrecords/city_name/{name}', CityAPI(), suffix='byname')
falcon_app.add_route(app_title + 'api/city/editstatus', City(), suffix='updatestatus')
falcon_app.add_route(app_title + 'api/city/getstates', CityAPI(), suffix='states')
falcon_app.add_route(app_title + 'api/city/getcities', CityAPI(), suffix='cities')

# Skillset
# skill api
falcon_app.add_route(app_title + 'api/skills/addskill', Skills())
falcon_app.add_route(app_title + 'api/skills/fetchskills', Skills(), suffix='all')
falcon_app.add_route(app_title + 'api/skills/editrecord', Skills(), suffix='update')
falcon_app.add_route(app_title + 'api/skills/editstatus', Skills(), suffix='updatestatus')

# skills
falcon_app.add_route(app_title + 'skillprofile', ServePages(), suffix='skillsprofile')
falcon_app.add_route(app_title + 'addskill', ServePages(), suffix='addskill')
falcon_app.add_route(app_title + 'editskill', ServePages(), suffix='editskill')

# functional org
falcon_app.add_route(app_title + 'api/funcorg/addrecord', FunctionalOrg())
falcon_app.add_route(app_title + 'api/funcorg/fetchrecord', FunctionalOrg(), suffix='all')
falcon_app.add_route(app_title + 'api/funcorg/editstatus', FunctionalOrg(), suffix='updatestatus')
falcon_app.add_route(app_title + 'api/funcorg/putrecord', FunctionalOrg(), suffix='orgputreq')

# functional orgs
falcon_app.add_route(app_title + 'funcorgprofile', ServePages(), suffix='orgprofile')
falcon_app.add_route(app_title + 'addorg', ServePages(), suffix='addorg')
falcon_app.add_route(app_title + 'editorg', ServePages(), suffix='editorg')

# Recruiter
falcon_app.add_route(app_title + 'recruiterprofile', ServePages(), suffix='recruiter')
falcon_app.add_route(app_title + 'addrecruiter', ServePages(), suffix='addrecruiter')
falcon_app.add_route(app_title + 'editrecruiter', ServePages(), suffix='editrecruiter')
falcon_app.add_route(app_title + 'recruiter', ServePages(), suffix='recruiter')

falcon_app.add_route(app_title + 'api/recruiter/addrecord', Recruiter())
# falcon_app.add_route(app_title + 'api/recruiter/updaterecord', Recruiter(), suffix='update')
falcon_app.add_route(app_title + 'api/recruiter/putrecord', Recruiter(), suffix='putreq')
falcon_app.add_route(app_title + 'api/recruiter/getrecord/first_name/{name}', RecruiterAPI(), suffix='byname')
falcon_app.add_route(app_title + 'api/recruiter/deleterecord/data/{data}', Recruiter(), suffix='trash_collection')
falcon_app.add_route(app_title + 'api/recruiter/getrecord/data/{data}', RecruiterAPI(), suffix='list')
falcon_app.add_route(app_title + 'api/recruiter/getrecords', RecruiterAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/recruiter/editstatus', Recruiter(), suffix='updatestatus')

# Job profile
falcon_app.add_route(app_title + 'jobprofile', ServePages(), suffix='jobprofile')
falcon_app.add_route(app_title + 'addjobprofile', ServePages(), suffix='addjobprofile')
falcon_app.add_route(app_title + 'editjobprofile', ServePages(), suffix='editjobprofile')

falcon_app.add_route(app_title + 'api/jobs/addrecord', Jobs())
falcon_app.add_route(app_title + 'api/jobs/deleterecord/code/{code}', Jobs(), suffix='collection')
falcon_app.add_route(app_title + 'api/jobs/getrecords', JobSearch(), suffix='all')
falcon_app.add_route(app_title + 'api/jobs/getrecord/id/{id}', JobSearch(), suffix='id')
falcon_app.add_route(app_title + 'api/jobs/getrecord/title/{title}', JobSearch(), suffix='title')
falcon_app.add_route(app_title + 'api/jobs/getrecord/company/{company}', JobSearch(), suffix='company')
falcon_app.add_route(app_title + 'api/jobs/getrecord/title-company', JobSearch(), suffix='titlecompany')
falcon_app.add_route(app_title + 'api/jobs/updaterecord', Jobs(), suffix='update')
falcon_app.add_route(app_title + 'api/jobs/updatestatus', Jobs(), suffix='updatestatus')
falcon_app.add_route(app_title + 'jobicon', ServePages(), suffix='jobicon')
falcon_app.add_route(app_title + 'api/jobs/getnotclosed', JobSearch(), suffix='notclosed')
falcon_app.add_route(app_title + 'api/jobs/skillsearch', JobSearch(), suffix='all_skillsearch')

falcon_app.add_route(app_title + 'api/applications/jobpreviewfile', JobSearch(), suffix='jobpreviewfile')

# applications
falcon_app.add_route(app_title + 'applications/candidateprofile', ServePages(), suffix='listcandidate')
falcon_app.add_route(app_title + 'applications/uploadresume', ServePages(), suffix='uploadresume')
falcon_app.add_route(app_title + 'applications/editcandidate', ServePages(), suffix='editcandidate')
falcon_app.add_route(app_title + 'applications/bulkcandidateprofile', ServePages(), suffix='bulkresumeupload')
falcon_app.add_route(app_title + 'api/applications/upload-applications', MapApplications())
falcon_app.add_route(app_title + 'api/applications/upload-bulk-applications', MapApplications(),
                     suffix='bulkresumeupload')
falcon_app.add_route(app_title + 'api/applications/putrecord', MapApplications(), suffix='putreq')
falcon_app.add_route(app_title + 'api/applications/editcandidate_status', MapApplications(), suffix='edit_status')
falcon_app.add_route(app_title + 'api/applications', Applications())
falcon_app.add_route(app_title + 'api/applications/{id}', Applications())
falcon_app.add_route(app_title + 'api/applications/job', Applications())
falcon_app.add_route(app_title + 'api/applications/job/{job}', Applications(), suffix='job')
falcon_app.add_route(app_title + 'api/applications/jobpreviewfile', JobSearch(), suffix='jobpreviewfile')
falcon_app.add_route(app_title + 'api/applications/candidatepreviewfile', Applications(), suffix='candidatepreviewfile')
falcon_app.add_route(app_title + 'api/applications/candidatesearch', MapApplications(), suffix='all_search')

# prescreening
falcon_app.add_route(app_title + 'listprescreening', ServePages(), suffix='prescreening')
falcon_app.add_route(app_title + 'editprescreening', ServePages(), suffix='editprescreening')

# prescreening api
falcon_app.add_route(app_title + 'api/prescreen/getrecords', PrescreeningAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/prescreen/editstatus', Prescreening(), suffix='updatestatus')
falcon_app.add_route(app_title + 'prescreenicon', ServePages(), suffix='prescreenicon')
falcon_app.add_route(app_title + 'api/prescreen/getnotaccepted', PrescreeningAPI(), suffix='notaccepted')

# assign interviewer
falcon_app.add_route(app_title + 'listinterviewer', ServePages(), suffix='interviewer')
falcon_app.add_route(app_title + 'editinterviewer', ServePages(), suffix='editinterviewer')
falcon_app.add_route(app_title + 'addinterviewer', ServePages(), suffix='addinterviewer')
# interviewer acceptance
falcon_app.add_route(app_title + 'interviewer_listpage', ServePages(), suffix='interviewer_listpage')
falcon_app.add_route(app_title + 'interviewer_edit', ServePages(), suffix='interviewer_edit')

# Assign Interviewer
falcon_app.add_route(app_title + 'api/scheduler/assign_interviewer', Scheduling(), suffix='assign_interviewer')
falcon_app.add_route(app_title + 'api/scheduler/re_assign', Scheduling(), suffix='re_assign')
falcon_app.add_route(app_title + 'api/scheduler/getrecords', SchedulingAPI(), suffix='all')
falcon_app.add_route(app_title + 'api/scheduler/recruiter_status', Scheduling(), suffix='recruiter_status')
falcon_app.add_route(app_title + 'api/scheduler/shortlistedprofiles/job/{job}', SchedulingAPI(),
                     suffix='shortlisted_jobs')
falcon_app.add_route(app_title + 'api/scheduler/interviewer_status', Scheduling(), suffix='interviewer_status')
falcon_app.add_route(app_title + 'api/scheduler/interviewer_edit', Scheduling(), suffix='interviewer_edit')
falcon_app.add_route(app_title + 'notscheduled', ServePages(), suffix='notscheduled')
falcon_app.add_route(app_title + 'api/scheduler/notschedule', SchedulingAPI(), suffix='notschedule')

# feedback
falcon_app.add_route(app_title + 'feedbacklist', ServePages(), suffix='feedback')
falcon_app.add_route(app_title + 'addfeedback', ServePages(), suffix='addfeedback')
# #feedback apis
falcon_app.add_route(app_title + 'api/feedback/fetchrecords', Feedback(), suffix='all')
falcon_app.add_route(app_title + 'api/feedback/addrecord', Feedback())
falcon_app.add_route(app_title + 'api/feedback/shortlistapplication/job/{job}', Feedback(),
                     suffix='shortlisted_applications')
falcon_app.add_route(app_title + 'api/feedback/interviewtype', Feedback(), suffix='interview_type')

# offer pages
falcon_app.add_route(app_title + 'offer_list', ServePages(), suffix='offer_list')
falcon_app.add_route(app_title + 'addoffer', ServePages(), suffix='add_offer')
# offer apis
falcon_app.add_route(app_title + 'api/offer/addrecord', OfferApi())
falcon_app.add_route(app_title + 'api/offer/getrecords', OfferApi(), suffix='all')
falcon_app.add_route(app_title + 'api/offer/offered_applicants/job/{job}', OfferApi(), suffix='accepted_offers')

if __name__ == "__main__":
    # connect('hiring_office', username='', password='', host=)
    con = connect(settings.dbcfg['dbname'], host=settings.dbcfg['host'], port=settings.dbcfg['port'],
                  username=settings.dbcfg['username'], password=settings.dbcfg['password'])

    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    print(PROJECT_ROOT)

    session_opts = {'session.type': 'ext:memcached',
                    'session.url': 'localhost:8000',  # '10.176.199.101:11211;10.176.199.102:11211',
                    'session.cookie_expires': True,
                    'session.data_dir': PROJECT_ROOT + '\session',
                    'session.use_cookies': False,
                    'cache.lock_dir': PROJECT_ROOT + '\lock',
                    'cache.short_term.expire': '1800',
                    '_path': PROJECT_ROOT + '\session'}

    wsgi_falcon_app = SessionMiddleware(falcon_app, session_opts)
    # app = SessionMiddleware(app, session_opts)
    httpd = simple_server.make_server('127.0.0.1', 8000, wsgi_falcon_app)
    httpd.serve_forever()
