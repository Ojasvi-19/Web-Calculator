pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: env.BRANCH_NAME,
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Upgrade pip and install dependencies including PyInstaller
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Executable') {
            steps {
                // Build executable using PyInstaller
                bat 'pyinstaller --onefile --name WebCalculator main.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Make sure Docker is installed and added to PATH on the agent
                bat 'docker build -t web-calculator:%BUILD_NUMBER% .'
            }
        }

        stage('Run Unit Tests & Coverage') {
            steps {
                bat '''
                docker run --rm ^
                web-calculator:%BUILD_NUMBER% ^
                pytest tests ^
                --cov=calculator_ops ^
                --cov-report=term ^
                --cov-report=xml
                '''
            }
        }

        stage('Archive Executable') {
            steps {
                // Archive the built executable as a Jenkins artifact
                archiveArtifacts artifacts: 'dist\\WebCalculator*', fingerprint: true
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
