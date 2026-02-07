pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: env.BRANCH_NAME,
                    url: 'https://github.com/Ojasvi-19/Web-Calculator.git'
            }
        }

        stage('Build Binary (PyInstaller)') {
            steps {
                dir("${env.WORKSPACE}/Web-Calculator"){
                    sh '''
                    cd /workspace/Web-Calculator
                    python3 -m pip install --upgrade pip
                    pip install -r Requirements.txt
                    pip install pyinstaller
                    pyinstaller --onefile --add-data "templates:templates" Calculator.py
                    '''
                    }
                }
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


