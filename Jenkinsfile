pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3'
        VENV_DIR = 'venv'
        // Task: Version Management (Major.Minor)
        MAJOR_VERSION = '1'
        MINOR_VERSION = '0'
        FULL_VERSION = "${MAJOR_VERSION}.${MINOR_VERSION}.${env.BUILD_NUMBER}"
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    sh 'echo "Setting up Python environment"'
                    
                    sh "python${PYTHON_VERSION} -m venv ${VENV_DIR}"
                    sh ". ${VENV_DIR}/bin/activate && pip install --upgrade pip"
                    sh ". ${VENV_DIR}/bin/activate && pip install -r requirements.txt"
                }
            }
        }
        
        stage('Lint Code') {
            steps {
                script {
                    sh ". ${VENV_DIR}/bin/activate && flake8 app/ --output-file=reports/flake8.txt || true"
                    sh ". ${VENV_DIR}/bin/activate && pylint app/ --output=reports/pylint.txt || true"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/*.txt', allowEmptyArchive: true
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                script {
                    sh 'mkdir -p reports'
                    // Task: Generate code coverage reports to htmlcov/
                    sh ". ${VENV_DIR}/bin/activate && pytest tests/unit/ -v --cov=app --cov-report=xml --cov-report=html --junit-xml=reports/unit-tests.xml"
                }
            }
            post {
                always {
                    junit 'reports/unit-tests.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Unit Test Coverage Report'
                    ])
                    archiveArtifacts artifacts: 'htmlcov/**/*', allowEmptyArchive: false
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                script {
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                        sh ". ${VENV_DIR}/bin/activate && pytest tests/integration/ -v --junit-xml=reports/integration-tests.xml"
                    }
                }
            }
            post {
                always {
                    junit 'reports/integration-tests.xml'
                }
            }
        }
        
        stage('End-to-End Tests') {
            steps {
                script {
                    // Task: Run tests on "Comet" (Chrome). 
                    // (Assuming you updated tests/e2e/test_web_interface.py to use Chrome)
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        export DISPLAY=:99
                        Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &
                        sleep 3
                        pytest tests/e2e/ -v --junit-xml=reports/e2e-tests.xml
                        killall Xvfb || true
                    '''
                }
            }
            post {
                always {
                    junit 'reports/e2e-tests.xml'
                }
            }
        }
        
        stage('Performance Tests') {
            // Task: Skip performance tests except in production environment
            when {
                branch 'main'
            }
            steps {
                script {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        
                        python main.py &
                        APP_PID=$!
                        sleep 5
                        
                        locust -f tests/performance/locustfile.py \\
                            --headless \\
                            --users 10 \\
                            --spawn-rate 2 \\
                            --run-time 10s \\
                            --host http://localhost:5000 \\
                            --html reports/performance-report.html
                        
                        kill $APP_PID || true
                    '''
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'reports',
                        reportFiles: 'performance-report.html',
                        reportName: 'Performance Test Report'
                    ])
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                script {
                    sh ". ${VENV_DIR}/bin/activate && bandit -r app/ -f json -o reports/bandit-report.json || true"
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/bandit-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                script {
                    echo "Building Version: ${FULL_VERSION}"
                    // Task: Create version tag and build Docker image
                    sh """
                        docker build -t devops-testing-app:${FULL_VERSION} -f docker/Dockerfile .
                        docker tag devops-testing-app:${FULL_VERSION} devops-testing-app:latest
                    """
                    // Note: 'docker push' commands would go here if you had credentials
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    // Task: Deploy to AWS staging (Simulated here with Docker)
                    sh """
                        echo "Deploying to staging environment (Version ${FULL_VERSION})"
                        docker stop staging-app || true
                        docker rm staging-app || true
                        docker run -d --name staging-app -p 5001:5000 devops-testing-app:${FULL_VERSION}
                        
                        sleep 5
                        curl -f http://localhost:5001/health || exit 1
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            script {
                sh 'echo "Pipeline completed successfully!"'
                emailext (
                    subject: "✅ Pipeline Success: ${env.JOB_NAME} - ${FULL_VERSION}",
                    body: """
                        <p>The pipeline completed successfully!</p>
                        <ul>
                            <li><strong>Version:</strong> ${FULL_VERSION}</li>
                            <li><strong>Branch:</strong> ${env.BRANCH_NAME}</li>
                            <li><strong>Duration:</strong> ${currentBuild.durationString}</li>
                            <li><strong>Reports:</strong> Check the artifacts section</li>
                        </ul>
                        <p><a href="${env.BUILD_URL}">View Build Details</a></p>
                    """,
                    to: "${env.CHANGE_AUTHOR_EMAIL}"
                )
            }
        }
        failure {
            script {
                echo "Pipeline failed! Sending alerts..."
                
                // 1. Send Email
                emailext (
                    subject: "❌ FAILED: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                    body: """<p>Build Failed!</p>
                             <p><strong>Stage:</strong> ${currentBuild.currentResult}</p>
                             <p>Check console: ${env.BUILD_URL}</p>""",
                    to: "eyal222222@gmail.com"
                )

                // 2. Create Jira Ticket
                def errorMsg = "Build #${env.BUILD_NUMBER} failed for ${env.JOB_NAME}. Please investigate."
                
                try {
                    def newIssue = jiraNewIssue(
                        site: 'my-jira',
                        issue: [
                            fields: [
                                project: [key: 'KAN'],
                                summary: "Build Failure: Build #${env.BUILD_NUMBER}",
                                description: errorMsg,
                                issuetype: [name: 'Bug']
                            ]
                        ]
                    )
                    echo "Created Jira Issue: ${newIssue.data.key}"
                } catch (e) {
                    echo "Could not create Jira ticket: ${e.getMessage()}"
                }
            }
        }
    }
}
