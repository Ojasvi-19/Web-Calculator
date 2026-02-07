pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Verify Workspace') {
            steps {
                sh '''
                echo "Workspace path:"
                pwd
                echo "Workspace contents:"
                ls -R
                '''
            }
        }

        stage('Build Executable with PyInstaller') {
            steps {
                sh '''
                docker run --rm \
                  -v "$WORKSPACE:/app" \
                  -w /app \
                  python:3.10-slim sh -c "
                    apt-get update &&
                    apt-get install -y binutils &&
                    pip install --no-cache-dir pyinstaller &&
                    pyinstaller --onefile Calculator.py
                  "
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t web-calculator:${BUILD_NUMBER} .'
            }
        }

        stage('Run Unit Tests & Coverage') {
            steps {
                sh '''
                docker run --rm \
                  web-calculator:${BUILD_NUMBER} \
                  pytest tests \
                  --cov=Calculator_ops \
                  --cov-report=term \
                  --cov-report=xml
                '''
            }
        }

        stage('Archive Executable') {
            steps {
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }
    }

    post {
        success {
            echo "Pipeline executed successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}







