pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: env.BRANCH_NAME,
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''
                python --version
                python -m ensurepip --upgrade || true
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                python -m pip install pyinstaller

                '''
            }
        }

        stage('Build Binary using PyInstaller') {
            steps {
                sh '''
                pyinstaller --clean --onefile Calculator.py
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


