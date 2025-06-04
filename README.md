# PostaHub - SMTP Warm-up & AI Email Interaction System

PostaHub is an AI-powered, modular system that automates SMTP warm-up processes and simulates inbox interactions using real Gmail sessions. It improves email deliverability, monitors engagement, and allows users to manage strategies through a modern dashboard.

## 🚀 Features

- 🔐 SMTP account onboarding and validation
- 🧠 AI-generated personalized email content (LLM via Hugging Face)
- 📩 Scheduled warm-up emails via Celery tasks
- 🤖 Inbox bot (Puppeteer + Dolphin Anty) simulates open/reply actions
- 📊 Admin & user dashboard (React + TailwindCSS)
- 🗂️ Fully loggable: email_logs, engagement_logs, warmup_targets
- 🐳 Docker-based setup for local testing

---

## 🛠️ Technologies Used

- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Alembic
- **Task Queue:** Celery + Redis
- **Database:** PostgreSQL
- **Frontend:** Next.js 14, React, TailwindCSS, ShadCN UI
- **AI Model:** Hugging Face Transformers (LLaMA-3 or Mistral-7B)
- **Inbox Bot:** Puppeteer, Node.js, Dolphin Anty API
- **DevOps:** Docker, dotenv

---

## ⚙️ Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/aliyuksal/postahub-backend.git
cd smtp-warming



2. Python environment

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


3. Environment setup
cp .env.example .env
# then edit the .env file with your credentials


4. Apply migrations
alembic upgrade head


5. Start backend API
uvicorn apps.api_server.main:app --reload

6. Run Celery worker
celery -A apps.warming_engine.scheduler.celery_app worker --loglevel=info

7. (Optional) Start Puppeteer inbox bot
cd inbox_bot
node puppeteer_controller.js

📁 Project Structure
smtp-warming/
├── apps/
│   ├── api_server/         # FastAPI endpoints
│   ├── warming_engine/     # Celery scheduled tasks
│   └── inbox_bot/          # Puppeteer interaction bot
├── shared/                 # Common configs & prompts
├── data/                   # Sample SMTP inputs
├── docker/                 # Docker setup
├── README.md
├── requirements.txt
└── .env.example


