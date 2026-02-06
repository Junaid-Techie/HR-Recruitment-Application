# HR Recruitment Application

## Overview

The **HR Recruitment Application** is a full-stack recruitment management system built with Python.  
It streamlines the complete hiring lifecycle including candidate management, job profiles, resume uploads, interview scheduling, prescreening, feedback, and offer management through a modular backend and a server-rendered web UI.

---

## Features

- Candidate lifecycle management
- Job profile creation and maintenance
- Resume and job description uploads
- Bulk resume upload
- Recruiter and interviewer assignment
- Interview scheduling
- Prescreening workflows
- Feedback and offer management
- Skill, education, and location master data
- Email notifications
- Centralized logging

---

## Architecture

\[
\text{UI} \rightarrow \text{API Layer} \rightarrow \text{Service Layer} \rightarrow \text{Models} \rightarrow \text{Storage}
\]

---

## Technology Stack

### Backend

- Python 3.x
- Flask (or Flask-compatible framework)
- REST-style APIs

### Frontend

- HTML (Jinja templates)
- CSS
- JavaScript
- jQuery
- DataTables

### Utilities

- Resume parsing and extraction
- SMTP-based email service
- Application logging

---

## Directory Structure

```text
HR-Recruitment-Application/
├── logs/
├── uploaded_files/
│   ├── candidateprofiles/
│   ├── jd/
│   └── jobprofiles/
│
├── README.md
├── requirements.txt
├── sendmail.py
├── server.py
│
├── server/
│   ├── api/
│   │   ├── applications.py
│   │   ├── candidate.py
│   │   ├── city.py
│   │   ├── country.py
│   │   ├── educations.py
│   │   ├── feedback.py
│   │   ├── functionalorg.py
│   │   ├── jobs.py
│   │   ├── offers.py
│   │   ├── prescreening.py
│   │   ├── recruiter.py
│   │   ├── scheduler.py
│   │   ├── skills.py
│   │   ├── state.py
│   │   └── __init__.py
│   │
│   ├── config/
│   │   ├── applogging.py
│   │   ├── badrequests.py
│   │   ├── config.py
│   │   ├── handlecors.py
│   │   ├── hooks.py
│   │   ├── middleware.py
│   │   ├── settings.py
│   │   └── __init__.py
│   │
│   ├── extraction/
│   │   ├── extract.py
│   │   ├── helpers.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── entities.py
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── application.py
│   │   ├── candidate.py
│   │   ├── city.py
│   │   ├── country.py
│   │   ├── education.py
│   │   ├── email.py
│   │   ├── feedback.py
│   │   ├── functionalorg.py
│   │   ├── job.py
│   │   ├── offer.py
│   │   ├── prescreening.py
│   │   ├── recruiter.py
│   │   ├── resume.py
│   │   ├── scheduler.py
│   │   ├── search.py
│   │   ├── servepages.py
│   │   ├── server_validation.py
│   │   ├── skill.py
│   │   ├── state.py
│   │   └── __init__.py
│   │
│   ├── ui/
│   │   ├── *.html
│   │   ├── css/
│   │   ├── js/
│   │   └── vendor assets
│   │
│   └── __init__.py


## Installation

### Prerequisites

- Python 3.7 or higher

### Clone Repository

    git clone <repository-url>
    cd HR-Recruitment-Application

### Create Virtual Environment

    python -m venv venv

### Activate Virtual Environment

Linux / macOS:

    source venv/bin/activate

Windows:

    venv\Scripts\activate

### Install Dependencies

    pip install -r requirements.txt

---

## Configuration

Configuration files are located at:

    server/config/

### Key Configuration Areas

- Application settings  
- Middleware and hooks  
- CORS handling  
- Logging configuration  
- Error handling  

---

## Running the Application

    python server.py

Application URL:

    http://localhost:PORT

The port is defined in `settings.py`.

---

## API Modules

### Candidate and Applications

- candidate.py  
- applications.py  

### Job and Hiring Workflow

- jobs.py  
- prescreening.py  
- scheduler.py  
- offers.py  
- feedback.py  

### Recruiter Management

- recruiter.py  

### Master Data

- skills.py  
- educations.py  
- city.py  
- state.py  
- country.py  
- functionalorg.py  

---

## UI Layer

UI templates and static assets are located at:

    server/ui/

### Includes

- Candidate management screens  
- Job profile management  
- Recruiter dashboards  
- Interview scheduling  
- Prescreening and feedback  
- Offer management  
- Resume upload and bulk upload  

---

## File Uploads

Uploaded files are stored locally at:

    uploaded_files/
    ├── candidateprofiles/
    ├── jd/
    └── jobprofiles/

Files are stored using UUID-based naming to avoid collisions.

---

## Logging

Application logs are written to:

    logs/

Logging configuration is defined in:

    server/config/applogging.py

---

## Email Service

Email notifications are handled using:

    sendmail.py

### Used For

- Interview notifications  
- Candidate communication  
- Offer letters  

---

## Security and Validation

- Server-side validation  
- Client-side form validation  
- CORS handling via middleware  
- File type and size validation  

---

## Known Limitations

- No role-based access control (RBAC)  
- Local filesystem storage only  
- No external authentication provider  
- Limited automated test coverage  

---

## Future Enhancements

- Role-based access control  
- Cloud storage integration  
- JWT / OAuth authentication  
- Resume–job matching intelligence  
- Analytics and reporting  
- Dockerized deployment  

---

## License

This project is intended for internal or educational use.  
Add a LICENSE file for public distribution.
