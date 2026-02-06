# HR Recruitment Application

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Falcon](https://img.shields.io/badge/Falcon-High%20Performance%20API-lightgrey)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)
![License](https://img.shields.io/badge/License-MIT-green)

A full-stack **HR Recruitment Management System** built with **Python** and the **Falcon** framework. It manages the complete hiring lifecycle—from job creation to candidate selection—using a **MongoDB** database and a responsive frontend powered by **jQuery** and **AJAX**.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Directory Structure](#-directory-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Modules](#-api-modules)
- [UI & File Management](#-ui-layer)
- [Security & Limitations](#-security--validation)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 📘 Overview

The **HR Recruitment Application** streamlines recruitment workflows including candidate management, job profiles, resume uploads, interview scheduling, prescreening, feedback, and offer management. 

It leverages the **Falcon** web framework for high-performance REST APIs and **MongoDB** for flexible, document-based data storage. The frontend uses **AJAX** for seamless, asynchronous data interactions without page reloads.

---

## ✨ Key Features

| Category | Capabilities |
|:---|:---|
| **Candidate Management** | Candidate profiles, applications, resumes |
| **Job Management** | Job profiles, skills, locations |
| **Recruitment Workflow** | Prescreening, interview scheduling, offers |
| **Recruiter Tools** | Recruiter & interviewer assignment |
| **Automation** | Email notifications via SMTP |
| **Data Management** | Skills, education, city, state, country |
| **Utilities** | Resume parsing, bulk uploads |
| **Operations** | Centralized logging & validation |

---

## 🧱 Architecture

The application follows a Service-Oriented Architecture (SOA) style:

> **UI (jQuery/AJAX)** $\rightarrow$ **Falcon API** $\rightarrow$ **Service Layer** $\rightarrow$ **MongoDB Models** $\rightarrow$ **Storage**

| Layer | Description |
|:---|:---|
| **UI** | HTML templates, CSS, jQuery, AJAX |
| **API** | Falcon REST Resources |
| **Services** | Business logic & workflows |
| **Models** | PyMongo / MongoDB Abstraction |
| **Storage** | File system (Resumes) & MongoDB (Data) |

---

## 🛠 Technology Stack

### Backend
| Technology | Purpose |
|:---|:---|
| **Python 3.x** | Core language |
| **Falcon** | High-performance Web API Framework |
| **MongoDB** | NoSQL Database |
| **PyMongo** | Database Driver |

### Frontend
| Technology | Purpose |
|:---|:---|
| **HTML / CSS** | Structure and Styling |
| **jQuery** | DOM Manipulation |
| **AJAX** | Asynchronous API calls |
| **DataTables** | Tabular UI components |

### Testing & Utilities
| Utility | Purpose |
|:---|:---|
| **Postman** | API Endpoint Testing (CRUD) |
| **Resume Parser** | Extraction of candidate data |
| **SMTP** | Email notifications |

---

## 📁 Directory Structure

```text
HR-Recruitment-Application/
├── logs/                      # Application logs
├── uploaded_files/            # Local storage for uploads
│   ├── candidateprofiles/
│   ├── jd/
│   └── jobprofiles/
│
├── server/
│   ├── api/                   # Falcon Resources (API Endpoints)
│   ├── config/                # DB Config, Logging, Settings
│   ├── extraction/            # Resume parsing logic
│   ├── models/                # MongoDB Data Models
│   ├── services/              # Business logic
│   ├── ui/                    # HTML Templates & Static assets
│   └── __init__.py
│
├── sendmail.py                # Email utility
├── server.py                  # WSGI Application Entry Point
├── requirements.txt           # Dependencies
└── README.md
```

## 🚀 Installation

### Prerequisites

- Python 3.7+
- pip
- MongoDB (Running instance)
- Virtual environment (recommended)

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd HR-Recruitment-Application
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * **Linux / macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Database Setup:**
    Ensure your MongoDB instance is running. Configure the connection string in `server/config/settings.py` (or equivalent config file).

---

## ⚙ Configuration

Configuration files are located at `server/config/`.

| Area | Description |
|:---|:---|
| **Settings** | MongoDB URI, App ports, Environment config |
| **Middleware** | Falcon middleware for CORS & Auth |
| **Logging** | Log levels & formatting |
| **Errors** | Centralized error handling |

---

## ▶ Running the Application

1.  **Start the server:**
    ```bash
    python server.py
    ```

2.  **Access the application:**
    Open your browser and navigate to:
    ```
    http://localhost:PORT
    ```
    *(Note: The `PORT` is defined in `settings.py`. APIs can be tested via `http://localhost:PORT/api/...`)*

---

## 🔌 API Modules

### Core Domains

| Module | Responsibility |
|:---|:---|
| `candidate.py` | Candidate management |
| `applications.py` | Job applications |
| `jobs.py` | Job profiles |
| `prescreening.py` | Prescreen workflows |
| `scheduler.py` | Interview scheduling |
| `offers.py` | Offer management |
| `feedback.py` | Interview feedback |

### Master Data

- `skills.py`
- `educations.py`
- `city.py`, `state.py`, `country.py`
- `functionalorg.py`

---

## 🖥 UI Layer

UI templates and static assets are located at `server/ui/`.

**Screens Include:**
- Candidate management
- Job profiles
- Recruiter dashboards
- Interview scheduling
- Prescreening & feedback
- Offer management
- Resume & bulk uploads

---

## 📂 File Uploads & Logging

**File Storage:**
Uploaded files are stored locally in `uploaded_files/` using UUID-based naming to avoid collisions.
- `candidateprofiles/`
- `jd/`
- `jobprofiles/`

**Logging:**
Logs are written to `logs/` and configured via `server/config/applogging.py`.

---

## ✉ Email Service

Handled by `sendmail.py`.

**Used For:**
- Interview notifications
- Candidate communication
- Offer letters

---

## 🔐 Security & Validation

- **Input Validation:** Server-side checks using Falcon hooks/validators.
- **Client Validation:** jQuery/HTML5 form validation.
- **CORS:** Configured in middleware to allow cross-origin requests (useful for separate frontends).
- **File Integrity:** Validates file types and sizes during upload.

---

## ⚠ Known Limitations

- No role-based access control (RBAC)
- Local filesystem storage only (Resumes not stored in MongoDB GridFS)
- No external authentication provider
- Limited automated test coverage

---

## 🔮 Future Enhancements

- [ ] Role-based access control (RBAC)
- [ ] Migrate file storage to MongoDB GridFS or AWS S3
- [ ] JWT / OAuth authentication
- [ ] Resume–job matching intelligence
- [ ] Analytics & reporting dashboard
- [ ] Dockerized deployment

---

## 📜 License

**MIT License**

Copyright © 2026 Junaid-Techie

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND.

---

💡 Maintained by **Junaid-Techie**
