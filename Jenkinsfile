pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: env.BRANCH_NAME,
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Build Binary using PyInstaller (Docker)') {
            steps {
                sh '''
                docker run --rm \
                -v $(pwd):/web-calculator \
                -w /web-calculator \
                python:3.9-slim \
                sh -c "
                pip install --upgrade pip &&
                pip install -r Requirements.txt &&
                pip install pyinstaller &&
                pyinstaller --clean --onefile Calculator.py
                "
                '''
            }
        }

        stage('Archive PyInstaller Artifact') {
            steps {
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
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
                --cov=calculator_ops \
                --cov-report=term \
                --cov-report=xml
                '''
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


