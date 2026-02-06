\section{HR Recruitment Application}

\subsection{Overview}

The \textbf{HR Recruitment Application} is a full-stack recruitment management system built with Python.  
It streamlines the complete hiring lifecycle including candidate management, job profiles, resume uploads, interview scheduling, prescreening, feedback, and offer management through a modular backend and a server-rendered web UI.

\hrulefill

\subsection{Features}

\begin{itemize}
  \item Candidate lifecycle management
  \item Job profile creation and maintenance
  \item Resume and job description uploads
  \item Bulk resume upload
  \item Recruiter and interviewer assignment
  \item Interview scheduling
  \item Prescreening workflows
  \item Feedback and offer management
  \item Skill, education, and location master data
  \item Email notifications
  \item Centralized logging
\end{itemize}

\hrulefill

\subsection{Architecture}

\[
\text{UI} \rightarrow \text{API Layer} \rightarrow \text{Service Layer} \rightarrow \text{Models} \rightarrow \text{Storage}
\]

\hrulefill

\subsection{Technology Stack}

\subsubsection{Backend}

\begin{itemize}
  \item Python 3.x
  \item Flask (or Flask-compatible framework)
  \item REST-style APIs
\end{itemize}

\subsubsection{Frontend}

\begin{itemize}
  \item HTML (Jinja templates)
  \item CSS
  \item JavaScript
  \item jQuery
  \item DataTables
\end{itemize}

\subsubsection{Utilities}

\begin{itemize}
  \item Resume parsing and extraction
  \item SMTP-based email service
  \item Application logging
\end{itemize}

\hrulefill

\subsection{Directory Structure}

\begin{verbatim}
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
\end{verbatim}



\section{Installation}

\subsection{Prerequisites}

\[
\text{Python} \ge 3.7
\]

\subsection{Clone Repository}

\begin{verbatim}
git clone <repository-url>
cd HR-Recruitment-Application
\end{verbatim}

\subsection{Create Virtual Environment}

\begin{verbatim}
python -m venv venv
\end{verbatim}

\subsection{Activate Virtual Environment}

\textbf{Linux / macOS}
\begin{verbatim}
source venv/bin/activate
\end{verbatim}

\textbf{Windows}
\begin{verbatim}
venv\Scripts\activate
\end{verbatim}

\subsection{Install Dependencies}

\begin{verbatim}
pip install -r requirements.txt
\end{verbatim}

---

\section{Configuration}

Configuration files are located at:

\begin{verbatim}
server/config/
\end{verbatim}

\subsection{Key Configuration Areas}

\begin{itemize}
  \item Application settings
  \item Middleware and hooks
  \item CORS handling
  \item Logging configuration
  \item Error handling
\end{itemize}

---

\section{Running the Application}

\begin{verbatim}
python server.py
\end{verbatim}

\[
\text{Application URL: http://localhost:PORT}
\]

The port is defined in \texttt{settings.py}.

---

\section{API Modules}

\subsection{Candidate and Applications}
\begin{itemize}
  \item \texttt{candidate.py}
  \item \texttt{applications.py}
\end{itemize}

\subsection{Job and Hiring Workflow}
\begin{itemize}
  \item \texttt{jobs.py}
  \item \texttt{prescreening.py}
  \item \texttt{scheduler.py}
  \item \texttt{offers.py}
  \item \texttt{feedback.py}
\end{itemize}

\subsection{Recruiter Management}
\begin{itemize}
  \item \texttt{recruiter.py}
\end{itemize}

\subsection{Master Data}
\begin{itemize}
  \item \texttt{skills.py}
  \item \texttt{educations.py}
  \item \texttt{city.py}
  \item \texttt{state.py}
  \item \texttt{country.py}
  \item \texttt{functionalorg.py}
\end{itemize}

---

\section{UI Layer}

UI templates and static assets are located at:

\begin{verbatim}
server/ui/
\end{verbatim}

\subsection{Includes}

\begin{itemize}
  \item Candidate management screens
  \item Job profile management
  \item Recruiter dashboards
  \item Interview scheduling
  \item Prescreening and feedback
  \item Offer management
  \item Resume upload and bulk upload
\end{itemize}

---

\section{File Uploads}

Uploaded files are stored locally at:

\begin{verbatim}
uploaded_files/
├── candidateprofiles/
├── jd/
└── jobprofiles/
\end{verbatim}

Files are stored using UUID-based naming to avoid collisions.

---

\section{Logging}

Application logs are written to:

\begin{verbatim}
logs/
\end{verbatim}

Logging configuration is defined in:

\begin{verbatim}
server/config/applogging.py
\end{verbatim}

---

\section{Email Service}

Email notifications are handled using:

\begin{verbatim}
sendmail.py
\end{verbatim}

\subsection{Used For}

\begin{itemize}
  \item Interview notifications
  \item Candidate communication
  \item Offer letters
\end{itemize}

---

\section{Security and Validation}

\begin{itemize}
  \item Server-side validation
  \item Client-side form validation
  \item CORS handling via middleware
  \item File type and size validation
\end{itemize}

---

\section{Known Limitations}

\begin{itemize}
  \item No role-based access control (RBAC)
  \item Local filesystem storage only
  \item No external authentication provider
  \item Limited automated test coverage
\end{itemize}

---

\section{Future Enhancements}

\begin{itemize}
  \item Role-based access control
  \item Cloud storage integration
  \item JWT / OAuth authentication
  \item Resume--job matching intelligence
  \item Analytics and reporting
  \item Dockerized deployment
\end{itemize}

---

\section{License}

This project is intended for internal or educational use.  
Add a \texttt{LICENSE} file for public distribution.

