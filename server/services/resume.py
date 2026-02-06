from server.models import entities


class Resume:
    def __init__(self):
        pass

    def save(self, resume):
        doc = entities.ResumeDoc(
            resume=resume.get('resume'),
            filename=resume.get('filename'),
        )
        doc.save()
