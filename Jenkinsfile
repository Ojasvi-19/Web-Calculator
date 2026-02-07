pipeline {
    agent any

    environment {
        PYTHON = 'python3' // change to 'python' if using Windows
    }

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
                sh "${env.PYTHON} -m pip install --upgrade pip"
                sh "${env.PYTHON} -m pip install -r Requirements.txt"
            }
        }

        stage('Build Executable') {
            steps {
                // Build executable using PyInstaller
                sh "pyinstaller --onefile --name WebCalculator Calculator.py"
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
                // Save the built executable as a Jenkins artifact
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
