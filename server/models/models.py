from mongoengine import *
import datetime


class SkillDoc(Document):
    skill_name= StringField()
    skill_desc = StringField()
    status = BooleanField(default=True)
    meta={
        'collection':'skills'
    }


class FunctionalOrgDoc(Document):
    functional_org = StringField()
    org_email = EmailField()
    cc_email = EmailField()
    status = BooleanField(default=True)
    meta = {
        'collection':'functional_orgs'
    }


class JobDoc(Document):
    code = StringField(required=True, default=None)
    title = StringField(required=True, default=None)
    location = StringField()
    desc = StringField(required=True, default=None)
    functional_org = ListField(StringField())
    positions = IntField()
    experience = StringField()
    edu = StringField()
    interview_pattern = ListField(StringField())
    job_status = StringField(choices=['Open', 'Active', 'Hold', 'Closed', 'Filled'], default='Open')
    jd = FileField()
    client = StringField()
    status = BooleanField(default=True)
    required_skills = ListField(StringField())
    emp_type = StringField()

    meta = {'collection': 'jobs'}


class RecruiterDoc(Document):
    emp_id = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField()
    middle_name = StringField()
    designation = StringField()
    phone = StringField()
    email = EmailField()
    location = StringField()
    shift_start_time = DateField()
    shift_end_time = DateField()
    status = BooleanField()

    meta = {'collection': 'recruiters'}


class SourcingAssignment(Document):
    job = ReferenceField(JobDoc)
    recruiter = ReferenceField(RecruiterDoc)

    meta = {'collection': 'assignments'}


class ResumeDoc(Document):
    resume = FileField()
    filename = StringField()
    content = StringField()
    content_type = StringField()
    meta = {
        'collection': 'resumes'
    }

class CandidateDoc(EmbeddedDocument):
    first_name = StringField(required=True, default=None)
    middle_name = StringField()
    last_name = StringField()
    phone = StringField(required=True, default=None)
    email = EmailField(required=True, default=None)
    primary_skill = ListField(StringField(), default=[])
    secondary_skill = ListField(StringField(), default=[])
    notice_period = IntField()
    experience = FloatField()
    education = StringField()
    resume = ReferenceField(ResumeDoc, dbref = True)
    status = BooleanField(default=True)
    meta = {'collection': 'candidates'}


class ScheduleDoc(EmbeddedDocument):
    interviewer_name = StringField()
    interviewer_email = StringField()
    interviewer_phone = StringField()
    scheduled_datetime = StringField()
    interviewer_acknowledgement = BooleanField()
    candidate_acknowledgement = BooleanField()
    candidate_comments = StringField()
    interview_feedback = StringField()
    nextround_eligibility = BooleanField()
    interview_type = ListField()
    reference_attachment = FileField()

class InterviewProcess(DynamicDocument):
    job = ReferenceField(JobDoc)
    applicant = EmbeddedDocument(CandidateDoc)
    prescreen_status = BooleanField()
    schedule =  EmbeddedDocumentListField(ScheduleDoc)



class ApplicationDoc(Document):
    job = ReferenceField(JobDoc, dbref=True)
    applicant = EmbeddedDocumentField("CandidateDoc")
    schedule = EmbeddedDocumentListField("ScheduleDoc")
    interview = EmbeddedDocumentListField("InterviewDoc")
    prescreen_status = BooleanField()
    meta = {
        'collection': 'applications'
    }

class PreScreeningDoc(Document):
    job = ReferenceField(JobDoc)
    applicant = EmbeddedDocumentField("CandidateDoc")
    #approved_rejected_role = ListField(StringField(), choices=['Admin', 'Manager', 'Recruiter'])
    #approved_rejected_by = ReferenceField(ListField(RecruiterDoc())
    shortlist_status = StringField(choices=['New', 'Reject', 'Accept', 'Hold'], default='New')
    prescreening_comments = StringField()
    prescreening_dt = DateTimeField(default=datetime.datetime.now)
    #prescreening_status = BooleanField()
    meta = {'collection': 'prescreening'}


class ScheduleDoc(Document):
    job = ReferenceField(JobDoc)
    candidate = ReferenceField(PreScreeningDoc)
    #candidate = ReferenceField(CandidateDoc)
    interviewer_name = StringField()
    interviewer_email = StringField()
    interviewer_phone = StringField()
    scheduled_datetime = StringField()
    interviewer_acknowledgement = BooleanField()
    candidate_acknowledgement = BooleanField()
    candidate_comments = StringField()
    recruiter_acknowledgement = BooleanField()
    recruiter_comments = StringField()

    schedule_status = StringField(choices=['Cancelled', 'Re-Schedule', 'Ready', 'Done'], default='Ready')
    meta = {'collection': 'schedules'}



class InterviewFeedbackDoc(Document):
    #application = ReferenceField(ApplicationDoc)
    schedule = ReferenceField(ScheduleDoc)
    interview_feedback = StringField()
    interview_type = ListField()
    reference_attachment = FileField()
    next_round = StringField()
    meta = {
        'collection': 'feedback'
    }


class EducationDoc(Document):
    qualification = StringField()
    university = StringField()
    qualification_description= StringField()
    status = BooleanField(default=True)
    meta = {
        'collection':'education'
    }


# class CityDoc(EmbeddedDocument):
#     city_name = StringField()
#     desc = StringField()
#     status = BooleanField(default=True)
#     meta = {'collection': 'countries'}
#
#
# class StateDoc(EmbeddedDocument):
#     city = EmbeddedDocumentListField("CityDoc")
#     state_name = StringField()
#     desc = StringField()
#     status = BooleanField(default=True)
#     meta = {'collection': 'countries'}


class CountryDoc(Document):
    country_name = StringField()
    desc = StringField()
    country_code = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'countries'}


class StateDoc(Document):
    country = ReferenceField(CountryDoc, dbref=True)
    state_name = StringField()
    state_desc = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'states'}


class CityDoc(Document):
    country = ReferenceField(CountryDoc, dbref=True)
    state = ReferenceField(StateDoc, dbref=True)
    city_name = StringField()
    address = StringField()
    city_desc = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'cities'}