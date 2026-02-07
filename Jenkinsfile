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
                    pip install --no-cache-dir pyinstaller &&
                    pyinstaller --onefile Calculator.py
                  "
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







