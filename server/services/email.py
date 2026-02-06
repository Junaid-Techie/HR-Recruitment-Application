import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from server.config import settings
from email.mime.base import MIMEBase
from email import encoders
import re

class Mail:
    def __init__(self):
        self.email_params = settings.email_params;

    def sendMail(self,):
        server = smtplib.SMTP(self.email_params.get('smtp_server'), self.email_params.get('smtp_port'))
        server.starttls()
        server.login(self.email_params.get('smtp_user'), self.email_params.get('smtp_password'))
        return server

    def jobprofile_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['jobprofile'].get('subject')+ ' '+data['jobcode']
        message = self.email_params['jobprofile'].get('message')
        message = message.replace('{{jobcode}}', data['jobcode'])
        message = message.replace('{{jobtitle}}', data['jobtitle'])
        message = message.replace('{{func_org}}', data['func_org'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']]+data['cc_email']), text)
        sendmailObj.quit()


    def jobprofile_edit_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['jobprofile_edit'].get('subject')+ ' '+data['jobcode']
        message = self.email_params['jobprofile_edit'].get('message')
        message = message.replace('{{jobcode}}', data['jobcode'])
        message = message.replace('{{jobtitle}}', data['jobtitle'])
        message = message.replace('{{func_org}}', data['func_org'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']]+data['cc_email']), text)
        sendmailObj.quit()



    def recruiterprofile_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Subject'] = self.email_params['recruiterprofile'].get('subject')+ ' '+data['emp_name']
        message = self.email_params['recruiterprofile'].get('message')
        message = message.replace('{{emp_id}}', data['emp_id'])
        message = message.replace('{{emp_name}}', data['emp_name'])
        message = message.replace('{{email}}', data['email'])
        message = message.replace('{{phone}}', data['phone'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], msg['To'], text)
        sendmailObj.quit()


    def recruiterprofile_edit_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Subject'] = self.email_params['recruiterprofile_edit'].get('subject')+ ' '+data['emp_name']
        message = self.email_params['recruiterprofile_edit'].get('message')
        message = message.replace('{{emp_id}}', data['emp_id'])
        message = message.replace('{{emp_name}}', data['emp_name'])
        message = message.replace('{{email}}', data['email'])
        message = message.replace('{{phone}}', data['phone'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], msg['To'], text)
        sendmailObj.quit()

    def resume_upload_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Subject'] = self.email_params['resumeupload'].get('subject')+ ' '+data['jobcode']
        message = self.email_params['resumeupload'].get('message')
        message = message.replace('{{jobcode}}', data['jobcode'])
        message = message.replace('{{candidate}}', data['candidate'])
        message = message.replace('{{email}}', data['email'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], msg['To'], text)
        sendmailObj.quit()


    def resume_edit_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Subject'] = self.email_params['resumeedit'].get('subject')+ ' '+data['jobcode']
        message = self.email_params['resumeedit'].get('message')
        message = message.replace('{{jobcode}}', data['jobcode'])
        message = message.replace('{{candidate}}', data['candidate'])
        message = message.replace('{{email}}', data['email'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], msg['To'], text)
        sendmailObj.quit()

    def bulk_upload_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Subject'] = self.email_params['bulkupload'].get('subject')+ ' '+data['jobcode']
        message = self.email_params['bulkupload'].get('message')
        message = message.replace('{{jobcode}}', data['jobcode'])
        message = message.replace('{{func_org}}', data['func_org'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], msg['To'], text)
        sendmailObj.quit()


    def prescreen_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['prescreen'].get('subject')+ ' '+data['jobcode']
        message = self.email_params['prescreen'].get('message')
        message = message.replace('{{jobcode}}', data['jobcode'])
        message = message.replace('{{c_name}}', data['c_name'])
        message = message.replace('{{c_email}}', data['c_email'])
        message = message.replace('{{shortlist_status}}', data['shortlist_status'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']]+data['cc_email']), text)
        sendmailObj.quit()


    def assigning_interviewer_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['assigning_interviewer'].get('subject') + ' '+data['jobcode']
        message = self.email_params['assigning_interviewer'].get('message')
        message = re.sub('{{DT}}', data.get('schedule_dt'), message)
        message = re.sub('{{JOB}}', data.get('jobcode'), message)
        message = re.sub('{{CANDIDATE}}', data.get('candidate'), message)
        message = message.replace('{{interviewer_name}}', data['interviewer_name'])
        message = message.replace('{{interviewer_email}}', data['interviewer_email'])
        message = message.replace('{{interview_type}}', data['interview_type'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']]+data['cc_email']), text)
        sendmailObj.quit()


    def interviewer_status_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['interviewer_status'].get('subject') + ' '+data['jobcode']
        message = self.email_params['interviewer_status'].get('message')
        message = re.sub('{{DT}}', data.get('schedule_date'), message)
        message = re.sub('{{JOB}}', data.get('jobcode'), message)
        message = re.sub('{{CANDIDATE}}', data.get('candidate'), message)
        message = message.replace('{{interviewer_name}}', data['interviewer_name'])
        message = message.replace('{{interview_type}}', data['interview_type'])
        message = message.replace('{{schedule_status}}', data['schedule_status'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']]+data['cc_email']), text)
        sendmailObj.quit()



    def interviewer_reschedule_sendmail(self,data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['interviewer_reschedule'].get('subject') + ' ' + data['candidate']
        message = self.email_params['interviewer_reschedule'].get('message')
        message = re.sub('{{DT}}', data.get('schedule_date'), message)
        message = re.sub('{{JOB}}', data.get('jobcode'), message)
        message = re.sub('{{CANDIDATE}}', data.get('candidate'), message)
        message = message.replace('{{interviewer_name}}', data['interviewer_name'])
        message = message.replace('{{interview_type}}', data['interview_type'])
        message = message.replace('{{schedule_status}}', data['schedule_status'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']] + data['cc_email']), text)
        sendmailObj.quit()


    def scheduler_reassign_sendmail(self,data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['scheduler_reassign'].get('subject') + ' ' + data['jobcode']
        message = self.email_params['scheduler_reassign'].get('message')
        message = re.sub('{{DT}}', data.get('schedule_dt'), message)
        message = re.sub('{{JOB}}', data.get('jobcode'), message)
        message = re.sub('{{CANDIDATE}}', data.get('candidate'), message)
        message = message.replace('{{interviewer_name}}', data['interviewer_name'])
        message = message.replace('{{interview_type}}', data['interview_type'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']] + data['cc_email']), text)
        sendmailObj.quit()



    def feedback_sendmail(self,data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['feedback'].get('subject')+' '+ data['candidate']
        message = self.email_params['feedback'].get('message')
        message = re.sub('{{JOB}}', data.get('jobcode'), message)
        message = re.sub('{{CANDIDATE}}', data.get('candidate'), message)
        message = message.replace('{{interview_type}}', data['interview_type'])
        message = message.replace('{{next_round}}', data['next_round'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']] + data['cc_email']), text)
        sendmailObj.quit()

    def offer_sendmail(self,data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] = data['to_email']
        msg['Cc'] = ", ".join(data['cc_email'])
        msg['Subject'] = self.email_params['offer'].get('subject') + ' ' + data['jobcode']
        filename = data["filename"]
        temp_file = re.split(r"\.", filename)[-1]
        attachment = open(data["filename"], "rb")
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename= %s" % data.get('candidate')+'.'+temp_file)
        msg.attach(p)
        message = self.email_params['offer'].get('message')
        message = re.sub('{{JOB}}', data.get('jobcode'), message)
        message = re.sub('{{CANDIDATE}}', data.get('candidate'), message)
        message = message.replace('{{join_date}}', data['join_date'])
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], ([msg['To']] + data['cc_email']), text)
        sendmailObj.quit()



    def candidate_acceptance_sendmail(self, data):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email_params['smtp_user']
        msg['To'] =data['to_email']
        msg['Subject'] = self.email_params['candidate_acceptance'].get('subject') + ' '+data['jobcode']
        message = self.email_params['candidate_acceptance'].get('message')
        #message = message.replace('{{email}}', data['email'])
        # msg.attach(MIMEText(settings.messagePlain, 'plain'))
        msg.attach(MIMEText(message, 'html'))
        text = msg.as_string()
        sendmailObj = self.sendMail()
        sendmailObj.sendmail(msg['From'], msg['To'], text)
        sendmailObj.quit()