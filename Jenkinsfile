pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: env.BRANCH_NAME,
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Setup Python & PyInstaller') {
            steps {
                dir('Web-Calculator') {
                    bat '''
                    REM Download get-pip.py if pip not installed
                    IF NOT EXIST get-pip.py (
                        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
                    )

                    REM Install pip and upgrade
                    python get-pip.py
                    python -m pip install --upgrade pip

                    REM Install required Python packages
                    python -m pip install -r requirements.txt

                    REM Install PyInstaller
                    python -m pip install pyinstaller
                    '''
                }
            }
        }

        stage('Build Binary (PyInstaller)') {
            steps {
                dir('Web-Calculator') {
                    bat '''
                    pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --name CalculatorApp Calculator.py
                    '''
                }
            }
        }

        stage('Archive PyInstaller Artifact') {
            steps {
                archiveArtifacts artifacts: 'Web-Calculator\\dist\\*', fingerprint: true
            }
        }

        stage('Build Docker Image') {
            steps {
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




