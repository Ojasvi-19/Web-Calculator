pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        PATH = "${env.HOME}/.local/bin:${env.PATH}" // ensures pip is found
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: env.BRANCH_NAME,
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Install pip & Dependencies') {
            steps {
                // Install pip locally and upgrade it
                sh '${PYTHON} -m ensurepip --upgrade --user'
                sh '${PYTHON} -m pip install --upgrade --user pip'
                
                // Install project dependencies and PyInstaller
                sh '${PYTHON} -m pip install --user -r Requirements.txt'
                sh '${PYTHON} -m pip install --user pyinstaller'
            }
        }

        stage('Build Executable') {
            steps {
                // Build Linux executable using PyInstaller
                sh 'pyinstaller --onefile --name WebCalculator Calculator.py'
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

        stage('Archive Executable') {
            steps {
                archiveArtifacts artifacts: 'dist/WebCalculator*', fingerprint: true
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

