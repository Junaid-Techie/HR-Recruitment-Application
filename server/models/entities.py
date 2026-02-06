from mongoengine import *
import datetime


# eductation model
class EducationDoc(Document):
    qualification = StringField(required=True)
    specialisation = StringField(required=True)
    university = StringField(required=True)
    qualification_description = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'education'}


# skill set model
class SkillDoc(Document):
    skill_name = StringField(required=True)
    skill_desc = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'skills'}


# functionalorg model
class FunctionalOrgDoc(Document):
    functional_org = StringField(required=True)
    org_email = EmailField(required=True)
    cc_email = EmailField()
    status = BooleanField(default=True)
    meta = {'collection': 'functional_orgs'}


# country model
class CountryDoc(Document):
    country_name = StringField(required=True)
    desc = StringField()
    country_code = StringField(required=True)
    status = BooleanField(default=True)
    meta = {'collection': 'countries'}


# state model
class StateDoc(Document):
    country = ReferenceField(CountryDoc, dbref=True)
    state_name = StringField(required=True)
    state_desc = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'states'}


# city model
class CityDoc(Document):
    country = ReferenceField(CountryDoc, dbref=True, required=True)
    state = ReferenceField(StateDoc, dbref=True, required=True)
    city_name = StringField()
    address = StringField()
    city_desc = StringField()
    status = BooleanField(default=True)
    meta = {'collection': 'cities'}


# job model
class JobDoc(Document):
    code = StringField(required=True, default=None)
    title = StringField(required=True, default=None)
    location = ReferenceField(CityDoc)
    desc = StringField(required=True, default=None)
    functional_org = ListField(StringField(), required=True)
    positions = IntField(required=True)
    experience = StringField(required=True)
    edu = StringField(required=True)
    interview_pattern = ListField(StringField(), required=True)
    job_status = StringField(choices=['Open', 'Active', 'Hold', 'Closed', 'Filled'], default='Open')
    jd = FileField(required=True)
    client = StringField(required=True)
    status = BooleanField(default=True)
    required_skills = ListField(StringField(), required=True)
    hr_name = StringField(required=True)
    hr_email = EmailField(required=True)
    hr_phone = StringField(required=True)
    end_date = DateField(required=True)
    emp_type = StringField()
    meta = {'collection': 'jobs'}


# recruiter model
class RecruiterDoc(Document):
    emp_id = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField()
    middle_name = StringField()
    designation = StringField()
    phone = StringField(required=True)
    email = EmailField(required=True)
    location = ReferenceField(CityDoc, required=True)
    shift_start_time = StringField(required=True)
    shift_end_time = StringField(required=True)
    status = BooleanField(default=True)
    functional_org = ListField(StringField(), required=True)
    meta = {'collection': 'recruiters'}


# Source_assignment model
class SourcingAssignment(Document):
    job = ReferenceField(JobDoc)
    recruiter = ReferenceField(RecruiterDoc)
    meta = {'collection': 'assignments'}


# Resume model
class ResumeDoc(Document):
    resume = FileField()
    filename = StringField()
    content = StringField()
    content_type = StringField()
    meta = {'collection': 'resumes'}


# candidate model
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
    resume = ReferenceField(ResumeDoc, dbref=True)
    status = BooleanField(default=True)
    meta = {'collection': 'candidates'}


# interviewer model
class InterviewerDoc(EmbeddedDocument):
    interviewer_name = StringField()
    interviewer_email = StringField()
    interviewer_phone = StringField()
    primary_skills = ListField()
    entry_datetime = DateTimeField(default=datetime.datetime.now)


# Feedback
class FeedbackRefereceDoc(Document):
    feedback = FileField()
    filename = StringField()
    content = StringField()
    content_type = StringField()
    meta = {'collection': 'feedback_reference_doc'}


class ImageReferenceDoc(Document):
    image = ImageField()
    filename = StringField()
    content = StringField()
    content_type = StringField()
    meta = {'collection': 'image_reference_doc'}


# Schedule model
class ScheduleDoc(DynamicEmbeddedDocument):
    interviewer = EmbeddedDocumentField(InterviewerDoc)
    interview_type = StringField()
    scheduled_datetime = StringField()
    round_number = IntField()
    interview_channel = StringField(choices=['Face 2 Face', 'Through Video Call', 'Telephonic'], required=True)

    interviewer_acknowledge_status = StringField(choices=['Yet to Confirm', 'Accepted', 'Rejected'],
                                                 default='Yet to Confirm')
    interviewer_acknowledge_comments = StringField()
    interviewer_acknowledge_dt = DateTimeField()

    candidate_acknowledge_status = StringField(choices=['Yet to Confirm', 'Accepted', 'Rejected'],
                                               default='Yet to Confirm')
    candidate_acknowledge_comments = StringField()
    candidate_acknowledge_dt = DateTimeField()

    interview_feedback_comments = StringField()
    interview_evaluation_dt = StringField()
    next_round = StringField()
    interview_evalution_doc = ReferenceField(FeedbackRefereceDoc, dbref=True)
    applicant_pic = ReferenceField(ImageReferenceDoc, dbref=True)
    nextround_eligibility = BooleanField()

    update_datetime = DateTimeField(default=datetime.datetime.now)
    entry_datetime = DateTimeField(default=datetime.datetime.now)
    schedule_status = StringField(choices=['Ready', 'Yet to Confirm'], default='Ready')
    recruiter_comments = StringField()

    created_by = StringField()
    modified_by = StringField()


# Interview process model
class InterviewProcessDoc(DynamicDocument):
    job = ReferenceField(JobDoc)
    applicant = EmbeddedDocumentField(CandidateDoc)
    prescreen_status = StringField(choices=['New', 'Accept', 'Hold', 'Reject'], default='New')
    prescreen_comments = StringField()
    prescreen_approve_by = StringField()

    schedule = EmbeddedDocumentListField(ScheduleDoc)
    entry_datetime = DateTimeField(default=datetime.datetime.now)
    created_by = StringField()
    modified_by = StringField()

    meta = {'collection': 'interview_process'}


# Offer model
class OfferDoc(Document):
    job = ReferenceField(JobDoc)
    applicant = EmbeddedDocumentField("CandidateDoc")
    comments = StringField()
    join_date = StringField()
    offer_attachment = FileField()
    meta = {'collection': 'offers'}
