# HR Recruitment Application

A full-stack **HR Recruitment Management System** built with Python to manage the complete hiring lifecycle—from job creation to candidate selection—through a modular backend and a server-rendered web interface.

---

## 📘 Overview

The **HR Recruitment Application** streamlines recruitment workflows including candidate management, job profiles, resume uploads, interview scheduling, prescreening, feedback, and offer management.  
It is designed with a clean separation of concerns, making it scalable, maintainable, and extensible.

---

## ✨ Key Features

| Category | Capabilities |
|-------|-------------|
| Candidate Management | Candidate profiles, applications, resumes |
| Job Management | Job profiles, skills, locations |
| Recruitment Workflow | Prescreening, interview scheduling, offers |
| Recruiter Tools | Recruiter & interviewer assignment |
| Automation | Email notifications |
| Data Management | Skills, education, city, state, country |
| Utilities | Resume parsing, bulk uploads |
| Operations | Centralized logging & validation |

---

## 🧱 Architecture

\[
\text{UI} \rightarrow \text{API Layer} \rightarrow \text{Service Layer} \rightarrow \text{Models} \rightarrow \text{Storage}
\]

| Layer | Description |
|-----|------------|
| UI | HTML templates, CSS, JavaScript |
| API | REST-style endpoints |
| Services | Business logic & workflows |
| Models | Entities & database abstraction |
| Storage | File system uploads & logs |

---

## 🛠 Technology Stack

### Backend
| Technology | Purpose |
|----------|--------|
| Python 3.x | Core language |
| Flask | Web framework |
| REST APIs | Communication layer |

### Frontend
| Technology | Purpose |
|----------|--------|
| HTML (Jinja) | Server-side templates |
| CSS | Styling |
| JavaScript / jQuery | Interactivity |
| DataTables | Tabular UI components |

### Utilities
| Utility | Purpose |
|--------|--------|
| Resume Parsing | Extract candidate data |
| SMTP | Email notifications |
| Logging | Audit & debugging |

---

## 📁 Directory Structure

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
│   ├── config/
│   ├── extraction/
│   ├── models/
│   ├── services/
│   ├── ui/
│   └── __init__.py

## 🚀 Installation

### Prerequisites

- Python 3.7+
- pip
- Virtual environment (recommended)

### Setup Steps

Command Line (Shell):

    git clone <repository-url>
    cd HR-Recruitment-Application
    python -m venv venv

### Activate Virtual Environment

Linux / macOS:

    source venv/bin/activate

Windows:

    venv\Scripts\activate

### Install Dependencies

    pip install -r requirements.txt

---

## ⚙ Configuration

Configuration files are located at:

    server/config/

### Configuration Scope

| Area       | Description                      |
|------------|----------------------------------|
| Settings   | Environment & app config         |
| Middleware | Request/response handling        |
| CORS       | Cross-origin configuration       |
| Logging    | Log levels & formatting          |
| Errors     | Centralized error handling       |

---

## ▶ Running the Application

Command Line (Shell):

    python server.py

Application URL:

    http://localhost:PORT

Note: The port is defined in `settings.py`.

---

## 🔌 API Modules

### Core Domains

| Module            | Responsibility            |
|-------------------|---------------------------|
| candidate.py      | Candidate management      |
| applications.py   | Job applications          |
| jobs.py           | Job profiles              |
| prescreening.py   | Prescreen workflows       |
| scheduler.py      | Interview scheduling     |
| offers.py         | Offer management          |
| feedback.py       | Interview feedback        |

### Master Data

- skills.py
- educations.py
- city.py
- state.py
- country.py
- functionalorg.py

---

## 🖥 UI Layer

UI templates and static assets are located at:

    server/ui/

### Screens Include

- Candidate management
- Job profiles
- Recruiter dashboards
- Interview scheduling
- Prescreening & feedback
- Offer management
- Resume & bulk uploads

---

## 📂 File Uploads

Uploaded files are stored locally:

    uploaded_files/
    ├── candidateprofiles/
    ├── jd/
    └── jobprofiles/

Files are stored using UUID-based naming to avoid collisions.

---

## 📝 Logging

Logs are written to:

    logs/

Configured via:

    server/config/applogging.py

---

## ✉ Email Service

Handled by:

    sendmail.py

### Used For

- Interview notifications
- Candidate communication
- Offer letters

---

## 🔐 Security & Validation

- Server-side validation
- Client-side form validation
- CORS handling via middleware
- File type & size validation

---

## ⚠ Known Limitations

- No role-based access control (RBAC)
- Local filesystem storage only
- No external authentication provider
- Limited automated test coverage

---

## 🔮 Future Enhancements

- Role-based access control
- Cloud storage integration
- JWT / OAuth authentication
- Resume–job matching intelligence
- Analytics & reporting dashboard
- Dockerized deployment

---

## 📜 License

MIT License

Copyright © 2026 Junaid-Techie

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the “Software”), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND.

---

💡 Maintained by **Junaid-Techie**
