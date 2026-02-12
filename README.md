# DevOps CI/CD Exercise - Lesson 47

> **Student:** Ayal Mauda  
> **GitHub:** [ayalmauda-ai/Devops-ci-cd-exercise](https://github.com/ayalmauda-ai/Devops-ci-cd-exercise)  
> **Docker Hub:** [ayalm/devops-testing-app](https://hub.docker.com/r/ayalm/devops-testing-app)  
> **Final Version:** `1.0.25` ✅

A complete CI/CD pipeline built with **Jenkins**, **Docker**, **Jira**, and **Email notifications** — deploying a Flask testing application with automated quality checks.

---

## 📐 Architecture Overview

### System Flow
┌──────────────┐
│ Developer │
│ (VS Code) │
└──────┬───────┘
│ git push
▼
┌──────────────┐
│ GitHub │
│ Repository │
└──────┬───────┘
│ webhook
▼
┌──────────────┐
│ Jenkins │
│ CI Server │
└──────┬───────┘
│ build & test
▼
┌──────────────┐
│ Docker Hub │
│ (ayalm/...) │
└──────┬───────┘
│
├─ ✅ Success ──→ Email
│
└─ ❌ Failure ──→ Jira + Email


### Pipeline Stages

| Order | Stage | Action | Duration |
|-------|-------|--------|----------|
| 1️⃣ | **Checkout** | Clone code from GitHub | ~3s |
| 2️⃣ | **Setup Environment** | Create Python venv + dependencies | ~25s |
| 3️⃣ | **Lint Code** | flake8 + pylint analysis | ~8s |
| 4️⃣ | **Unit Tests** | pytest with coverage | ~12s |
| 5️⃣ | **Integration Tests** | API endpoint testing | ~15s |
| 6️⃣ | **E2E Tests** | Selenium + Chrome (Comet) | ~50s |
| 7️⃣ | **Security Scan** | Bandit security check | ~5s |
| 8️⃣ | **Build Docker** | Create versioned image | ~1m 38s |
| 9️⃣ | **Push to Hub** | Upload to Docker Hub | ~30s |
| 🔔 | **Notify** | Email + Jira (on failure) | ~5s |

---

## 🏗️ Project Structure

devops-ci-cd-exercise/
│
├── 📁 app/ # Flask Application
│ ├── init.py # App factory
│ ├── routes/
│ │ ├── user_routes.py # User API endpoints
│ │ └── product_routes.py # Product API endpoints
│ └── templates/
│ └── index.html # Web UI
│
├── 📁 tests/ # Test Suite
│ ├── unit/ # Unit tests
│ ├── integration/ # API integration tests
│ ├── e2e/ # Selenium browser tests
│ └── performance/ # Locust load tests
│
├── 📁 docker/
│ └── Dockerfile # Container definition
│
├── 📁 docs/
│ └── images/ # Screenshots
│ ├── build-25-success.png
│ └── build-22-failure.png
│
├── 📄 Jenkinsfile # CI/CD pipeline
├── 📄 requirements.txt # Python dependencies
├── 📄 pytest.ini # Test configuration
├── 📄 main.py # App entry point
└── 📄 README.md # This file

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
| Feature            | Description                           |
| ------------------ | ------------------------------------- |
| Base Image         | Python 3.9 slim (lightweight)         |
| Chrome Integration | Chromium + ChromeDriver pre-installed |
| Health Check       | Built-in monitoring endpoint          |
| Size               | ~856 MB (optimized)                   |


⚙️ Task 2: Jenkins Pipeline Enhancement
A. Testing Phase
1. Chrome Browser Integration ("Comet")
All E2E tests run on Chrome (Chromium) in headless mode:

# tests/e2e/test_web_interface.py
chrome_options = Options()
chrome_options.add_argument("--headless")           # No GUI
chrome_options.add_argument("--no-sandbox")         # Docker compatibility
chrome_options.add_argument("--disable-dev-shm-usage")  # Memory optimization

driver = webdriver.Chrome(service=service, options=chrome_options)


Test Coverage:

✅ 9 UI interaction tests

✅ Button clicks and API calls

✅ Responsive design validation

✅ JSON response verification


2. Code Coverage Reports
Generated automatically to htmlcov/ directory:

Format: HTML + XML

Overall Coverage: 63%

Jenkins Integration: Published as "Unit Test Coverage Report"

Viewable: Directly in Jenkins UI with trend graphs


B. Build & Artifact Creation
Version Management
Format: {MAJOR}.{MINOR}.{BUILD_NUMBER}
Example: 1.0.25

| Component | Value | Description      | When to Change                |
| --------- | ----- | ---------------- | ----------------------------- |
| MAJOR     | 1     | Breaking changes | API changes, major features   |
| MINOR     | 0     | New features     | Backward-compatible additions |
| BUILD     | 25    | Build number     | Auto-incremented by Jenkins   |

Docker Build & Push Process
# 1. Build image
docker build -t devops-testing-app:1.0.25 -f docker/Dockerfile .

# 2. Tag for Docker Hub
docker tag devops-testing-app:1.0.25 ayalm/devops-testing-app:1.0.25
docker tag devops-testing-app:1.0.25 ayalm/devops-testing-app:latest

# 3. Push to registry
docker push ayalm/devops-testing-app:1.0.25
docker push ayalm/devops-testing-app:latest

Result:

✅ Image available at: hub.docker.com/r/ayalm/devops-testing-app

✅ Tags: 1.0.25, latest

✅ Platform: linux/amd64


C. Failure Handling
1. Jira Integration
Configuration:

Jira Instance: eyal222222-1770656009249.atlassian.net

Project: KAN (Kanban board)

Trigger: Automatic ticket creation on pipeline failure

Issue Type: Bug

Example Ticket:
Summary: Build Failure: DevOps-Exercise-47 - #22

Description:
Build failed in Jenkins.

Build Number: 22
Branch: main
Status: FAILURE
Failed Stage: End-to-End Tests
Build URL: http://localhost:8080/job/DevOps-Exercise-47/22/


2. Email Notifications
Configuration:

Provider: Gmail SMTP (smtp.gmail.com:465)

Authentication: App Password

Recipient: eyal222222@gmail.com

Format: HTML with full build details

Email Template:
Subject: ❌ Pipeline Failure: DevOps-Exercise-47 - #22

The pipeline failed!

Build Details:
-  Build Number: 22
-  Branch: main
-  Failed Stage: End-to-End Tests
-  Duration: 23 seconds

View Build: http://localhost:8080/job/DevOps-Exercise-47/22/


D. Test Reports Integration
Jenkins UI Features:
| Feature          | Description                                            |
| ---------------- | ------------------------------------------------------ |
| JUnit Reports    | Published for all test stages (Unit, Integration, E2E) |
| Coverage Reports | HTML reports archived and viewable in Jenkins          |
| Trend Graphs     | Historical pass/fail visualization                     |
| Artifacts        | All reports archived: reports/*.xml, htmlcov/**/*      |
| Test Details     | Individual test case results with failure messages     |


📸 Task 3: Pipeline Execution Screenshots
✅ Successful Build - #25
Build 25 Success
Build Summary:

Status: ✅ SUCCESS

Started: 13 hours ago

Duration: ~2 minutes 26 seconds

Version Created: 1.0.25

Docker Image: Successfully pushed to Docker Hub

Stage Results:

✅ Checkout SCM           (3s)
✅ Setup Environment      (25s)
✅ Lint Code             (8s)
✅ Unit Tests            (12s)
✅ Integration Tests     (15s)
✅ End-to-End Tests      (50s)
⚠️  Performance Tests     (Skipped - not production)
✅ Security Scan         (5s)
✅ Build Docker Image    (1m 38s)
⚠️  Deploy to Staging     (Skipped - not develop branch)
✅ Post Actions          (1s)


Key Achievements:

✅ All 9 E2E tests passed on Chrome

✅ Integration tests passed (user persistence fixed)

✅ Docker image built and pushed successfully

✅ Version 1.0.25 now available on Docker Hub


❌ Failed Build - #22
Build 22 Failure

Build Summary:

Status: ❌ FAILURE

Failed Stage: End-to-End Tests

Duration: 23 seconds (stopped at failure)

Error Type: Assertion Error

Root Cause:

# Test: test_button_interactions
# Error: assert 5 >= 6
#   where 5 = len([<WebElement>, <WebElement>, ...])

# The test expected 6 buttons, but the page only contained 5


Resolution Steps:

✅ Identified the issue in test expectations

✅ Updated test to match actual button count

✅ Fixed in Build #23

Automated Actions Taken:

✅ Jira ticket automatically created (KAN-8)

✅ Email notification sent to eyal222222@gmail.com

✅ Jenkins workspace cleaned

✅ Build artifacts archived


🔄 Build Evolution

| Build | Status | Key Event                  | Lesson Learned                          |
| ----- | ------ | -------------------------- | --------------------------------------- |
| #5    | ❌      | Integration test failure   | Fixed user database persistence bug     |
| #20   | ❌      | Firefox driver not found   | Switched to Chrome (Comet browser)      |
| #21   | ❌      | ChromeDriver path issue    | Fixed ChromeDriver path detection       |
| #22   | ❌      | Button count assertion     | Updated test expectations               |
| #23   | ✅      | First all-green test suite | All tests passing, Docker skipped       |
| #24   | ❌      | Docker permission error    | Fixed Jenkins Docker socket permissions |
| #25   | ✅      | Complete success           | First Docker Hub push + full pipeline   |


🚦 Quick Start
1. Run Application Locally
# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run app
python main.py

# App available at: http://localhost:5000


2. Run with Docker

# Build image
docker build -t devops-testing-app -f docker/Dockerfile .

# Run container
docker run -p 5000:5000 devops-testing-app

# App available at: http://localhost:5000


3. Pull from Docker Hub

# Pull latest image
docker pull ayalm/devops-testing-app:latest

# Or specific version
docker pull ayalm/devops-testing-app:1.0.25

# Run
docker run -p 5000:5000 ayalm/devops-testing-app:latest


🌐 API Endpoints

| Method | Endpoint           | Description        | Example                  |
| ------ | ------------------ | ------------------ | ------------------------ |
| GET    | /                  | Web UI (HTML page) | -                        |
| GET    | /health            | Health check       | {"status": "healthy"}    |
| GET    | /api/users/        | List all users     | [{id, name, email}, ...] |
| GET    | /api/users/<id>    | Get user by ID     | {id: 1, name: "John"}    |
| POST   | /api/users/        | Create new user    | Body: {name, email}      |
| GET    | /api/products/     | List all products  | [{id, name, price}, ...] |
| GET    | /api/products/<id> | Get product by ID  | {id: 1, name: "Laptop"}  |


🎓 Key Learnings
1. Browser Testing Configuration
Challenge: Initial setup used Firefox (GeckoDriver), but we needed Chrome.
Solution: Configured Chrome in headless mode with proper Docker compatibility flags.


chrome_options.add_argument("--no-sandbox")         # Docker requirement
chrome_options.add_argument("--disable-dev-shm-usage")  # Memory fix

2. State Management in Flask
Challenge: Integration tests failing because user data wasn't persisting.
Solution: Moved users_db dictionary to global scope instead of recreating it
