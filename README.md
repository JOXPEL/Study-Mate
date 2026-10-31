# StudyMate - AI-Powered E-Learning Platform

**StudyMate** is an intelligent full-stack e-learning web application built using **Django**, **PostgreSQL**, and **Google Gemini (Agentic AI)**. The platform features an automated study planner that analyzes student quiz performances and dynamically generates customized study schedules directly in the database.

---

## Key Features

- **Role-Based Access Control (RBAC):** Custom user model supporting `Student`, `Instructor`, and `Admin` roles with tailor-made dashboards.
- **Course & Content Management:** Structured modules, video lessons, and interactive multiple-choice quizzes.
- **Interactive Quiz Engine:** Tracks student attempts, calculates percentage scores, and logs performance history in PostgreSQL.
- **Agentic AI Assistant (Tool Calling):** An AI assistant powered by Google Gemini that inspects student performance via custom Python tools to create actionable `StudyPlan` records automatically.
- **Dynamic Dashboard:** Real-time visualization of upcoming study tasks and recent quiz performance.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.12+, Django 6.1 (MVT Architecture)
- **Database:** PostgreSQL
- **AI Integration:** Google Gemini 2.5 Flash (`google-genai` SDK)
- **Frontend:** Django Templates, HTML5, Bootstrap 5 (RTL)
- **Version Control & Environment:** Git, GitHub Desktop, `python-dotenv`

---

## System Architecture & AI Tool Calling
[ User Request ] ──► [ Gemini AI Agent ]
│
(Perceives Goal & Selects Tool)
│
▼
[ create_study_plan_tool() ]
│
┌───────────────────────┴───────────────────────┐
▼                                               ▼
[ Query QuizAttempt ]                       [ Insert StudyPlan ]
(Find weak modules <70%)                   (In PostgreSQL DB)

1. **User Prompt:** Student asks for a revision plan (e.g., *"Analyze my scores and make a study plan"*).
2. **AI Decision Loop:** Gemini detects the intent and triggers `create_study_plan_tool`.
3. **Database Side-Effect:** The tool queries `QuizAttempt` to identify weak modules (scores below 70%) and inserts a new `StudyPlan` with mapped `StudyPlanItem` records into PostgreSQL.
4. **User Response:** AI confirms plan creation with a summary of scheduled modules.

---

## Getting Started

### Prerequisites
- Python 3.12+ installed
- PostgreSQL database configured

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Study-Mate.git](https://github.com/Joxpel/Study-Mate.git)

Create and activate a virtual environment:

# On Windows
python -m venv venv
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt
Environment Variables (.env):
Create a .env file in the root directory and add your API key:
GEMINI_API_KEY=your_gemini_api_key_here
Apply Database Migrations:

python manage.py migrate
Run the Development Server:

python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.

 Project Structure
Plaintext
Study-Mate/
├── accounts/          # Custom User Model & RBAC Authentication
├── courses/           # Course & Module Management
├── quizzes/           # Quiz Engine & Performance Tracking
├── dashboard/         # Student Dashboard & Study Plans
├── ai_agent/          # Gemini Agentic AI & Tool Calling Functions
│   ├── tools.py       # Python DB Side-Effect Tools
│   └── services.py    # Gemini Agent Execution Logic
├── templates/         # Centralized HTML Templates
│   ├── base.html
│   ├── accounts/
│   ├── courses/
│   ├── dashboard/
│   └── quizzes/
├── config/            # Django Settings & Core URLs
├── .env               # Private Environment Keys (Git-ignored)
├── manage.py
└── README.md

 Graduation Project Context
Developed as part of the Information Technology Institute (ITI) Summer Training Program in Web Development & Generative AI.
