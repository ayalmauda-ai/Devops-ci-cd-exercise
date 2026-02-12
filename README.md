# DevOps CI/CD Exercise - Lesson 47

> **Student:** Ayal Mauda  
> **GitHub:** [ayalmauda-ai/Devops-ci-cd-exercise](https://github.com/ayalmauda-ai/Devops-ci-cd-exercise)  
> **Docker Hub:** [ayalm/devops-testing-app](https://hub.docker.com/r/ayalm/devops-testing-app)  
> **Final Version:** `1.0.25` ✅

A complete CI/CD pipeline built with **Jenkins**, **Docker**, **Jira**, and **Email notifications** — deploying a Flask testing application with automated quality checks.

---

## 📐 Architecture Overview

Developer → GitHub → Jenkins CI → Docker Hub → Notifications
│ │ │ │ │
Code Webhook Build & Image Jira + Email
Push Trigger Test All Storage Alerts

text

### Pipeline Flow

┌──────────────┐
│ Checkout │ Clone code from GitHub
└──────┬───────┘
▼
┌──────────────┐
│ Setup Python │ Create venv + install dependencies
└──────┬───────┘
▼
┌──────────────┐
│ Lint Code │ flake8 + pylint
└──────┬───────┘
▼
┌──────────────┐
│ Unit Tests │ pytest + coverage reports
└──────┬───────┘
▼
┌──────────────┐
│ Integration │ API endpoint testing
│ Tests │
└──────┬───────┘
▼
┌──────────────┐
│ E2E Tests │ Selenium + Chrome (Comet browser)
└──────┬───────┘
▼
┌──────────────┐
│ Security │ Bandit security scanner
│ Scan │
└──────┬───────┘
▼
┌──────────────┐
│ Build Docker │ Build versioned image (1.0.25)
│ Image │
└──────┬───────┘
▼
┌──────────────┐
│ Push to Hub │ ayalm/devops-testing-app:1.0.25
└──────────────┘
│
├─ Success ──→ Email ✅
│
└─ Failure ──→ Email + Jira Ticket ❌

text

---

## 🏗️ Project Structure

.
├── app/ # Flask Application
│ ├── init.py
│ ├── routes/
│ │ ├── user_routes.py
│ │ └── product_routes.py
│ └── templates/
│ └── index.html
│
├── tests/ # Test Suite
│ ├── unit/ # Unit tests
│ ├── integration/ # API tests
│ ├── e2e/ # Selenium tests
│ └── performance/ # Locust load tests
│
├── docker/
│ └── Dockerfile # Application container
│
├── Jenkinsfile # CI/CD pipeline definition
├── requirements.txt # Python dependencies
└── README.md # This file

text

---

## 🔧 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Application** | Python 3.13, Flask | REST API + Web UI |
| **CI/CD Engine** | Jenkins 2.x | Pipeline orchestration |
| **Containerization** | Docker | App packaging |
| **Registry** | Docker Hub | Image storage |
| **Testing** | pytest, Selenium, Locust | Unit/Integration/E2E/Performance |
| **Security** | Bandit | Static security analysis |
| **Linting** | Flake8, Pylint | Code quality |
| **Notifications** | Gmail SMTP, Jira API | Failure alerts |
| **Version Control** | Git, GitHub | Source management |

---

## 🚀 CI/CD Pipeline Stages

### Stage Overview

| # | Stage | Description | Duration | Status |
|---|-------|-------------|----------|--------|
| 1 | **Checkout SCM** | Pull code from GitHub | ~3s | ✅ |
| 2 | **Setup Environment** | Python venv + dependencies | ~25s | ✅ |
| 3 | **Lint Code** | flake8 + pylint | ~8s | ✅ |
| 4 | **Unit Tests** | pytest + coverage (63%) | ~12s | ✅ |
| 5 | **Integration Tests** | API endpoint testing | ~15s | ✅ |
| 6 | **End-to-End Tests** | Selenium Chrome tests (9 tests) | ~50s | ✅ |
| 7 | **Performance Tests** | Locust (production only) | - | ⚠️ Skipped |
| 8 | **Security Scan** | Bandit | ~5s | ✅ |
| 9 | **Build Docker Image** | Build + tag version | ~1m 38s | ✅ |
| 10 | **Deploy to Staging** | Conditional deployment | - | ⚠️ Skipped |

---

## 📦 Task 1: Docker Setup

### Dockerfile (`docker/Dockerfile`)

```dockerfile
FROM python:3.9-slim

# Install system dependencies + Chrome for E2E tests
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "main.py"]
Key Features
✅ Base Image: Python 3.9 slim (lightweight)

✅ Chrome Integration: Chromium + ChromeDriver pre-installed

✅ Health Check: Built-in monitoring

✅ Size: ~856 MB (optimized)

⚙️ Task 2: Jenkins Pipeline Enhancement
A. Testing Phase
1. Chrome Browser Integration ("Comet")
All E2E tests run on Chrome (Chromium) in headless mode:

python
# tests/e2e/test_web_interface.py
chrome_options = Options()
chrome_options.add_argument("--headless")           # No GUI
chrome_options.add_argument("--no-sandbox")         # Docker compatibility
chrome_options.add_argument("--disable-dev-shm-usage")  # Memory optimization

driver = webdriver.Chrome(service=service, options=chrome_options)
Tests: 9 UI interaction tests
Coverage: Button clicks, API calls, responsive design

2. Code Coverage Reports
Generated automatically to htmlcov/ directory:

Format: HTML + XML

Overall Coverage: 63%

Jenkins Integration: Published as "Unit Test Coverage Report"

B. Build & Artifact Creation
Version Management
text
Format: {MAJOR}.{MINOR}.{BUILD_NUMBER}
Example: 1.0.25
Component	Value	Description
MAJOR	1	Breaking changes
MINOR	0	New features
BUILD	25	Jenkins build number (auto-increment)
Docker Build & Push
bash
# Build
docker build -t devops-testing-app:1.0.25 -f docker/Dockerfile .

# Tag for Docker Hub
docker tag devops-testing-app:1.0.25 ayalm/devops-testing-app:1.0.25
docker tag devops-testing-app:1.0.25 ayalm/devops-testing-app:latest

# Push to registry
docker push ayalm/devops-testing-app:1.0.25
docker push ayalm/devops-testing-app:latest
Docker Hub: hub.docker.com/r/ayalm/devops-testing-app

C. Failure Handling
1. Jira Integration ✅
Project: KAN

Trigger: Automatic ticket creation on pipeline failure

Issue Type: Bug

Example Ticket:

text
Summary: Build Failure: DevOps-Exercise-47 - #22

Description:
Build failed in Jenkins.
Build Number: 22
Branch: main
Status: FAILURE
Failed Stage: End-to-End Tests
Build URL: http://localhost:8080/job/DevOps-Exercise-47/22/
2. Email Notifications ✅
Provider: Gmail SMTP (smtp.gmail.com:465)

Recipient: eyal222222@gmail.com

Format: HTML with build details

Email Template:

text
Subject: ❌ Pipeline Failure: DevOps-Exercise-47 - #22

The pipeline failed!
-  Build: 22
-  Branch: main
-  Failed Stage: End-to-End Tests
-  View Build: http://localhost:8080/job/DevOps-Exercise-47/22/
D. Test Reports Integration
✅ JUnit Reports: Published for all test stages

✅ Coverage Reports: HTML reports archived and viewable in Jenkins UI

✅ Trend Graphs: Historical pass/fail visualization

✅ Artifacts: All reports archived for each build

📸 Task 3: Pipeline Execution Screenshots
✅ Successful Build - #25
Build 25 Success

Details:

Status: ✅ SUCCESS

Duration: 13 hours ago

Version: 1.0.25

Docker Image: Pushed to Docker Hub

All Stages: Green checkmarks

Key Achievements:

All 9 E2E tests passed on Chrome

Integration tests passed (user persistence fixed)

Docker image successfully built and pushed

Version 1.0.25 now available on Docker Hub

❌ Failed Build - #22
Build 22 Failure

Details:

Status: ❌ FAILURE

Failed Stage: End-to-End Tests

Duration: 23 seconds (before failure)

Error: test_button_interactions failed

Root Cause:

python
# Test expected 6 buttons, but page only had 5
assert 5 >= 6  # AssertionError
Resolution:
Fixed test assertion to match actual button count (5 buttons):

python
# Changed from:
assert len(buttons) >= 6

# To:
assert len(buttons) >= 5
Actions Taken:

✅ Jira ticket automatically created (KAN-8)

✅ Email notification sent

✅ Jenkins workspace cleaned

✅ Fixed in Build #23

🔄 Build Evolution
Build	Status	Key Event
#5	❌	Integration test failure (user DB bug)
#20	❌	Firefox driver not found
#21	❌	ChromeDriver path issue
#22	❌	Button count assertion
#23	✅	First all-green test suite
#24	❌	Docker permission error
#25	✅	First complete success with Docker push
🚦 Quick Start
1. Run Locally
bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
python main.py
# App available at http://localhost:5000
2. Run with Docker
bash
# Build
docker build -t devops-testing-app -f docker/Dockerfile .

# Run
docker run -p 5000:5000 devops-testing-app
# App available at http://localhost:5000
3. API Endpoints
Method	Endpoint	Description
GET	/	Web UI
GET	/health	Health check
GET	/api/users/	List all users
GET	/api/users/<id>	Get user by ID
POST	/api/users/	Create user
GET	/api/products/	List products
🎓 Key Learnings
1. Browser Testing
Switched from Firefox to Chrome (Comet browser)

Configured headless mode for Docker environment

Fixed ChromeDriver path detection issues

2. State Management
Moved database to global scope for persistence

Fixed integration tests by maintaining state between requests

3. Docker Permissions
Solved Docker socket permissions by restarting Jenkins with proper groups

Enabled Jenkins to build and push images

4. CI/CD Best Practices
Implemented version tagging (Major.Minor.Build)

Set up automatic failure notifications

Created comprehensive test coverage reports
