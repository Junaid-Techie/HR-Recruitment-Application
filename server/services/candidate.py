from server.models import entities

class Candidate():
    def __init__(self):
        pass

    def save(self, recruiter):
        doc = entities.CandidateDoc(
            emp_id=recruiter.get('emp_id'),
            first_name=recruiter.get('first_name'),
            middle_name=recruiter.get('middle_name'),
            last_name=recruiter.get('last_name'),
            phone=recruiter.get('phone'),
            email=recruiter.get('email'),
            designation=recruiter.get('designation'), )
        object.save(doc)
