import os, sys
dbcfg = {'dbname':'hiring_office',
    'host': 'localhost', # or external server address
    'port': 27017,
    'username': os.environ.get('MONGO_USER'),
    'password': os.environ.get('MONGO_PASS'),}
ui_params = {
'host': 'localhost',
'port': 8000,
'protocal': 'http',
'app_title': '/hroffice/',
'static': 'static/'
},

ui_pages ={

            'master_pages': [{'url': 'educationprofile', 'label': 'Education Master', 'title': 'Qualifications', 'suffix':'', 'icon': 'fa fa-graduation-cap'},
                             {'url': 'skillprofile', 'label': 'Technical Skills', 'title': 'Technical Skills', 'suffix':'', 'icon': 'fa fa-pencil'},
                             {'url': 'countryprofile', 'label': 'Country Profile', 'title': 'Country Profile', 'suffix': '', 'icon': 'fa fa-globe'},
                             {'url': 'stateprofile', 'label': 'State Profile', 'title': 'State Profile', 'suffix': '', 'icon': 'fa fa-map'},
                             {'url': 'cityprofile', 'label': 'City Profile', 'title': 'City Profile', 'suffix': '', 'icon': 'fa fa-building'},
                             {'url': 'funcorgprofile', 'label': 'Functional Org Profile', 'title': 'Functional Org Profile', 'suffix': '', 'icon': 'fa fa-users'},
                             ],
            'service_pages': [
                {'url': 'recruiter', 'label': 'Recruiter Profile', 'title': 'Recruiter Profile', 'suffix': '', 'icon': 'fa fa-user'},
                {'url': 'jobprofile', 'label': 'Job Profile', 'title': 'Job Profile', 'suffix':'', 'icon': 'fa fa-briefcase'},
                {'url': 'applications/candidateprofile', 'label': 'Upload Resume', 'title': 'Upload Candidate Profile', 'suffix': '', 'icon': 'fa fa-id-card'},
                {'url': 'applications/bulkcandidateprofile', 'label': 'Bulk Profiles Upload', 'title': 'Bulk Profiles Upload', 'suffix': '', 'icon': 'fa fa-files-o'},
                {'url': 'listprescreening', 'label': 'Profile Pre-screening', 'title': 'Profile Pre-screening', 'suffix': '','icon': 'fa fa-desktop'},
                {'url': 'listinterviewer', 'label': 'Schedule Interview', 'title': 'Schedule Interview', 'suffix': '', 'icon': 'fa fa-calendar'},
                {'url': 'interviewer_listpage', 'label': 'Interviewer Acceptance', 'title': 'Interviewer Acceptance', 'suffix': '','icon': 'fa fa-calendar-check-o'},
                {'url': 'feedbacklist', 'label': 'Interviewer Feedback', 'title': 'Interviewer Feedback', 'suffix': '', 'icon': 'fa fa-commenting'},
                {'url': 'offer_list', 'label': 'Release Offer', 'title': 'Offer', 'suffix': '', 'icon': 'fa fa-handshake-o'},
            ],
        }

icon_pages = {'jobicon_url':'jobicon','prescreenicon_url':'prescreenicon','notscheduled_url':'notscheduled'}


interview_type = {
    'Technical-1': 'Technical-1',
    'Technical-2': 'Technical-2',
    'Technical-3': 'Technical-3',
    'HR-1': 'HR-1',
    'HR-2': 'HR-2',
    'Managerial-1': 'Managerial-1',
    'Managerial-2': 'Managerial-2',
    'Offer': 'Offer',
    'Rejected': 'Rejected',
}
next_round = {
     'Technical-1': 'Technical-1',
    'Technical-2': 'Technical-2',
    'Technical-3': 'Technical-3',
    'HR-1': 'HR-1',
    'HR-2': 'HR-2',
    'Managerial-1': 'Managerial-1',
    'Managerial-2': 'Managerial-2',
    'Offer': 'Offer',
    'Rejected': 'Rejected',
}
interview_channel = {
    'Face 2 Face': 'Face 2 Face',
    'Through Video Call': 'Through Video Call',
    'Telephonic': 'Telephonic',
}

employement_type = {
    'Full Time' : 'Full Time',
    'Contract' : 'Contract',
    'Intern' : 'Intern',

}

email_params = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': '587',
    'smtp_user' : 'rohithsai160@gmail.com',
    'smtp_password' : 'rohithsai12345',
    'jobprofile' :{
                    'from_email': 'rohithsai160@gmail.com',
                    'to_email': 'rsurampally@nisum.com',
                    'subject': 'Needed your review on newly added Job Description in our tool with job code: ',
                    'message': """
                    <!DOCTYPE html>
                    <html>
                    <head>
                    <style>
                    table, th, td {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }
                    </style>
                    </head>
                        <body><p> Dear Recruiter/Manager,</p>
                            <p>Please review and approve below job requirement added in hroffice tool .</p>
                            <table style="width:100%">
                              <tr>
                                <th>Job Code</th>
                                <th>Jobtitle</th>
                                <th>Funtional Organisation</th>
                                <th>To Navigate</th>
                              </tr>
                              <tr>
                                <td>{{jobcode}}</td>
                                <td>{{jobtitle}}</td>
                                <td>{{func_org}}</td>
                                <td><a href="http://localhost:8000/hroffice/jobprofile?job_code={{Job Code}}">Click Here</a></td>
                              </tr>
                            </table> 
                            <p><strong>Regards,</strong></p>
                            <p>HROffice Tool</p>                            
                        </body>
                    </html>
                    """
                 },

    'jobprofile_edit': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Needed your review on Updated Job Description in our tool with job code: ',
        'message': """
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                table, th, td {
                  border: 1px solid black;
                  border-collapse: collapse;
                }
                </style>
                </head>
                    <body><p> Dear Recruiter/Manager,</p>
                        <p>Please review and approve below job requirement updated in hroffice tool .</p>
                        <table style="width:100%">
                          <tr>
                            <th>Job Code</th>
                            <th>Jobtitle</th>
                            <th>Funtional Organisation</th>
                            <th>To Navigate</th>
                          </tr>
                          <tr>
                            <td>{{jobcode}}</td>
                            <td>{{jobtitle}}</td>
                            <td>{{func_org}}</td>
                            <td><a href="http://localhost:8000/hroffice/jobprofile?job_code={{Job Code}}">Click Here</a></td>
                          </tr>
                        </table> 
                        <p><strong>Regards,</strong></p>
                        <p>HROffice Tool</p>                            
                    </body>
                </html>
                """
    },

    'resumeupload': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Needed your review on newly added Resumes in our tool with job code: ',
        'message': """
                <!DOCTYPE html>
                <html>
                <head>
                <style>
                table, th, td {
                  border: 1px solid black;
                  border-collapse: collapse;
                }
                </style>
                </head>
                    <body><p> Dear Recruiter/Manager,</p>
                        <p>Please review and approve below Uploaded Resumes in hroffice tool .</p>
                        <table style="width:100%">
                          <tr>
                            <th>Job Code</th>
                            <th>Candidate Name</th>
                            <th>Candidate Email</th>
                            <th>To Navigate</th>
                          </tr>
                          <tr>
                            <td>{{jobcode}}</td>
                            <td>{{candidate}}</td>
                            <td>{{email}}</td>
                            <td><a href="http://localhost:8000/hroffice/listprescreening">Click Here</a></td>
                          </tr>
                        </table> 
                        <p><strong>Regards,</strong></p>
                        <p>HROffice Tool</p>                            
                    </body>
                </html>
                """
    },

    'resumeedit': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Needed your review on Updated Resumes in our tool with job code: ',
        'message': """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
            </style>
            </head>
                <body><p> Dear Recruiter/Manager,</p>
                    <p>Please review and approve below Updated Resumes in hroffice tool .</p>
                    <table style="width:100%">
                      <tr>
                        <th>Job Code</th>
                        <th>Candidate Name</th>
                        <th>Candidate Email</th>
                        <th>To Navigate</th>
                      </tr>
                      <tr>
                        <td>{{jobcode}}</td>
                        <td>{{candidate}}</td>
                        <td>{{email}}</td>
                        <td><a href="http://localhost:8000/hroffice/listprescreening">Click Here</a></td>
                      </tr>
                    </table> 
                    <p><strong>Regards,</strong></p>
                    <p>HROffice Tool</p>                            
                </body>
            </html>
            """
    },

    'bulkupload': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Needed your review on newly added Resumes in our tool with job code: ',
        'message': """
            <!DOCTYPE html>
            <html>
            <head>
            <style>
            table, th, td {
              border: 1px solid black;
              border-collapse: collapse;
            }
            </style>
            </head>
                <body><p> Dear Recruiter/Manager,</p>
                    <p>Please review and approve below Uploaded Resumes in hroffice tool .</p>
                    <table style="width:100%">
                      <tr>
                        <th>Job Code</th>
                        <th>Functional Organization</th>
                        <th>To Navigate</th>
                      </tr>
                      <tr>
                        <td>{{jobcode}}</td>
                        <td>{{func_org}}</td>
                        <td><a href="http://localhost:8000/hroffice/listprescreening">Click Here</a></td>
                      </tr>
                    </table> 
                    <p><strong>Regards,</strong></p>
                    <p>HROffice Tool</p>                            
                </body>
            </html>
            """
    },

    'recruiterprofile': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Your Recruiter  Account successfully created for ',
        'message': """
                <!DOCTYPE html>
                <html>
                    <head>
                    <style>
                    table, th, td {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }
                    </style>
                    </head>                
                    <body><p> Dear Recruiter,</p>
                        <p>Welcome, Your account has been added in the hroffice application .</p>
                        <table style="width:100%">
                          <tr>
                            <th>Recruiter ID</th>
                            <th>Recruiter Name</th>
                            <th>Email</th>
                            <th>Mobile Number</th>
                            <th>To Navigate</th>
                          </tr>
                          <tr>
                            <td>{{emp_id}}</td>
                            <td>{{emp_name}}</td>
                            <td>{{email}}</td>
                            <td>{{phone}}</td>
                            <td><a href="http://localhost:8000/hroffice/recruiter">Click Here</a></td>
                          </tr>
                        </table> 
                        <p><strong>Regards,</strong></p>
                        <p>HROffice Tool</p>  
                    </body>
                </html>
                """
    },

    'recruiterprofile_edit': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Your Recruiter  Account successfully Updated for ',
        'message': """
                <!DOCTYPE html>
                <html>
                    <head>
                    <style>
                    table, th, td {
                      border: 1px solid black;
                      border-collapse: collapse;
                    }
                    </style>
                    </head>                
                    <body><p> Dear Recruiter,</p>
                        <p>Welcome, Your account has been updated in the hroffice application .</p>
                        <table style="width:100%">
                          <tr>
                            <th>Recruiter ID</th>
                            <th>Recruiter Name</th>
                            <th>Email</th>
                            <th>Mobile Number</th>
                            <th>To Navigate</th>
                          </tr>
                          <tr>
                            <td>{{emp_id}}</td>
                            <td>{{emp_name}}</td>
                            <td>{{email}}</td>
                            <td>{{phone}}</td>
                            <td><a href="http://localhost:8000/hroffice/recruiter">Click Here</a></td>
                          </tr>
                        </table> 
                        <p><strong>Regards,</strong></p>
                        <p>HROffice Tool</p>  
                    </body>
                </html>
                """
    },

    'prescreen': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'The Profile is ready for the scheduling the interviews for Job Code : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p> Dear Recruiter/Manager,</p>
                <p>Please review and approve below Uploaded Resumes in hroffice tool .</p>
                <table style="width:100%">
                  <tr>
                    <th>Job Code</th>
                    <th>Candidate Name</th>
                    <th>Candidate Email</th>
                    <th>Status</th>
                    <th>To Navigate</th>
                  </tr>
                  <tr>
                    <td>{{jobcode}}</td>
                    <td>{{c_name}}</td>
                    <td>{{c_email}}</td>
                    <td>{{shortlist_status}}</td>
                    <td><a href="http://localhost:8000/hroffice/listinterviewer">Click Here</a></td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
    },

    'assigning_interviewer': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Need your action for a Shortlisted Candidate Profile Interview scheduled for job code : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p> Dear Interviewer,</p>
                <p>Welcome, We have scheduled an interview on {{DT}}.</p>
                <table style="width:100%">
                  <tr>
                    <th>Job code</th>
                    <th>Candidate Name</th>
                    <th>Interviewer Name</th>
                    <th>Interviewer Email</th>
                    <th>Scheduled Date</th>
                    <th>Interview Type</th>
                    <th>To Navigate</th>
                  </tr>
                  <tr>
                    <td>{{JOB}}</td>
                    <td>{{CANDIDATE}}</td>
                    <td>{{interviewer_name}}</td>
                    <td>{{interviewer_email}}</td>
                    <td>{{DT}}</td>
                    <td>{{interview_type}}</td>
                    <td><a href="http://localhost:8000/hroffice/interviewer_listpage">Click Here</a></td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
        },

    'interviewer_status': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'The Profile is ready for the further processing for job code : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p> Dear Interviewer,</p>
                <p>Welcome, We have scheduled an interview on {{DT}}.</p>
                <table style="width:100%">
                  <tr>
                    <th>Job Code</th>
                    <th>Candidate Name</th>
                    <th>Interviewer Name</th>
                    <th>Interviewer Type</th>
                    <th>Scheduled Date</th>
                    <th>Scheduled Status</th>
                    <th>To Navigate</th>
                  </tr>
                  <tr>
                    <td>{{JOB}}</td>
                    <td>{{CANDIDATE}}</td>
                    <td>{{interviewer_name}}</td>
                    <td>{{interview_type}}</td>
                    <td>{{DT}}</td>
                    <td>{{schedule_status}}</td>
                    <td><a href="http://localhost:8000/hroffice/interviewer_listpage">Click Here</a></td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
        },

    'interviewer_reschedule': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Re-Schedule request for Candidate Profile : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p> Dear Recruiter/Admin,</p>
                <p>Please Re-Schedule an interview on {{DT}} for below details.</p>
                <table style="width:100%">
                  <tr>
                    <th>Job Code</th>
                    <th>Candidate Name</th>
                    <th>Interviewer Name</th>
                    <th>Interviewer Type</th>
                    <th>Scheduled Date</th>
                    <th>Scheduled Status</th>
                    <th>To Navigate</th>
                  </tr>
                  <tr>
                    <td>{{JOB}}</td>
                    <td>{{CANDIDATE}}</td>
                    <td>{{interviewer_name}}</td>
                    <td>{{interview_type}}</td>
                    <td>{{DT}}</td>
                    <td>{{schedule_status}}</td>
                    <td><a href="http://localhost:8000/hroffice/listinterviewer?job={{JOB}}&candidate={{CANDIDATE}}">Click Here</a></td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
        },

    'scheduler_reassign': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Need your action for a Shortlisted Candidate Profile Interview scheduled for Job Code : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p> Dear Interviewer,</p>
                <p>Welcome, We have Re-Scheduled an interview on {{DT}}.</p>
                <table style="width:100%">
                  <tr>
                    <th>Job Code</th>
                    <th>Candidate Name</th>
                    <th>Interviewer Name</th>
                    <th>Interviewer Type</th>
                    <th>Scheduled Date</th>
                    <th>To Navigate</th>
                  </tr>
                  <tr>
                    <td>{{JOB}}</td>
                    <td>{{CANDIDATE}}</td>
                    <td>{{interviewer_name}}</td>
                    <td>{{interview_type}}</td>
                    <td>{{DT}}</td>
                    <td><a href="http://localhost:8000/hroffice/interviewer_listpage">Click Here</a></td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
        },

    'feedback': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Interview Feedback for the Candidate : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p>  Dear Recruiter/Manager,</p>
                <p> This is a Feedback on the {{CANDIDATE}} for Job Code {{JOB}}.</p>
                <table style="width:100%">
                  <tr>
                    <th>Job Code</th>
                    <th>Candidate Name</th>
                    <th>Round Name</th>
                    <th>Next Round</th>
                    <th>To Navigate</th>
                  </tr>
                  <tr>
                    <td>{{JOB}}</td>
                    <td>{{CANDIDATE}}</td>
                    <td>{{interview_type}}</td>
                    <td>{{next_round}}</td>
                    <td><a href="http://localhost:8000/hroffice/feedbacklist">Click Here</a></td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
        },

    'offer': {
        'from_email': 'rohithsai160@gmail.com',
        'to_email': 'rsurampally@nisum.com',
        'subject': 'Releasing Offer for the Job Code : ',
        'message': """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>
            <body><p>  Dear {{CANDIDATE}} ,</p>
                <p> Congratulation, Your Profile has been selected. Please find the Offer Letter in the Attachment below</p>
                <table style="width:100%">
                  <tr>
                    <th>Job Code</th>
                    <th>Candidate Name</th>
                    <th>Join Date</th>
                  </tr>
                  <tr>
                    <td>{{JOB}}</td>
                    <td>{{CANDIDATE}}</td>
                    <td>{{join_date}}</td>
                  </tr>
                </table> 
                <p><strong>Regards,</strong></p>
                <p>HROffice Tool</p>                            
            </body>
        </html>
        """
        },

}